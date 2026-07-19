from pathlib import Path
import numpy as np
import pandas as pd

x = np.arange(1, 101)
result = pd.DataFrame({"x": x, "x_squared": x**2})
Path("results").mkdir(exist_ok=True)
result.to_csv("results/python-results.csv", index=False)
print(result.tail())
