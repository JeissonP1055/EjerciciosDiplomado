

import pandas as pd
import numpy as np
import json
from pathlib import Path


DATA_PATH = Path("ventas_tienda.csv")        # archivo crudo
EXPORT_XLSX = Path("ventas_limpio.xlsx")     # Excel limpio
EXPORT_JSON = Path("resumen.json")           # resumen en JSON


df = pd.read_csv(DATA_PATH, parse_dates=["fecha"], encoding="utf-8")


if df["fecha"].isna().any():
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce", infer_datetime_format=True)


df.columns = [c.strip().lower() for c in df.columns]


for c in ["sucursal", "categoria", "producto"]:
    if c in df.columns:
        df[c] = (
            df[c].astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.upper()
        )


df = df.drop_duplicates()


df = df.dropna(subset=["fecha", "sucursal", "categoria", "producto"])


for col in ["unidades", "precio"]:
    med_by_prod = df.groupby("producto")[col].transform("median")
    med_by_suc = df.groupby("sucursal")[col].transform("median")
    global_med = df[col].median()
    df[col] = df[col].fillna(med_by_prod)
    df[col] = df[col].fillna(med_by_suc)
    df[col] = df[col].fillna(global_med)
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["unidades", "precio"])


df["ingreso"] = df["unidades"] * df["precio"]


def kpis_por(grupo_cols):
    total_ingresos = df.groupby(grupo_cols)["ingreso"].sum().rename("total_ingresos")
    ticket_promedio = df.groupby(grupo_cols)["ingreso"].mean().rename("ticket_promedio")
    top_products = (
        df.groupby(grupo_cols + ["producto"])["ingreso"].sum()
        .sort_values(ascending=False)
        .groupby(level=grupo_cols, group_keys=False)
        .head(3)
        .reset_index()
    )
    top3 = (
        top_products.groupby(grupo_cols)
        .apply(lambda x: [{"producto": r["producto"], "ingreso": float(r["ingreso"])} for _, r in x.iterrows()])
        .rename("top_3_productos")
    )
    out = (
        pd.concat([total_ingresos, ticket_promedio], axis=1)
        .join(top3, how="left")
        .reset_index()
    )
    return out

kpi_sucursal = kpis_por(["sucursal"])
kpi_categoria = kpis_por(["categoria"])


df["mes"] = df["fecha"].dt.to_period("M").astype(str)
pivot_mensual = pd.pivot_table(
    df, index="mes", columns="categoria", values="ingreso", aggfunc="sum", fill_value=0
)


df["ingreso_original"] = df["ingreso"]

def replace_outliers_with_median(group):
    q1 = group["ingreso"].quantile(0.25)
    q3 = group["ingreso"].quantile(0.75)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    median_val = group["ingreso"].median()
    mask = (group["ingreso"] < low) | (group["ingreso"] > high)
    group.loc[mask, "ingreso"] = median_val
    group["outlier_flag"] = mask.astype(int)
    return group

df = df.groupby("sucursal", group_keys=False).apply(replace_outliers_with_median)
outlier_rate = df["outlier_flag"].mean()


kpi_sucursal_post = kpis_por(["sucursal"])
kpi_categoria_post = kpis_por(["categoria"])
pivot_mensual_post = pd.pivot_table(
    df, index="mes", columns="categoria", values="ingreso", aggfunc="sum", fill_value=0
)


with pd.ExcelWriter(EXPORT_XLSX, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="datos_limpios", index=False)
    kpi_sucursal_post.to_excel(writer, sheet_name="kpi_sucursal", index=False)
    kpi_categoria_post.to_excel(writer, sheet_name="kpi_categoria", index=False)
    pivot_mensual_post.to_excel(writer, sheet_name="pivot_mensual")

resumen = {
    "filas_finales": int(len(df)),
    "n_sucursales": int(df["sucursal"].nunique()),
    "n_categorias": int(df["categoria"].nunique()),
    "total_ingresos": float(df["ingreso"].sum()),
    "tasa_outliers": float(outlier_rate),
    "top_sucursal": kpi_sucursal_post.loc[kpi_sucursal_post["total_ingresos"].idxmax(), "sucursal"],
    "top_categoria": kpi_categoria_post.loc[kpi_categoria_post["total_ingresos"].idxmax(), "categoria"],
}

with open(EXPORT_JSON, "w", encoding="utf-8") as f:
    json.dump(resumen, f, ensure_ascii=False, indent=2)

print("Exportaciones listas:")
print(f"- {EXPORT_XLSX}")
print(f"- {EXPORT_JSON}")
