import pandas as pd

def clean_data(df):
    if df is not None:
        # تنظيف البيانات الأساسي
        df = df.drop_duplicates()
        df = df.fillna(0)
        return df
    return None
