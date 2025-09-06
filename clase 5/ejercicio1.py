import pandas as pd,numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
#
sns.set_theme()

df = pd.read_csv("ventas_anuales.csv")
print("Primeras:\n",df.head())

df = df.sort_values(
    by ="Periodo",
    key = lambda s: pd.to_datetime(s,format = "%Y-%m")
)

fig, ax =plt.subplots(figsize=(9,4))

ax.plot(df ["Periodo"],df["Ingreso"],marker="o",label="Ingresos 2025")
ax.set_title("EcoMarket - Ingresos por mes (2025)")
ax.set_xlabel("Periodo (YYYY-MM)")
ax.set_ylabel("Ingresos")

for tick in ax.get_xticklabels():
    tick.set_rotation(45)

ax.grid(True, alpha=0.3)
ax.legend()

file_max = df["Ingreso"].idxmax()
mes_top = df.loc[file_max,"Periodo"]
valor_top = df.loc[file_max,"Ingreso"]

x_top = list(df["Periodo"]).index(mes_top)

ax.annotate(
    f"Mejor mes: {mes_top}\n${valor_top:,.0f}",
    xy=(x_top, valor_top),
    xytext = (0.65, 0.75),
    textcoords="axes fraction",
    arrowprops=dict(arrowstyle="->")
)

fig.tight_layout()
plt.show()
