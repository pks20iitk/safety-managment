from settings import app_settings, openai_client


def get_embeddings(text: str):
    embedding = (
        openai_client.embeddings.create(
            input=text, model=app_settings.embedding_model
        )
        .data[0]
        .embedding
    )
    return embedding


def embed_chunks(documents: list):
    chunks = []
    for i, item in enumerate(documents):
        chunks.append(
            {
                "Id": str(i),
                "Book": item["Book"],
                "Chapter": item["Chapter"],
                "Section": item["Section"],
                "Chunk_Content": item["Chunk_Content"],
                "Chunk_Content_w_Metadata": item["Chunk_Content_w_Metadata"],
                "Pages": item["Pages"],
                "Embedding": get_embeddings(item["Chunk_Content_w_Metadata"]),
            }
        )

    print(f"Processed {len(chunks)} items for embeddings.")
    return chunks
