import numpy as np

nombres = np.array(["Bairon","Daniel","Brandon","Mary","ivan","Mary","sara","Daniel"])

#eliminar duplicados con np.unique

unique_name = np.unique(nombres)

print ("original:", nombres)
print ("sin duplicados", unique_name)

