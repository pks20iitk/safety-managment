from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    HnswParameters,
    VectorSearchAlgorithmKind,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SemanticSearch,
    SearchFieldDataType,
)


from preprocessors import rules, embed
from settings import app_settings, index_client, search_client
from utils import load_json


class AzureSearchManager:
    def __init__(self) -> None:
        self.create_index(app_settings.azure_search_index_name)

    def create_index(self, index_name: str):
        fields = [
            SimpleField(
                name="Id",
                type="Edm.String",
                key=True,
                sortable=True,
                filterable=True,
                facetable=True,
            ),
            SearchableField(
                name="Book",
                type="Edm.String",
                filterable=True,
                searchable=True,
                facetable=True,
            ),
            SearchableField(name="Chapter", type="Edm.String", filterable=True, searchable=True),
            SearchableField(name="Section", type="Edm.String", filterable=True, searchable=True),
            SearchableField(
                name="Chunk_Content_w_Metadata", type="Edm.String", filterable=True, searchable=True
            ),
            SearchableField(
                name="Embedding",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                filterable=True,
                searchable=True,
                vector_search_dimensions=app_settings.embedding_dimension,
                vector_search_profile_name="myHnswProfile",
            ),
        ]

        vector_search = VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="myHnsw",
                    kind=VectorSearchAlgorithmKind.HNSW,
                    parameters=HnswParameters(m=4, ef_construction=400, ef_search=500),
                )
            ]
        )

        semantic_config = SemanticConfiguration(
            name="my-semantic-config",
            prioritized_fields=SemanticPrioritizedFields(
                content_fields=[SemanticField(field_name="section")],
                keywords_fields=[SemanticField(field_name="chunk_content")],
            ),
        )

        index = SearchIndex(
            name=index_name,
            fields=fields,
            vector_search=vector_search,
            semantic_search=SemanticSearch(configurations=[semantic_config]),
        )
        result = index_client.create_or_update_index(index)
        print(f"Azure Search Index '{result.name}' created.")

    def upload_documents(self, index_name: str, documents: list):
        for i in range(0, len(documents), 200):
            batch = documents[i : i + 200]
            search_client.upload_documents(batch)
            print(f"Uploaded batch of {len(batch)} documents to index '{index_name}'.")
    
if __name__ == "__main__":
    paragraphs = load_json(r"C:\Users\I8924\projects\os_safety-ai-rules\data\analysis_result.json")["analyze_result"]["paragraphs"]
    chunks = rules.pdf_processor.create_rule_book_chunks("Operating Rules", paragraphs)
    chunks = embed.embed_chunks(chunks)
    azure_search = AzureSearchManager()
    azure_search.upload_documents(app_settings.azure_search_index_name, chunks)

