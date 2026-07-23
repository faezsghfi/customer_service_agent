
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


def get_embedding_model():

    model_name = "BAAI/bge-m3"


    model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )


    return model
