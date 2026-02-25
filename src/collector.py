from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()

api_key = os.environ.get('BRAPI_TOKEN')

TICKERS = [
    "PETR4", "VALE3", "ITUB4", "BBDC4", "BBAS3", 
    "WEGE3", "EMBR3", "TOTS3", "VIVT3",            
    "MGLU3", "RENT3", "LREN3",                      
    "SUZB3", "JBSS3", "ABEV3",                      
    "RDOR3", "HAPV3"                                  
]
def get_data(tickers = TICKERS):
    symbols = ','.join(tickers)
    url = f'https://brapi.dev/api/quote/{symbols}?token={api_key}'
    request_data = requests.get(url)
    data = request_data.json()['results']

    df = pd.DataFrame(data)[['symbol', 'regularMarketPrice', 'regularMarketChangePercent',
    'regularMarketVolume']]
    df.columns = ['ticker','preco', 'variacao_pct', 'volume']
    return df
