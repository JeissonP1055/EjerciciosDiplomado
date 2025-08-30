import numpy as np
#-----------------------------------------------------------------------
#Primer Punto
#---------------------------------------------------------------------

data = np.array([90, 110, np.nan, 85, 100, 95, np.nan, 120, 105, 99])
print("=" * 90)
print(f"1.Deteccion De Datos Faltantes:")
print("=" * 90)
print(f"arreglo original", data)
print(f"¿Dónde hay NaN?", np.isnan(data))

#-----------------------------------------------------------------------------------
#Segundo punto fue fusionado con el tercero por temas de practicidad
#-----------------------------------------------------------------------------

data = np.array([90, 110, np.nan, 85, 100, 95, np.nan, 120, 105, 99])

cleaned = data[~np.isnan(data)]

promedio_validos = cleaned.mean()
minimo = cleaned.min()
maximo = cleaned.max()
print("=" * 90)
print(f"2 y 3. Ocultar NaN y Reemplazar NaN:")
print("=" * 90)
print(f"Datos válidos (sin NaN): {cleaned}")
print(f"Promedio de glucosa: {promedio_validos:.2f}")
print(f"Valor mínimo: {minimo}")
print(f" Valor máximo: {maximo}")

promedio = np.nanmean(data)

data_reemplazado = np.nan_to_num(data, nan=promedio)

print(f"Promedio usado para reemplazo: {promedio:.2f}")
print(f"Datos con NaN reemplazados: {data_reemplazado}")

#-------------------------------------------------------------------------
#Cuarto Punto
#-------------------------------------------------------------------------------

pesos = np.array([50, 72, 65, 80, 90, 100])

print("=" * 90)
print(f"4.Normalizacion de datos:")
print(f"=" * 90)
print(f" Normalización de datos (Min-Max)")
print(f"Pesos originales:", pesos)


pesos_norm = (pesos - np.min(pesos)) / (np.max(pesos) - np.min(pesos))

print("Pesos normalizados (0 a 1):", pesos_norm)

#-----------------------------------------------------------------------------
#Quinto punto
#---------------------------------------------------------------------------------------

comidas = np.array(["Pizza", "Pasta", "Pizza", "Sushi", "Hamburguesa", "Sushi", "Pizza"])
comidas_unicas = np.unique(comidas)

print("=" * 90)
print(f"5.Eliminacion de Datos Repetidos")
print("=" * 90)
print(f"Comidas originales:", comidas)
print(f"Opciones únicas:", comidas_unicas)

#----------------------------------------------------------------------------------------------
#Sexto Punto
#---------------------------------------------------------------------------------------------

ventas = np.array([250, 300, 150, 400, 500, 200, 350])
print("=" * 90)
print(f"6.Calculo de ventas de la semana:")
print("=" * 90)
print(f"Ventas registradas:", ventas)

venta_min = np.min(ventas)
venta_max = np.max(ventas)

print(f" Venta mínima: {venta_min} mil pesos")
print(f" Venta máxima: {venta_max} mil pesos")


