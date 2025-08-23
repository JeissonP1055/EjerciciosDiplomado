import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
ventas = pd.read_csv("clase 3/ventas.csv")

# --- Manejo de nulos ---
print("Valores nulos por columna:")
print(ventas.isnull().sum())

# Imputación según columnas reales
if 'sucursal' in ventas.columns:
    ventas['sucursal'] = ventas['sucursal'].fillna('Desconocida')

if 'categoria' in ventas.columns:
    ventas['categoria'] = ventas['categoria'].fillna('Sin categoria')

# --- Manejo de duplicados ---
print("Duplicados antes:", ventas.duplicated().sum())
ventas = ventas.drop_duplicates()
print("Duplicados después:", ventas.duplicated().sum())

# --- Estandarización manual ---
num_cols = ventas.select_dtypes(include=['int64','float64']).columns
ventas[num_cols] = (ventas[num_cols] - ventas[num_cols].mean()) / ventas[num_cols].std()

print("Columnas numéricas estandarizadas:")
print(ventas[num_cols].head())

# --- Visualización ---
for col in num_cols:
    plt.figure(figsize=(10,4))

    # Histograma
    plt.subplot(1, 3, 1)
    plt.hist(ventas[col], bins=20, edgecolor="black")
    plt.title(f"Histograma - {col}")

    # Boxplot
    plt.subplot(1, 3, 2)
    plt.boxplot(ventas[col], vert=False)
    plt.title(f"Boxplot - {col}")

    # Gráfico de densidad
    plt.subplot(1, 3, 3)
    ventas[col].plot(kind="kde")
    plt.title(f"Densidad - {col}")

    plt.tight_layout()
    plt.show()
