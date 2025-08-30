import numpy as np

data = np.array([3,7,np.nan,15,np.nan,21])

print("Donde hay una NaN?", np.isnan(data))
