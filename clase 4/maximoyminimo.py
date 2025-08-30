import numpy as np

edades = np.array([15,22,19,30,25,40,18,28,35,50,45,33])
print ("edades registradas:", edades)

print("persona mas joven:", np.min(edades), "años")
print("persona mas adulta:", np.max(edades), "años")

print("Rango de edades:", np.max(edades)-np.min(edades),"años")