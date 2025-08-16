import pandas as pd

data = {'Nombre': ['Jeisson', 'Brandon', 'Bairon', 'Samantha', 'Alejandro'],
        'Edad': [20, 21, 19, 22, 20],
        'Nota1': [2.5, 3.0, 3.5, 2.0, 4.0],
        'Nota2': [3.0, 3.5, 4.0, 2.5, 4.5]}
df = pd.DataFrame(data)

df['Promedio'] = (df['Nota1'] + df['Nota2']) / 2

aprobados_df = df[df['Promedio'] >= 3.0]
print("Estudiantes con promedio mayor o igual a 3.0:")
print(aprobados_df)

#Se genera el el csv
aprobados_df.to_csv('aprobados.csv', index=False)

print("\nLos estudiantes que han pasado se han guardado en 'aprobados.csv'")