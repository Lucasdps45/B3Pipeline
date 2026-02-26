import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

@st.cache_resource
def get_connection():
    db_url = os.environ.get("B3_DATABASE_URL")
    return create_engine(db_url)

@st.cache_data(ttl=300)
def get_data():
    engine = get_connection()
    return pd.read_sql_query('SELECT DISTINCT ON (ticker) ticker, preco, \
     variacao_pct, volume, data_coleta \
    FROM acoes \
    ORDER BY ticker, data_coleta DESC', engine)


st.set_page_config(page_title='Ações B3', layout='wide')
st.title('Ações B3')


df = get_data()[['ticker', 'preco', 'variacao_pct', 'volume', 'data_coleta']]
df = df.rename(columns={
    'ticker': 'Ação',
    'preco': 'Preço (R$)',
    'variacao_pct': 'Variação (%)',
    'volume': 'Volume',
    'data_coleta': 'Última Atualização'
})
df['Última Atualização'] = pd.to_datetime(df['Última Atualização']).dt.strftime('%d/%m/%Y | %H:%M')

col1, col2, col3 = st.columns(3)
em_alta = len(df[df['Variação (%)' ]> 0])
em_baixa = len(df[df['Variação (%)'] < 0])

col1.metric('🟢 Em Alta', em_alta)
col2.metric('🔴 Em Baixa', em_baixa)
col3.metric('📊 Total Monitoradas', len(df))



styled_df = (
    df.style
    .map(
        lambda x: 'color: green' if x > 0 else 'color: red',
        subset=['Variação (%)'])
    .format({
        'Preço(R$)': lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        'Variação (%)': lambda x: f"{x:.2f}%".replace(".", ",")
    })
)

st.dataframe(styled_df, width='stretch')

ticker_selecionado = st.selectbox("Selecione uma ação", df['Ação'].unique())

query = f"""
    SELECT preco, data_coleta 
    FROM acoes 
    WHERE ticker = '{ticker_selecionado}'
    ORDER BY data_coleta
"""

historico = pd.read_sql_query(query, get_connection())

st.line_chart(historico.set_index('data_coleta')['preco'])