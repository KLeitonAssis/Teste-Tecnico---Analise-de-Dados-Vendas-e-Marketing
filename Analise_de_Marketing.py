import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

banco = sqlite3.connect('vendas_marketing.db')
cursor = banco.cursor()


##Eficiência das Campanhas:

campanhas_df = pd.read_sql_query("SELECT * FROM Campanhas_Marketing", banco)
interacoes_df = pd.read_sql_query("SELECT * FROM Interacoes_Marketing", banco)
conversoes_df = interacoes_df[interacoes_df['tipo_interacao'] == 'Conversão']
conversoes_por_campanha = conversoes_df.groupby('id_campanha').size().reset_index(name='num_conversoes')


merged_df = pd.merge(campanhas_df, conversoes_por_campanha, on='id_campanha', how='inner')
merged_df = pd.merge(merged_df, interacoes_df[['id_campanha']], on='id_campanha', how='inner')
merged_df = merged_df.drop_duplicates()

merged_df['taxa_conversao'] = merged_df['num_conversoes'] / merged_df['orcamento']

merged_df['eficiencia'] = merged_df['num_conversoes'] / merged_df['custo']

campanhas_eficientes = merged_df.sort_values(by='eficiencia', ascending=False)
print(campanhas_eficientes.head())

result_df = (campanhas_eficientes[['nome_campanha', 'num_conversoes','taxa_conversao' ,'eficiencia']])
result_df = result_df.sort_values(by='taxa_conversao', ascending=False)
print(result_df)




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

##Canais de Marketing:

