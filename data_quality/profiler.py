import pandas as pd
import numpy as np

def generate_quality_profile(df):
    profile = {}
    profile['row_count'] = len(df)
    profile['column_count'] = len(df.columns)
    profile['missing'] = df.isnull().sum().to_dict()
    profile['duplicate_rows'] = df.duplicated().sum()
    profile['outliers'] = {}
    for col in df.select_dtypes(include=np.number).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower) | (df[col] > upper)][col]
        profile['outliers'][col] = len(outliers)
    # Genel skor: 1.0 mükemmel
    score = 1.0
    if profile['row_count'] == 0:
        score = 0.0
    else:
        missing_ratio = sum(profile['missing'].values()) / (profile['row_count'] * profile['column_count'])
        dup_ratio = profile['duplicate_rows'] / profile['row_count']
        outlier_ratio = sum(profile['outliers'].values()) / (profile['row_count'] * profile['column_count'])
        score = max(0.0, 1.0 - (missing_ratio * 0.4 + dup_ratio * 0.3 + outlier_ratio * 0.3))
    profile['quality_score'] = round(score, 2)
    return profile