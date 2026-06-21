import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ========== FİLTRE ==========
def calculate(measure_func, df, filter_str):
    """CALCULATE: measure'ı belirtilen filtre ile hesaplar."""
    return measure_func(df.query(filter_str))

def filter_table(df, condition):
    return df.query(condition)

def all_except(df, columns):
    # Gerçek bağlam olmadığı için df döndürüyoruz.
    return df

# ========== ZAMAN ZEKASI ==========
def sameperiodlastyear(df, date_col, measure_col):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df['_ly_date'] = df[date_col] - pd.DateOffset(years=1)
    merged = pd.merge(df, df, left_on=date_col, right_on='_ly_date', suffixes=('', '_ly'))
    return merged.set_index(date_col)[measure_col + '_ly']

def datesytd(df, date_col):
    today = pd.Timestamp.today()
    return df[df[date_col] <= today]

def totalmtd(df, date_col, value_col):
    df[date_col] = pd.to_datetime(df[date_col])
    last_date = df[date_col].max()
    month_start = last_date.replace(day=1)
    return df[(df[date_col] >= month_start) & (df[date_col] <= last_date)][value_col].sum()

# Diğer zaman zekası fonksiyonları benzer şekilde eklenebilir.
# (PREVIOUSMONTH, STARTOFMONTH, CLOSINGBALANCEMONTH...)

# ========== MATEMATİK / İSTATİSTİK ==========
def sumx(df, column):
    return df[column].sum()

def averagex(df, column):
    return df[column].mean()

def rankx(df, order_col, ascending=False):
    return df[order_col].rank(ascending=ascending)

def countx(df, column):
    return df[column].count()

def distinctcount(df, column):
    return df[column].nunique()

# ========== MANTIKSAL ==========
def if_func(cond, true_val, false_val):
    return true_val if cond else false_val

def switch(expr, *args):
    for i in range(0, len(args), 2):
        if expr == args[i]:
            return args[i+1]
    return args[-1] if len(args) % 2 else None

# ========== METİN ==========
def concatenatex(df, col, delimiter=', '):
    return delimiter.join(df[col].astype(str).tolist())

def left(text, num):
    return str(text)[:num]

def right(text, num):
    return str(text)[-num:]

def upper(text):
    return str(text).upper()

def lower(text):
    return str(text).lower()

# ========== TABLO ==========
def summarize(df, group_col, agg_dict):
    return df.groupby(group_col).agg(agg_dict).reset_index()

def addcolumns(df, new_col, expr):
    df[new_col] = eval(expr, {'df': df})
    return df

def selectcolumns(df, cols):
    return df[cols]