import requests
from xml.etree import ElementTree

def get_abstract_from_pubmed(query):
    #Arquivo
    arq = open('csv_buscas.csv','w',encoding='utf-8')
    
    # Base URL das E-utilities
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    # Fazendo a busca do artigo no PubMed usando ESearch
    esearch_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmode=xml&retstart=0&retmax=10&"
    #print(esearch_url)
    esearch_response = requests.get(esearch_url)
    esearch_tree = ElementTree.fromstring(esearch_response.content)

    # Obtendo o ID do artigo
    id_list = esearch_tree.find("IdList")
    #print('ID LIST:', len(id_list))
    if id_list is None or len(id_list) == 0:
        return "Nenhum artigo encontrado para a consulta fornecida."


    for id in id_list.iter('Id'):
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
        arq.writelines(pmid+';'+title_f+';'+abstract_text)
        

    return abstract_text.strip() if abstract_text else "Abstract não disponível."

# Exemplo de uso
query = "pediatric AND suspension AND flavor"
abstract = get_abstract_from_pubmed(query)
#print(abstract)