import os
from openai import AzureOpenAI
from dotenv import load_dotenv

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_VERSION,
    EMBEDDING_MODEL_NAME,
    LLM_NAME,
)

load_dotenv()

AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)


def get_llm_response(message):
    completion = client.chat.completions.create(
        model=LLM_NAME, messages=message, max_tokens=3000, temperature=0
    )
    response = completion.choices[0].message.content.strip()
    print(response)
    return response


def get_embeddings(text, model=EMBEDDING_MODEL_NAME):
    return client.embeddings.create(input=text, model=model).data[0].embedding