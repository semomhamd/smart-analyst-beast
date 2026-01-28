import pandas as pd

def load_file(file):
    ext = file.name.split(".")[-1].lower()

    if ext in ["xlsx", "xls"]:
        return pd.read_excel(file)
    elif ext == "csv":
        return pd.read_csv(file)
    else:
        raise ValueError("نوع الملف غير مدعوم")

def clean_df(df):
    df = df.copy()
    df.columns = df.columns.astype(str)
    return df
