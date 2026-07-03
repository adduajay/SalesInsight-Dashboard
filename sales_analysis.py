
import pandas as pd
def clean_data(path):
    df=pd.read_csv(path)
    df.drop_duplicates(inplace=True)
    df.fillna(0,inplace=True)
    return df
