import pandas as pd
from collector import get_data

def transform_data(df):
    df['data_coleta'] = pd.Timestamp.now()
    return df

if __name__ == '__main__':
    print(transform_data(get_data()))
