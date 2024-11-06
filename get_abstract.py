import requests
from xml.etree import ElementTree
import pandas as pd
import numpy as np
import os
import glob

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"



diretorio = 'D:/Documentos/CEDERJ/6º P/TCC/Trabalho/repositorio/TCC_/arquivos_csv/'
diretorio_com_abs = 'D:/Documentos/CEDERJ/6º P/TCC/Trabalho/repositorio/TCC_/arquivos_csv_com_abs/'
diretorio_unidos = 'D:/Documentos/CEDERJ/6º P/TCC/Trabalho/repositorio/TCC_/arquivos_csv_unidos/'

#df = pd.read_csv(diretorio+'csv-pediatricA-set.csv')

#print(df)

def get_abs(pmid):
    try:
        # Usando EFetch para obter o abstract do artigo
        efetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={pmid}&retmode=xml&rettype=abstract"
        #print(efetch_url)
        efetch_response = requests.get(efetch_url)
        efetch_tree = ElementTree.fromstring(efetch_response.content)

        # Extraindo o abstract
        abstract_text = ""
        for abstract in efetch_tree.iter("AbstractText"):
            abstract_text += abstract.text + " "

        #Extraindo o title
        title_f = ''
        for title in efetch_tree.iter('ArticleTitle'):
            title_f = title.text

        #Salvar no arquivo
        #arq.writelines(pmid+'\t'+title_f+'\t'+abstract_text.replace('\n',' ')+'\n')
        return (abstract_text.replace('\n',' '),pmid)
    except:
        print('Erro')

    return (abstract_text.strip(),0) if abstract_text else ("",0)


def join_dfs(df1, df2):
    ''' Une o DF com o ABS com o DF sem ABSTRACT'''
    n1 = df1.split('.')[0].split('/')[-1] 
    n2 = df2.split('.')[0].split('/')[-1]
    df1 = pd.read_csv(df1)
    df2 = pd.read_csv(df2)

    r = pd.merge(df1, df2, on='PMID', how='inner')

    r.to_csv(diretorio_unidos+'join_'+n1+'_'+n2+'_'+'.csv')
    return r


def join_joined():
    # Caminho do diretório com os arquivos CSV

    # Listar todos os arquivos CSV no diretório
    arquivos_csv = glob.glob(os.path.join(diretorio_unidos, "*.csv"))

    # Lista para armazenar cada DataFrame
    dataframes = []

    # Ler cada arquivo CSV e adicioná-lo à lista de DataFrames
    for arquivo in arquivos_csv:
        df = pd.read_csv(arquivo)
        dataframes.append(df)

    # Concatenar todos os DataFrames em um único DataFrame
    df_unificado = pd.concat(dataframes, ignore_index=True)

    df_unificado.to_csv('csv_buscas_unificado.csv')

to_join = {
    'PMID': [],
    'abstract':[]
}

#df_n = join_dfs(diretorio+'csv-amoxicilli-set.csv',diretorio+'ABS_csv-amoxicilli-set.csv')

#print(df_n.columns)

df = []
arquivos = os.listdir(diretorio)
arquivos_abs = os.listdir(diretorio_com_abs)
print(f"Arquivos no diretório '{diretorio}':")
for arquivo in arquivos:
    try:
        if arquivo not in arquivos_abs:
            print("Arquivo atual:", arquivo)
            df = pd.read_csv(diretorio+arquivo)

            for id in range(0,df['PMID'].shape[0]):
                to_join['PMID'].append(df['PMID'][id])
                to_join["abstract"].append(get_abs(df['PMID'][id])[0])

            df_to_join = pd.DataFrame(to_join)
            df_to_join.to_csv(diretorio_com_abs+arquivo)
            join_dfs(diretorio_com_abs+arquivo, diretorio+arquivo)

            to_join = {
                'PMID': [],
                'abstract':[]
            }
        else:
            print('já está no arquivo com abs')
    except:
        print('Erro no for')

join_joined()