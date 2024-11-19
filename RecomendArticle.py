# -*- coding: utf-8 -*-
import pandas as pd
import pickle
from time import time

from ControllerOpenAI import ControllerOpenAI


class RecomendArticle:
    def __init__(self, dataset_path):
        #Get OpenAI Controller instace
        self.openai_ctr = ControllerOpenAI()
        #Archive base name
        #dataset_path = dataset_path
        #Load CSV
        df = pd.read_csv(dataset_path, delimiter='\t',)
        #filtering DF
        self.abstract_article_list = df['ABSTRACT'].tolist()
        # set path to embedding cache
        self.embedding_cache_path = dataset_path.split('.')[0]+'.pkl'
        # load the cache if it exists, and save a copy to disk
        try:
            self.embedding_cache = pd.read_pickle(self.embedding_cache_path)
        except FileNotFoundError:
            self.embedding_cache = {}
        with open(self.embedding_cache_path, "wb") as embedding_cache_file:
            pickle.dump(self.embedding_cache, embedding_cache_file)

        #return (self.openai_ctr,embedding_cache,embedding_cache_path)

    def embedding_from_dataset(self,texto, modelo) -> list:

        """Retorna o embedding de um texto, usando cache para evitar recomputação."""
        if (texto, modelo) not in self.embedding_cache:
            self.embedding_cache[(texto, modelo)] = self.openai_ctr.get_embedding(texto, modelo)
            with open(self.embedding_cache_path, "wb") as cache_file:
                pickle.dump(self.embedding_cache, cache_file)

        return self.embedding_cache[(texto, modelo)]
    
    def print_neighbors_by_distance(
            self,
            query_string,
            indices_of_neighbors,
            k_neighbors,
            distances
    ):
        k_counter = 0
        for i in indices_of_neighbors:
            # skip any strings that are identical matches to the starting string
            if query_string == self.abstract_article_list[i]:
                continue
            # stop after printing out k articles
            if k_counter >= k_neighbors:
                break
            k_counter += 1

            # print out the similar strings and their distances
            print(
                f"""
            --- Recomendação #{k_counter} (nearest neighbor {k_counter} of {k_neighbors}) ---
            String: {self.abstract_article_list[i]}
            Distance: {distances[i]:0.3f}"""
            )

    def print_recommendations_from_strings(
        self,
        index_of_source_string: int,
        k_nearest_neighbors: int = 1,
        model="text-embedding-3-small",
    ) -> list[int]:

        """Print out the k nearest neighbors of a given string."""
        # get embeddings for all strings
        embeddings = [self.embedding_from_dataset(string, modelo=model) for string in self.abstract_article_list]

        # get the embedding of the source string
        query_embedding = embeddings[index_of_source_string]

        # get distances between the source embedding and other embeddings (function from ControllerOpenAI.py)
        distances = self.openai_ctr.distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")
        
        # get indices of nearest neighbors (function from utils.utils.embeddings_utils.py)
        indices_of_nearest_neighbors = self.openai_ctr.indices_of_nearest_neighbors_from_distances(distances)

        indices_of_furtherest_neighbors = self.openai_ctr.indices_of_furtherest_neighbors_from_distances(distances)

        # print out source string
        query_string = self.abstract_article_list[index_of_source_string]
        print(f"Source string: {query_string}")
        # print out its k nearest neighbors
        k_counter = 0
        for i in indices_of_nearest_neighbors:
            # skip any strings that are identical matches to the starting string
            if query_string == self.abstract_article_list[i]:
                continue
            # stop after printing out k articles
            if k_counter >= k_nearest_neighbors:
                break
            k_counter += 1

            # print out the similar strings and their distances
            print(
                f"""
            --- Recomendação #{k_counter} (nearest neighbor {k_counter} of {k_nearest_neighbors}) ---
            String: {self.abstract_article_list[i]}
            Distance: {distances[i]:0.3f}"""
            )
            
        return indices_of_nearest_neighbors
    
        ### METHOD TEST 
        # RecomendArticle.print_neighbors_by_distance(query_string, indices_of_furtherest_neighbors, k_nearest_neighbors, distances)

if __name__ == "__main__":
    ra = RecomendArticle('csv_buscas_encoded.csv')
    articles = ra.print_recommendations_from_strings(0, 5)
    print(articles)