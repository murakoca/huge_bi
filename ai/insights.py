from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

def anomaly_detection(df, contamination=0.05):
    model = IsolationForest(contamination=contamination, random_state=42)
    df = df.copy()
    df['anomaly'] = model.fit_predict(df.select_dtypes(include=np.number))
    return df

def smart_narrative(df, measures):
    parts = []
    for col, func in measures.items():
        if func == 'sum':
            val = df[col].sum()
            parts.append(f"Toplam {col}: {val:,.2f}")
        elif func == 'mean':
            val = df[col].mean()
            parts.append(f"Ortalama {col}: {val:,.2f}")
    return " | ".join(parts)