# -*- coding: utf-8 -*-
import pandas as pd
import pickle
from time import time
#import numpy as np


from ControllerOpenAI import ControllerOpenAI


class RecomendArticle:
    def __init__(self, dataset_path, readed_abstract):
        #Get OpenAI Controller instace
        self.openai_ctr = ControllerOpenAI()
        #Load CSV
        df = pd.read_csv(dataset_path)
        #Load abstract as a list from df
        self.abstract_article_list = df['ABSTRACT'].tolist()
        self.abstract_article_list.insert(0, readed_abstract)
        #Load DOIs as a list from df
        self.doi_article_list = df['DOI'].tolist()
        #Set path to embedding cache
        self.embedding_cache_path = dataset_path.split('.')[0]+'.pkl'
        #Load the cache if it exists, and save a copy to disk
        try:
            self.embedding_cache = pd.read_pickle(self.embedding_cache_path)
        except FileNotFoundError:
            self.embedding_cache = {}
        with open(self.embedding_cache_path, "wb") as embedding_cache_file:
            pickle.dump(self.embedding_cache, embedding_cache_file)

    def embedding_from_dataset(self, text, model) -> list:

        """Return text embedding, using cache to avoid recomputing."""
        if (text, model) not in self.embedding_cache:
            self.embedding_cache[(text, model)] = self.openai_ctr.get_embedding(text, model)
            with open(self.embedding_cache_path, "wb") as cache_file:
                pickle.dump(self.embedding_cache, cache_file)

        return self.embedding_cache[(text, model)]
    
    def print_neighbors_by_distance(
            self,
            query_string,
            indices_of_neighbors,
            k_neighbors,
            distances
    ):
        
        k_counter = 0
        article_return = []
        for i in indices_of_neighbors:
            #Skip any strings that are identical matches to the starting string
            if query_string == self.abstract_article_list[i]:
                continue
            #Stop after printing out k articles
            if k_counter >= k_neighbors:
                break
            k_counter += 1

            article_return.append(
                {
                    'article_priority': k_counter,
                    'abstract': self.abstract_article_list[i],
                    'distance': distances[i],
                    'doi': self.doi_article_list[i]
                }
            )
        return article_return

    def print_recommendations_from_strings(
            self,
            k_nearest_neighbors: int = 1,
            model="text-embedding-3-small",
            ) -> list[int]:

        """Print out the k nearest neighbors of a given string."""
        #Define index source
        index_of_source_string = 0

        #Get embeddings for all strings
        embeddings = [self.embedding_from_dataset(string, model=model) for string in self.abstract_article_list]

        #Get the embedding of the source string
        query_embedding = embeddings[index_of_source_string]

        #Get distances between the source embedding and other embeddings (function from ControllerOpenAI.py)
        distances = self.openai_ctr.distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")

        #Get indices of nearest neighbors (function from from ControllerOpenAI.py)
        indices_of_nearest_neighbors = self.openai_ctr.indices_of_nearest_neighbors_from_distances(distances)

        indices_of_furtherest_neighbors = self.openai_ctr.indices_of_furtherest_neighbors_from_distances(distances)

        #Get query_string from abstract
        query_string = self.abstract_article_list[index_of_source_string]
        
        articles = self.print_neighbors_by_distance(distances=distances,indices_of_neighbors=indices_of_nearest_neighbors,k_neighbors=k_nearest_neighbors, query_string=query_string)
            
        return (query_string, articles, indices_of_nearest_neighbors, indices_of_furtherest_neighbors, embeddings)
