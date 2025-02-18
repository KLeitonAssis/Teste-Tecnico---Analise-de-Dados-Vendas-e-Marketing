import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

banco = sqlite3.connect('vendas_marketing.db')
cursor = banco.cursor()

############################################################
##################### Relação Temporal: ####################
############################################################

# Selecionando Tabelas
df_venda = pd.read_sql_query("SELECT * FROM Vendas", banco)
df_produto = pd.read_sql_query("SELECT * FROM Produtos", banco)
df_campanha = pd.read_sql_query("SELECT * FROM Campanhas_Marketing", banco)

# Convertendo as colunas de data para datetime
df_venda['data_venda'] = pd.to_datetime(df_venda['data_venda'])
df_campanha['data_inicio'] = pd.to_datetime(df_campanha['data_inicio'])
df_campanha['data_fim'] = pd.to_datetime(df_campanha['data_fim'])

# Unindo os DataFrames
df = pd.merge(df_venda, df_produto, on='id_produto', how='left')
df = pd.merge(df, df_campanha, on='id_campanha', how='left')

# Criando uma coluna indicando se a venda ocorreu antes, durante ou depois do início da campanha
df['periodo_relativo'] = df.apply(lambda row: 'Antes' if row['data_venda'] < row['data_inicio'] else ('Durante' if row['data_venda'] <= row['data_fim'] else 'Depois'), axis=1)

# Agrupando os dados por produto e período relativo
vendas_agrupadas = df.groupby(['nome_produto', 'periodo_relativo'])['quantidade'].sum().unstack(fill_value=0)

# Exibindo o DataFrame com vendas antes, durante e depois das campanhas
##print(vendas_agrupadas)


# realizando o gráfico pelo Matplotlib
ax = vendas_agrupadas.plot(kind='bar', figsize=(10, 6))
plt.title('Vendas de Produtos Durante e Depois das Campanhas de Marketing')
plt.xlabel('Produto')
plt.ylabel('Quantidade Vendida')
plt.legend(title='Período Relativo')
plt.xticks(rotation=45)
plt.grid(True)

for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

plt.show()

############################################################
##################### Análise Regional: ####################
############################################################


# Selecionando Tabelas
df_venda = pd.read_sql_query("SELECT * FROM Vendas", banco)
df_campanha = pd.read_sql_query("SELECT * FROM Campanhas_Marketing", banco)
df_cliente = pd.read_sql_query("SELECT * FROM Clientes", banco)

# Unindo os DataFrames
df = pd.merge(df_venda, df_campanha, on='id_campanha', how='left')
df = pd.merge(df, df_cliente, on='id_cliente', how='left')

df['nome_campanha'] = df['nome_campanha'].fillna('campanha indefinida')

# Agrupando os dados por cidade e campanha de marketing
vendas_por_cidade = df.groupby(['cidade', 'nome_campanha'])['id_venda'].nunique().unstack(fill_value=0)

# Ordenando em ordem decrescente pelo total de vendas e limitando a 5 resultados
vendas_por_cidade['total_vendas'] = vendas_por_cidade.sum(axis=1)

#deixando em ordem decrescente e pegando os 5 primeiros
vendas_por_cidade = vendas_por_cidade.sort_values(by='total_vendas', ascending=False).head(5)



# realizando o gráfico pelo Matplotlib
ax = vendas_por_cidade.plot(kind='bar', figsize=(14, 7))
plt.title('Vendas por Cidade e Campanha de Marketing')
plt.xlabel('Cidade')
plt.ylabel('Valor Total das Vendas')
plt.legend(title='Campanha de Marketing')
plt.xticks(rotation=45)
plt.grid(True)

# Adicionando os números dos resultados em cima das barras
for p in ax.patches:
    ax.annotate(str(round(p.get_height(), 2)), (p.get_x() + p.get_width() / 2, p.get_height()), ha='center')

plt.show()
