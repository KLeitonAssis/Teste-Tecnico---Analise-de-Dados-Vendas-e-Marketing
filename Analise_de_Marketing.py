import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

banco = sqlite3.connect('vendas_marketing.db')
cursor = banco.cursor()

############################################################
############### Eficiência das Campanhas: ##################
############################################################

# Selecionando Tabelas
campanhas_df = pd.read_sql_query("SELECT * FROM Campanhas_Marketing", banco)
interacoes_df = pd.read_sql_query("SELECT * FROM Interacoes_Marketing", banco)

#separando a conversao
conversoes_df = interacoes_df[interacoes_df['tipo_interacao'] == 'Conversão']
conversoes_por_campanha = conversoes_df.groupby('id_campanha').size().reset_index(name='num_conversoes')

# realizando os inner joins das tabelas
merged_df = pd.merge(campanhas_df, conversoes_por_campanha, on='id_campanha', how='inner')
merged_df = pd.merge(merged_df, interacoes_df[['id_campanha']], on='id_campanha', how='inner')

# dropando as duplicadas se houver
merged_df = merged_df.drop_duplicates()

# realizando a divisao para taxa_conversao
merged_df['taxa_conversao'] = merged_df['num_conversoes'] / merged_df['orcamento']

# realizando a divisao para eficiencia
merged_df['eficiencia'] = merged_df['num_conversoes'] / merged_df['custo']

# deixando em ordem decrescente
campanhas_eficientes = merged_df.sort_values(by='eficiencia', ascending=False)

# inserindo 'nome_campanha', 'num_conversoes','taxa_conversao' ,'eficiencia'
result_df = (campanhas_eficientes[['nome_campanha', 'num_conversoes','taxa_conversao' ,'eficiencia']])

# deixando em ordem decrescente
result_df = result_df.sort_values(by='taxa_conversao', ascending=False)

# realizando o gráfico pelo Matplotlib
plt.figure(figsize=(10, 6))
bars = plt.bar(result_df['nome_campanha'], result_df['taxa_conversao'], color='skyblue')
plt.xlabel('nome_campanha')
plt.ylabel('taxa_conversao')
plt.title('Eficiência das Campanhas:')
plt.xticks(rotation=45)
plt.grid(axis='y')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 3), ha='center', va='bottom')

plt.show()

############################################################
################## Canais de Marketing: ####################
############################################################

# selecionaod tabelas
campanhas_df = pd.read_sql_query("SELECT * FROM Campanhas_Marketing", banco)
interacoes_df = pd.read_sql_query("SELECT * FROM Interacoes_Marketing", banco)

#realizando o inner join
merged_df = pd.merge(campanhas_df, interacoes_df, on='id_campanha', how='inner')

#realizando o group by
canais = merged_df.groupby(['canal_marketing'])['tipo_interacao'].count().reset_index()
canais = canais.sort_values(by='tipo_interacao', ascending=False)

# realizando o gráfico pelo Matplotlib

plt.figure(figsize=(10, 6))
bars = plt.bar(canais['canal_marketing'], canais['tipo_interacao'], color='skyblue')
plt.xlabel('canal_marketing')
plt.ylabel('tipo_interacao')
plt.title('Canais de Marketing:')
plt.xticks(rotation=45)
plt.grid(axis='y')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 3), ha='center', va='bottom')

plt.show()

############################################################