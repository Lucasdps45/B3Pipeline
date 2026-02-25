import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

db_url = os.environ.get('B3_DATABASE_URL')
engine = create_engine(db_url)


def load_to_db(df):
    df.to_sql(
        'acoes',
        engine, 
        if_exists='append',
        index=False,
        chunksize=1000,
        method='multi'
    )