"""
algorithm.py

This module provides functions to retrieve search results using the CustomAzureSearch client.
"""

import logging
import os
from azure_ai_search import CustomAzureSearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
SERVICE_ENDPOINT = os.getenv("SERVICE_ENDPOINT")
AZURE_AI_SEARCH_KEY = os.getenv("AZURE_AI_SEARCH_KEY")
AZURE_SEARCH_SEMANTIC_CONFIG_NAME = os.getenv("AZURE_SEARCH_SEMANTIC_CONFIG_NAME")
LIST_OF_FIELDS = ["book", "chapter", "section", "chunk_content", "page"]
EMBEDDING_FIELD_NAME = "embedding"

def get_results_vector_search(prompt, filter_value, number_of_search_results, k_nearest_neighbors, hybrid=False, exhaustive_knn=False, semantic_search=False):
    """
    Retrieves the results of a vector search using Azure AI Search.

    Args:
        prompt (str): Search query.
        filter_value (str): Filter value (optional).
        number_of_search_results (int): Number of results to return.
        k_nearest_neighbors (int): Nearest neighbors to be searched.
        hybrid (bool): Whether to use hybrid search (default=False).
        exhaustive_knn (bool): Whether to use exhaustive KNN search (default=False).
        semantic_search (bool): Whether to use semantic search (default=False).

    Returns:
        tuple: (results_content, results_source, page)
    """
    logging.info(f"Searching with query '{prompt}' and filter '{filter_value}'")
    
    custom_azure_search = CustomAzureSearch(
        endpoint=SERVICE_ENDPOINT,
        key=AZURE_AI_SEARCH_KEY,
        index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
        number_results_to_return=number_of_search_results,
        model_name=os.getenv("MODEL"),
        number_near_neighbors=k_nearest_neighbors,
        embedding_field_name=EMBEDDING_FIELD_NAME,
        semantic_config=AZURE_SEARCH_SEMANTIC_CONFIG_NAME,
    )

    if hybrid:
        logging.info("Using hybrid search")
        return custom_azure_search.get_results_hybrid_search(prompt, filter_value, LIST_OF_FIELDS)
    
    if semantic_search:
        logging.info("Using semantic search")
        return custom_azure_search.get_results_semantic_search(prompt, filter_value, LIST_OF_FIELDS)
    
    logging.info("Using pure vector search")
    return custom_azure_search.get_results_vector_search(prompt, filter_value, LIST_OF_FIELDS)