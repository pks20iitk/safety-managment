"""
config.py

This module loads and manages configuration settings for the Azure AI Search application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure AI Search Configuration
AZURE_SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")
AZURE_SEARCH_ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
AZURE_SEARCH_SEMANTIC_CONFIG_NAME = os.getenv("AZURE_SEARCH_SEMANTIC_CONFIG_NAME")
NUMBER_OF_RESULTS_TO_RETURN = os.getenv("NUMBER_OF_RESULTS_TO_RETURN")
NUMBER_OF_NEAR_NEIGHBORS = os.getenv("NUMBER_OF_NEAR_NEIGHBORS")

# Azure OpenAI Configuration
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_ID = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")
AZURE_OPENAI_DEPLOYMENT_ID_AGENTS = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID_AGENTS")