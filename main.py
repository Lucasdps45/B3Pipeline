from src.collector import get_brapi_b3_data
from src.transformer import transform_data
from src.loader import load_to_db
from src.alerter import verify_variation

df = get_brapi_b3_data()

transformed_df = transform_data(df)

load_to_db(transformed_df)

verify_variation(transformed_df)

