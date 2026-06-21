from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd

class SMOTESynthetic:
    """SMOTE tabanlı sentetik veri üretici."""
    def generate(self, df, target_col, n_samples=100):
        from imblearn.over_sampling import SMOTE
        X = df.drop(columns=[target_col])
        y = df[target_col]
        smote = SMOTE(sampling_strategy='auto', k_neighbors=min(5, len(df)-1))
        X_syn, y_syn = smote.fit_resample(X, y)
        return pd.concat([pd.DataFrame(X_syn, columns=X.columns),
                          pd.DataFrame(y_syn, columns=[target_col])], axis=1)