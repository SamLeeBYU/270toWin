import pandas as pd
import numpy as np

class Analysis:

    def __init__(self, data, name, truth="2020"):

        self.data = data
        self.name = name
        self.data["Democrat"] = pd.to_numeric(self.data["Democrat"], errors='coerce')
        self.data["Republican"] = pd.to_numeric(self.data["Republican"], errors='coerce')
        self.data["Democrat"] = self.data["Democrat"].fillna(0).astype(int)
        self.data["Republican"] = self.data["Republican"].fillna(0).astype(int)
        self.data = self.data.drop_duplicates()

        self.data.to_csv(f"maps/{name}-map.csv", index=False)

        self.truth = pd.read_csv(f"maps/{truth}-map.csv")

    def metrics(self):

        D = np.sum(self.data["Democrat"])
        R = np.sum(self.data["Republican"])