import pandas as pd

def load_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    elif file.name.endswith('.ods'):
        return pd.read_excel(file, engine='odf')
    else:
        raise ValueError("نوع الملف غير مدعوم!")

def clean_df(df):
    # تنظيف أولي
    return df.dropna(how='all')
