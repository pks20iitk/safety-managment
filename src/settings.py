import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from azure.identity import ClientSecretCredential
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class AppSettings(BaseSettings):
    download_dir: str = str(BASE_DIR / "data")

    service_bus_host: str = "np-safetyrules-sbus.servicebus.windows.net"
    service_bus_topic_name: str = "np-safety-rules-topic"
    service_bus_subscription_name: str = "np-safety-rules-sb-subscription"

    tenant_id: str = os.getenv("AZURE_TENANT_ID")
    client_id: str = os.getenv("AZURE_CLIENT_ID")
    client_secret: str = os.getenv("AZURE_CLIENT_SECRET")
    container_name: str = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
    storage_account_name: str = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")

    credential: ClientSecretCredential = ClientSecretCredential(
        tenant_id=os.getenv("AZURE_TENANT_ID"),
        client_id=os.getenv("AZURE_CLIENT_ID"),
        client_secret=os.getenv("AZURE_CLIENT_SECRET"),
    )

    azure_openai_endpoint: str = "https://investment-tracker.openai.azure.com/"
    azure_search_endpoint: str = "https://investmenttracker.search.windows.net"

    azure_search_index_name: str = "safetydocs_rules"

    embedding_model: str = "text-embedding-3-large"
    embedding_dimension: int = 3072

    chat_model: str = "gpt4-o"


app_settings = AppSettings()

openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=app_settings.azure_openai_endpoint,
)
index_client = SearchIndexClient(
    endpoint=app_settings.azure_search_endpoint,
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY")),
)

search_client = SearchClient(
    endpoint=app_settings.azure_search_endpoint,
    index_name=app_settings.azure_search_index_name,
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"]),
)
