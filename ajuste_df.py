import pandas as pd

name = 'csv_buscas_unificado.csv'

df = pd.read_csv(name)
print(df)
df = df[['PMID', 'abstract',
       'Title', 'Authors', 'Citation', 'First Author', 'Journal/Book',
       'Publication Year', 'Create Date', 'PMCID', 'NIHMS ID', 'DOI']]

df = df[df['abstract'].isnull() == False]
df = df.drop_duplicates()

nome_ajustado = name.split('.')[0]+'_ajustado.csv'

df.to_csv(nome_ajustado)

