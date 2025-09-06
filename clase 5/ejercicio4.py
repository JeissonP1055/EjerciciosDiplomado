import numpy as np
import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker   

# Estilo Global
sns.set_theme(style="whitegrid", font_scale=1.08)

plt.rcParams["axes.titleweight"] = "bold" 
plt.rcParams["font.family"] = "DejaVu Sans"

COLORS = {
    "primary": "#138FED", # Series Principales
    "accent": "#EDC113",  # Resaltar Anotaciones
    "muted": "#C4C4C4",   # Elementos Secundarios
    "line2": "#866400",   # Segundas Lineas
}

def read_csv_smart(path, parse_dates=None):
    try:
        return pd.read_csv(path, parse_dates=parse_dates)
    except Exception:
        return pd.read_csv(path, sep=";", decimal=",", parse_dates=parse_dates)

customers = read_csv_smart("customers.csv", parse_dates=["signup_date"])
orders = read_csv_smart("orders.csv", parse_dates=["order_date"])
items = read_csv_smart("items.csv")

print("Customers", customers)
print("Orders", orders)
print("Items", items)

def clean_str(s):
    return s.strip().title() if isinstance(s, str) else s

for col in ["city", "channel"]:
    if col in orders.columns:
        orders[col] = orders[col].apply(clean_str)

for col in ["product", "category"]:
    if col in items.columns:
        items[col] = items[col].apply(clean_str)

customers["signup_date"] = pd.to_datetime(customers.get("signup_date"), errors="coerce")
orders["order_date"] = pd.to_datetime(orders.get("order_date"), errors="coerce")
items["units"] = pd.to_numeric(items.get("units"), errors="coerce")
items["unit_price"] = pd.to_numeric(items.get("unit_price"), errors="coerce")

orders_before = len(orders)
items_before = len(items)

orders = orders.dropna(subset=["order_id", "customer_id", "order_date"])
items = items.dropna(subset=["order_id", "units", "unit_price"])

orders = orders.drop_duplicates(subset=["order_id"])
items = items.drop_duplicates(subset=["order_id", "product", "category"])

items = items[(items["units"] > 0) & (items["unit_price"] > 0)]
items = items[items["order_id"].isin(orders["order_id"])]

# Crear DB en memoria
con = sqlite3.connect(":memory:")
customers.to_sql("customers", con, index=False, if_exists="replace")
items.to_sql("items", con, index=False, if_exists="replace")
orders.to_sql("orders", con, index=False, if_exists="replace")

sql_order_totals = """
WITH line_totals AS(
    SELECT order_id, (units*unit_price) AS line_totals
    FROM items 
) 
SELECT o.order_id, o.customer_id, o.order_date, o.city, o.channel,
    SUM(l.line_totals) AS order_total
FROM orders o
JOIN line_totals l USING (order_id)
GROUP BY o.order_id, o.customer_id, o.order_date, o.city, o.channel
"""
order_totals = pd.read_sql_query(sql_order_totals, con, parse_dates=["order_date"])

try:
    con.close()
except:
    pass

# KPIs
order_totals["mes"] = order_totals["order_date"].dt.to_period("M").astype(str)
ingresos_mes = (order_totals.groupby("mes", as_index=False)["order_total"]
                .sum()
                .rename(columns={"order_total": "ingreso_mes"})
                .sort_values("mes"))

ingresos_ciudad = (order_totals.groupby("city", as_index=False)["order_total"]
                .sum()
                .rename(columns={"order_total": "ingreso_ciudad"})
                .sort_values("ingreso_ciudad", ascending=False))

customer_totals = (order_totals.groupby("customer_id", as_index=False)
                .agg(n_orders=("order_id", "nunique"),
                     customer_total=("order_total", "sum"))
                .sort_values("customer_total", ascending=False))

total_revenue = float(order_totals["order_total"].sum())
num_customers = customer_totals["customer_id"].nunique()
aov = float(order_totals["order_total"].mean())
repeat_rate = float((customer_totals["n_orders"] > 1).mean())

# Curva de pareto
pareto = customer_totals.copy()
pareto["cum_ingreso"] = pareto["customer_total"].cumsum()
pareto["cum_pct_clientes"] = (np.arange(1, len(pareto) + 1) / max(1, len(pareto)))
pareto["cum_ptc_ingreso"] = pareto["cum_ingreso"] / max(1, pareto["customer_total"].sum())

fig, axes = plt.subplots(2, 2, figsize=(12, 7))
(ax1, ax2), (ax3, ax4) = axes 

# Lineal - ingresos por mes
ax1.plot(ingresos_mes["mes"], ingresos_mes["ingreso_mes"],
         marker="o", color=COLORS.get("primary", "#138FED"))
ax1.set(title="Ingresos por mes", xlabel="Mes", ylabel="Ingresos")
for t in ax1.get_xticklabels(): 
    t.set_rotation(45)
ax1.yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))

# Barras - ranking por ciudad
topN = ingresos_ciudad.head(8).reset_index(drop=True)
sns.barplot(data=topN, x="ingreso_ciudad", y="city", ax=ax2, palette="viridis")
ax2.set(title="Ranking por Ciudad", xlabel="Ingresos", ylabel="Ciudad")
ax2.xaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))

# KDE - monto por pedido
if "channel" in order_totals.columns and order_totals["channel"].nunique() >= 2:
    hue_col, data_kde = "channel", order_totals.dropna(subset=["order_total", "channel"])
else:
    hue_col = "city"
    data_kde = order_totals[order_totals["city"].isin(ingresos_ciudad.head(3)["city"])]

sns.kdeplot(data=data_kde, x="order_total", hue=hue_col, fill=True,
            common_norm=False, bw_adjust=0.9, cut=0, alpha=0.25,
            linewidth=1.6, ax=ax3)
ax3.set(title=f"KDE - Monto por Pedido por {hue_col}", xlabel="Monto por Pedido", ylabel="Densidad")
ax3.xaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))

# Pareto
ax4.plot(pareto["cum_pct_clientes"], pareto["cum_ptc_ingreso"],
         marker="o", color=COLORS.get("line2", "#866400"))
ax4.axhline(0.8, color=COLORS.get("accent", "#EDC113"), linestyle="--", linewidth=1)
ax4.axhline(0.2, color=COLORS.get("primary", "#138FED"), linestyle="--", linewidth=1)
ax4.set(title="Pareto 80/20", xlabel="% clientes (acum.)", ylabel="% ingreso (acum.)", xlim=(0,1), ylim=(0,1))
ax4.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
ax4.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))

# Título general
fig.suptitle("Dashboard de Eco Market", fontsize=14, fontweight="bold", y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

