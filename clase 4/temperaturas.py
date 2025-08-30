import numpy as np

temperaturas = np.array([28,30,np.nan,32,31,np.nan,29])

print ("datos originales", temperaturas)

prome_tem = np.nanmean(temperaturas)
print ("el promedio es:", prome_tem)
temperaturas_limpio= np.nan_to_num(temperaturas,nan=prome_tem)

print("datos limpios", temperaturas_limpio)