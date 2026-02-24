CREATE TABLE IF NOT EXISTS acoes (
  id SERIAL PRIMARY KEY,
  ticker VARCHAR(10) NOT NULL,
  preco NUMERIC(10, 2) NOT NULL,
  variacao_pct NUMERIC(5, 2),
  volume BIGINT,
  data_coleta TIMESTAMP DEFAULT NOW()
)