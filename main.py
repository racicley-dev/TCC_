import requests
from xml.etree import ElementTree
import pandas as pd
import numpy as np

def get_abstract_from_pubmed(query):
    retstart = 0
    retmax = 200

    #Arquivo
    arq = open('csv_buscas.csv','a',encoding='utf-8')
    #arq.write("PMID"+'\t'+"TITLE"+'\t'+"ABSTRACT"+'\n')

    for i in range(0,10000,10):
        
        print(str(i)+" "+10 * '-----')

        
        
        # Base URL das E-utilities
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

        # Fazendo a busca do artigo no PubMed usando ESearch
        esearch_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmode=xml&retstart={i}&retmax={i+10}&"
        print(esearch_url)
        esearch_response = requests.get(esearch_url)
        esearch_tree = ElementTree.fromstring(esearch_response.content)

        # Obtendo o ID do artigo
        id_list = esearch_tree.find("IdList")
        #print('ID LIST:', len(id_list))
        if id_list is None or len(id_list) == 0:
            return ("Nenhum artigo encontrado para a consulta fornecida.","0")

    
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

# Exemplo de uso
#query = ["pediatric AND suspension AND flavor"]
#abstract = get_abstract_from_pubmed(query)
#print(abstract)

list_pmid = []
a = pd.read_fwf('queries.txt')
for query in a['search'].tolist():
    ret = get_abstract_from_pubmed(query)
    if ret[1] != 0:
        if ret[0] not in list_pmid:
            list_pmid.append(ret[0])




