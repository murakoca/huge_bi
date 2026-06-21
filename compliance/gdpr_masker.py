import pandas as pd

def mask_pii(df, columns):
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: '*' * len(str(x)))
    return df