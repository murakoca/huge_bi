import pandas as pd

class Transformer:
    @staticmethod
    def split_column(df, col, delimiter, new_cols):
        df[new_cols] = df[col].str.split(delimiter, expand=True)
        return df

    @staticmethod
    def filter_rows(df, condition):
        return df.query(condition)

    @staticmethod
    def merge_tables(left, right, on, how='inner'):
        return pd.merge(left, right, on=on, how=how)

    @staticmethod
    def pivot(df, index, columns, values, aggfunc='sum'):
        return pd.pivot_table(df, index=index, columns=columns, values=values, aggfunc=aggfunc).reset_index()

    @staticmethod
    def unpivot(df, id_vars, value_vars):
        return pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='Variable', value_name='Value')

    @staticmethod
    def change_type(df, column, dtype):
        df[column] = df[column].astype(dtype)
        return df