import mysql.connector
import pandas as pd

#Conexión a la base de datos 
conexion = mysql.connector.connect(
    host="localhost",      
    user="root",           
    password="",            
    database="tarea"      
)

cursor = conexion.cursor()

#Mostrar tablas
tablas = ["ventas", "clientes", "devoluciones"]
for tabla in tablas:
    print(f"\n--- Datos en {tabla} ---")
    cursor.execute(f"SELECT * FROM {tabla}")
    for fila in cursor.fetchall():
        print(fila)

#Consulta 1
query_ingresos = """
SELECT c.region, v.producto, SUM(v.precio * v.cantidad) AS ingreso_total
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id
GROUP BY c.region, v.producto;
"""
cursor.execute(query_ingresos)
resultados_ingresos = cursor.fetchall()

df_ingresos = pd.DataFrame(resultados_ingresos, columns=["region", "producto", "ingreso_total"])
print("\n--- Ingreso total por región y producto ---")
print(df_ingresos)

#Consulta 2
query_bogota = """
SELECT c.nombre, SUM(v.precio * v.cantidad) AS ingreso_total
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id
WHERE c.ciudad = 'Bogotá'
GROUP BY c.nombre;
"""
cursor.execute(query_bogota)
resultados_bogota = cursor.fetchall()

df_bogota = pd.DataFrame(resultados_bogota, columns=["cliente", "ingreso_total"])
print("\n--- Clientes de Bogotá con ingreso total ---")
print(df_bogota)

# resultados a CSV 
df_ingresos.to_csv("ingreso_region_producto.csv", index=False, encoding="utf-8")
df_bogota.to_csv("clientes_bogota.csv", index=False, encoding="utf-8")

print("\n✅ Resultados exportados a 'ingreso_region_producto.csv' y 'clientes_bogota.csv'.")


cursor.close()
conexion.close()
