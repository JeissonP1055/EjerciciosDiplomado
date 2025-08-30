import numpy as np
data = np.array([90, 110, np.nan, 85, 100, 95, np.nan, 120, 105, 99])
print("Donde hay una NaN?", np.isnan(data))

print(~np.isnan(data))

cleaned = data[~np.isnan(data)]

print("datos limpios:", cleaned)

promedio = np.nanmean(data)
print("promedio calculado", promedio)

filled = np.nan_to_num(data, nan=promedio)
print("nueva lista con reemprazados:", filled)