import pandas as pd


def transform_data(df):
    df['data_coleta'] = pd.Timestamp.now()
    return df


