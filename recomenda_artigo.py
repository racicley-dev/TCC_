# -*- coding: utf-8 -*-
import pandas as pd
import pickle
from time import time

from utils.embeddings_utils import (
    get_embedding,
    distances_from_embeddings,
    tsne_components_from_embeddings,
    chart_from_components,
    indices_of_nearest_neighbors_from_distances,
)


#Definindo nome do modelo
EMBEDDING_MODEL = "text-embedding-3-small"

embedding_cache_path = "csv_buscas.pkl"
embedding_cache = pd.read_pickle(embedding_cache_path)

def setting_up():
    #Nome do arquivo
    dataset_path = "csv_buscas.csv"
    #Leitura do CSV
    df = pd.read_csv(dataset_path)
    #Filtrando o DataFrame
    df_novo = df[['TITLE', 'ABSTRACT']]
    # set path to embedding cache
    embedding_cache_path = "csv_buscas.pkl"

    # load the cache if it exists, and save a copy to disk
    try:
        embedding_cache = pd.read_pickle(embedding_cache_path)
    except FileNotFoundError:
        embedding_cache = {}
    with open(embedding_cache_path, "wb") as embedding_cache_file:
        pickle.dump(embedding_cache, embedding_cache_file)



def embedding_from_dataset(texto, modelo) -> list:
    inicio_embedding = time()
    """Retorna o embedding de um texto, usando cache para evitar recomputação."""
    if (texto, modelo) not in embedding_cache:
        embedding_cache[(texto, modelo)] = get_embedding(texto, modelo)
        with open(embedding_cache_path, "wb") as cache_file:
            pickle.dump(embedding_cache, cache_file)

    tempo_embedding = time() - inicio_embedding
    print('Tempo de execução do embedding: ', tempo_embedding)
    return embedding_cache[(texto, modelo)]

def print_recommendations_from_strings(
    strings: list[str],
    index_of_source_string: int,
    k_nearest_neighbors: int = 1,
    model=EMBEDDING_MODEL,
) -> list[int]:
    inicio_recomendacao = time()
    """Print out the k nearest neighbors of a given string."""
    # get embeddings for all strings
    embeddings = [embedding_from_dataset(string, modelo=model) for string in strings]

    # get the embedding of the source string
    query_embedding = embeddings[index_of_source_string]

    # get distances between the source embedding and other embeddings (function from utils.embeddings_utils.py)
    distances = distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")
    
    # get indices of nearest neighbors (function from utils.utils.embeddings_utils.py)
    indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)

    # print out source string
    query_string = strings[index_of_source_string]
    print(f"Source string: {query_string}")
    # print out its k nearest neighbors
    k_counter = 0
    for i in indices_of_nearest_neighbors:
        # skip any strings that are identical matches to the starting string
        if query_string == strings[i]:
            continue
        # stop after printing out k articles
        if k_counter >= k_nearest_neighbors:
            break
        k_counter += 1

        # print out the similar strings and their distances
        print(
            f"""
        --- Recomendação #{k_counter} (nearest neighbor {k_counter} of {k_nearest_neighbors}) ---
        String: {strings[i]}
        Distance: {distances[i]:0.3f}"""
        )
    tempo_recomendacao = time() - inicio_recomendacao
    print("Tempo de execução da recomendação: ", tempo_recomendacao) 
    return indices_of_nearest_neighbors



def main(df):
    article_abstracts = df["ABSTRACT"].tolist()

    pubmed_articles = print_recommendations_from_strings(
        strings=article_abstracts,  # let's base similarity off of the article description
        index_of_source_string=0,  # articles similar to the first one about Tony Blair
        k_nearest_neighbors=5,  # 5 most similar articles
    )

    print(pubmed_articles)

if __name__ == "__main__":
    df = pd.read_csv('csv_buscas.csv')

    main(df)