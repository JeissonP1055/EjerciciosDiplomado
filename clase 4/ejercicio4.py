import numpy as np

matematicas = 150 #sobre 200
ingles = 80 #sobre 100 
etica= 8 #sobre 10

notas= np.array([matematicas,ingles,etica])
maximos= np.array([200,100,10])

notas_nomalizadas= notas/maximos

print("notas originales:",notas)
print("maximos posibles:",notas)
print("notas normalizadas:",notas_nomalizadas)
