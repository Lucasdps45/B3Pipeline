import streamlit as st
import os
import pandas as pd
import plotly.express as px 
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



df = df.sort_values('Variação (%)', ascending=False)

def color_row(row):
    if row['Variação (%)'] > 0:
        return ['background-color: #1a3a1a'] * len(row)
    elif row['Variação (%)'] < 0:
        return ['background-color: #3a1a1a'] * len(row)
    return [''] * len(row)

styled_df = (
    df.style
    .apply(color_row, axis=1)
    .format({
        'Preço (R$)': lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        'Variação (%)': lambda x: f"{x:.2f}%".replace(".", ",")
    })
)

st.dataframe(styled_df, hide_index=True, use_container_width=True)

df['cor'] = df['Variação (%)'].apply(lambda x: 'green' if x > 0 else 'red')

fig = px.bar(
    df,
    x='Ação',
    y='Variação (%)',
    color='cor',
    color_discrete_map={'green': 'green', 'red': 'red'}
)

fig.update_layout(xaxis_tickangle=-45, showlegend=False)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Histórico de Preços")
ticker_selecionado = st.selectbox("Selecione uma ação", df['Ação'].unique())

query = f"""
    SELECT preco, data_coleta 
    FROM acoes 
    WHERE ticker = '{ticker_selecionado}'
    ORDER BY data_coleta
"""

historico = pd.read_sql_query(query, get_connection())

fig2 = px.line(
    historico,
    x='data_coleta',
    y='preco',
    title=f'Histórico de Preços - {ticker_selecionado}',
    labels={'data_coleta': 'Data', 'preco': 'Preço (R$)'}
)

st.plotly_chart(fig2, use_container_width=True)