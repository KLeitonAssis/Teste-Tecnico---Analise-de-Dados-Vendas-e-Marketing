import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

banco = sqlite3.connect('vendas_marketing.db')
cursor = banco.cursor()

## Total de Vendas por Canal:

query = """SELECT VALOR_TOTAL,CANAL_AQUISICAO 
            FROM Vendas 
            WHERE data_venda BETWEEN  date('now', 'start of month', '-3 months', 'start of month') AND date('now', 'start of month', 'start of month', '-1 day')"""
df = pd.read_sql_query(query,banco)

vendas_mensais = df.groupby(['canal_aquisicao'])['valor_total'].sum().reset_index() 
##print(vendas_mensais)

plt.figure(figsize=(10, 6))
bars = plt.bar(vendas_mensais['canal_aquisicao'], vendas_mensais['valor_total'], color='skyblue')
plt.xlabel('Canal de Aquisição')
plt.ylabel('Valor Total')
plt.title('Valor Total de Vendas por Canal de Aquisição (Últimos 3 Meses)')
plt.xticks(rotation=45)
plt.grid(axis='y')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

plt.show()

## Top Produtos:

vendas_df = pd.read_sql_query("SELECT * FROM Vendas", banco)
produtos_df = pd.read_sql_query("SELECT * FROM Produtos", banco)
merged_df = pd.merge(vendas_df, produtos_df, on='id_produto', how='inner')

result_df = (merged_df.groupby('nome_produto')
             .agg(media_valor=('valor_total', lambda x: round(x.sum() / x.count(), 2)))
             .reset_index()
             .sort_values(by='media_valor', ascending=False)
             .head(5))

##print(result_df)

plt.figure(figsize=(10, 6))
bars = plt.bar(result_df['nome_produto'], result_df['media_valor'], color='skyblue')
plt.xlabel('nome_produto')
plt.ylabel('Valor Total')
plt.title('Top Produtos')
plt.xticks(rotation=45)
plt.grid(axis='y')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')
             
plt.show()


## Segmentação de Clientes:

vendas_df = pd.read_sql_query("SELECT * FROM Vendas", banco)
clientes_df = pd.read_sql_query("SELECT * FROM Clientes", banco)
merged_df = pd.merge(vendas_df, clientes_df, on='id_cliente', how='inner')

result_df = (merged_df.groupby('segmento')
             .agg(ticket_medio=('valor_total', lambda x: round(x.sum() / x.count(), 2)))
             .reset_index()
             .sort_values(by='ticket_medio', ascending=False))

##print(result_df)

plt.figure(figsize=(10, 6))
bars = plt.bar(result_df['segmento'], result_df['ticket_medio'], color='skyblue')
plt.xlabel('segmento')
plt.ylabel('Valor Total')
plt.title('Top Produtos')
plt.xticks(rotation=45)
plt.grid(axis='y')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')
             
plt.show()

## Sazonalidade:

vendas_df = pd.read_sql_query("SELECT * FROM Vendas", banco)

vendas_df['data_venda'] = pd.to_datetime(vendas_df['data_venda'])

vendas_df['ano'] = vendas_df['data_venda'].dt.year
vendas_df['mes'] = vendas_df['data_venda'].dt.month

vendas_df['ano'] = vendas_df['ano'].astype(int)
vendas_df['mes'] = vendas_df['mes'].astype(int)

vendas_mensais = vendas_df.groupby(['ano', 'mes'])['valor_total'].sum().reset_index()

##print(vendas_df.head())

from datetime import datetime
def create_date(row):
    return datetime(year=int(row['ano']), month=int(row['mes']), day=1)

vendas_mensais['data'] = vendas_mensais.apply(create_date, axis=1)

##.print(vendas_mensais.head())

plt.figure(figsize=(12, 6))
plt.plot(vendas_mensais['data'], vendas_mensais['valor_total'], marker='o', linestyle='-')
plt.title('Padrão de Vendas ao Longo do Ano')
plt.xlabel('Data')
plt.ylabel('Total de Vendas (R$)')
plt.grid(True)
plt.show()

""" Ao analizar o grafico podemos realizar a conclusão que os picos de vendas são realizados em momentos de festas, feriados e promoções de queima de estoque. 
Vendas podem cair após grandes eventos ou feriados devido à redução no consumo além de mudanças econômicas e climáticas. """