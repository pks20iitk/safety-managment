"""
azure_ai_search.py

This module provides a custom Azure Search client for various search functionalities, including vector search, hybrid search, exhaustive KNN search, and semantic search.
"""

import os
import logging
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import (
    VectorizedQuery,
    QueryType,
)
from rule_parser.embedding import EmbeddingProcessor 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomAzureSearch:
    """
    A custom Azure Search client for various search functionalities.
    """

    def __init__(self, endpoint, key, index_name, number_results_to_return, number_near_neighbors, model_name, embedding_field_name, semantic_config):
        """
        Initializes the CustomAzureSearch client.

        Args:
            endpoint (str): The Azure Search service endpoint.
            key (str): The Azure Search service key.
            index_name (str): The name of the search index.
            number_results_to_return (int): The number of results to return.
            number_near_neighbors (int): The number of near neighbors.
            model_name (str): The name of the language model.
            embedding_field_name (str): The name of the embedding field.
            semantic_config (str): The semantic configuration name.
        """
        self.endpoint = endpoint
        self.key = key
        self.index_name = index_name
        self.model_name = model_name
        self.embedding_field_name = embedding_field_name
        self.number_results_to_return = number_results_to_return
        self.number_near_neighbors = number_near_neighbors
        self.semantic_config = semantic_config
        self.client = SearchClient(endpoint=self.endpoint, index_name=self.index_name, credential=AzureKeyCredential(self.key))
        logger.info("CustomAzureSearch client initialized")

    @staticmethod
    def get_embedding_query_vector(query):
        """
        Retrieves the embedding query vector.

        Args:
            query (str): The search query.

        Returns:
            torch.Tensor: The embedding query vector.
        """
        query_vector = get_embeddings(query, os.getenv("MODEL"))
        logger.info("Embedding query vector retrieved")
        return query_vector

    def get_results_vector_search(self, query, filter_value=None, list_fields=None):
        """
        Returns the results of a vector search.

        Args:
            query (str): The search query.
            filter_value (str, optional): The filter to apply to the search.
            list_fields (list, optional): List of fields to return.

        Returns:
            dict: The search results.
        """
        logger.info("Getting results for vector search...")
        vector_query = self.get_vectorized_query(query)
        filter_expression = self.prepare_filter_expression(filter_value) if filter_value else None
        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            select=list_fields,
            top=self.number_results_to_return,
            filter=filter_expression,
        )
        logger.info("Received results for vector search.")
        return self.__get_results_to_return(results)

    @staticmethod
    def prepare_filter_expression(filter_value):
        """
        Prepares the filter expression from the user input string.

        Args:
            filter_value (str): The user input filter string.

        Returns:
            str: The filter expression.
        """
        if filter_value:
            filter_values = [keyword.strip() for keyword in filter_value.split(',')]
            filter_clauses = [f"search.ismatch('{word}', 'line', 'full', 'any')" for word in filter_values]
            filter_expression = ' or '.join(filter_clauses)
            logger.info("Filter expression created.")
            return filter_expression
        return None

    def get_vectorized_query(self, query, exhaustive_knn=False):
        """
        Returns a vectorized query.

        Args:
            query (str): The search query.
            exhaustive_knn (bool, optional): Whether to use exhaustive KNN.

        Returns:
            VectorizedQuery: The vectorized query.
        """
        logger.info("Getting vectorized query...")
        query_vector = self.get_embedding_query_vector(query)
        vector_query = VectorizedQuery(
            vector=query_vector,
            k_nearest_neighbors=self.number_near_neighbors,
            fields=self.embedding_field_name,
            exhaustive_knn=exhaustive_knn,
        )
        logger.info("Got vectorized query.")
        return vector_query

    @staticmethod
    def __get_results_to_return(results):
        """
        Returns the results to return.

        Args:
            results: The search results.

        Returns:
            list: The results to return.
        """
        results_to_return = []
        for result in results:
            results_to_return.append(result)
        logger.info("Returned results.")
        return results_to_return

    def get_results_hybrid_search(self, query, filter_value=None, list_fields=None):
        """
        Returns the results of a hybrid search.

        Args:
            query (str): The search query.
            filter_value (str, optional): The filter to apply to the search.
            list_fields (list, optional): List of fields to return.

        Returns:
            dict: The search results.
        """
        logger.info("Getting results for hybrid search...")
        vector_query = self.get_vectorized_query(query)
        filter_expression = self.prepare_filter_expression(filter_value) if filter_value else None
        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            select=list_fields,
            top=self.number_results_to_return,
            filter=filter_expression,
        )
        logger.info("Received results for hybrid search.")
        return self.__get_results_to_return(results)

    def get_results_semantic_search(self, query, filter_value, list_fields=None):
        """
        Returns the results of a semantic search.

        Args:
            query (str): The search query.
            filter_value (str): The filter to apply to the search.
            list_fields (list, optional): List of fields to return.

        Returns:
            dict: The search results.
        """
        logger.info("Getting results for semantic search...")
        vector_query = self.get_vectorized_query(query)
        filter_expression = self.prepare_filter_expression(filter_value) if filter_value else None
        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            select=list_fields,
            query_type=QueryType.SEMANTIC,
            semantic_configuration_name=self.semantic_config,
            top=self.number_results_to_return,
            filter=filter_expression,
        )
        logger.info("Received results for semantic search.")
        return self.__get_results_to_return(results)