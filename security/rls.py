def apply_rls(df, column, allowed_values):
    return df[df[column].isin(allowed_values)]

def apply_ols(df, visible_columns):
    return df[visible_columns]