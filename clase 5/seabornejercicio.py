import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

df = pd.read_csv("tickets_soporte.csv", parse_dates=["fecha"])

fig, ax= plt.subplots(figsize=(8, 4))

sns.histplot(data=df, x="tiempo_respuesta_min", bins=5, kde=True, ax=ax)

ax.set_title("Detalle Mesa de Soporte (Tiempos de Respuesta)")
ax.set_xlabel("Minutos")
ax.set_ylabel("Cantidad de Casos")

media = df["tiempo_respuesta_min"].mean()
ax.axvline(media, linestyle="--", linewidth=1, label=f"media= {media:.1f} min")

ax.legend()
plt.tight_layout()
plt.show()
