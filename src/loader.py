import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from collector import get_data
from transformer import transform_data

load_dotenv()

db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url)

df = transform_data(get_data())

df.to_sql(
    'acoes',
    engine, 
    if_exists='append',
    index=False,
    chunksize=1000,
    method='multi'
)