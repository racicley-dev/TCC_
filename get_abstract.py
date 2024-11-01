import requests
from xml.etree import ElementTree
import pandas as pd
import numpy as np

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


df = pd.read_csv('csv-pediatricA-set.csv')

print(df['PMID'].shape[0])



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

    return (abstract_text.strip(),0) if abstract_text else ("Abstract não disponível.",0)


for id in range(0,71):
    print('ABSTRACT::: ', get_abs(df['PMID'][id]))

'''
for id in id_list.iter('Id'):
    try:
        pmid = id.text

        #pmid = id_list[3].text

        # Usando EFetch para obter o abstract do artigo
        efetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={pmid}&retmode=xml&rettype=abstract"
        print(efetch_url)
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
        arq.writelines(pmid+'\t'+title_f+'\t'+abstract_text.replace('\n',' ')+'\n')
        return ("",pmid)
    except:
        print('Erro')
        continue
        

    return (abstract_text.strip(),0) if abstract_text else ("Abstract não disponível.",0)
''' 