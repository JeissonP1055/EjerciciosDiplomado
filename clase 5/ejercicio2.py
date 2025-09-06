import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
df = pd.read_csv("ventas_por_ciudad.csv")
df = df.sort_values(by="ingresos", ascending=False)
fig, ax = plt.subplots(figsize=(9, 4))
pos = list(range(len(df)))
ax.barh(pos, df["ingresos"])
maxv = df["ingresos"].max()
ax.set_xlim(0, maxv*1.15)
padding =  maxv *0.02

ax.set_yticks(pos)
ax.set_yticklabels(df["ciudad"])
ax.set_title("EcoMarket - Ingresos por ciudad")
ax.set_xlabel("Ingresos")
ax.set_ylabel("Ciudad")
ax.invert_yaxis()
ax.grid(axis="x", alpha=0.2)
for i, valor in enumerate(df['ingresos']):
    ax.text(valor + padding, i, f"${valor:,.0f}",
            va = "center", ha = "left", fontsize=9, clip_on=False
        
    )
plt.tight_layout()
plt.show()