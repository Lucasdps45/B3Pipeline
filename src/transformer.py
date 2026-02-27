import pandas as pd


def transform_data(df):
    
    df['preco'] = df['preco'].astype(float)
    df['variacao_pct'] = df['variacao_pct'].astype(float)
    df['volume'] = df['volume'].astype(int)
    df['data_coleta'] = pd.to_datetime(df['data_coleta'])


    df = df.sort_values('data_coleta')
    df = df.drop_duplicates(subset=['ticker'], keep='last')
    
    return df


