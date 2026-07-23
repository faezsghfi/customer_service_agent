

from langchain_qdrant import QdrantVectorStore


def create_vectorstore(
    chunks,
    embedding_model
):


    vectorstore = QdrantVectorStore.from_documents(

        documents=chunks,

        embedding=embedding_model,

        location=":memory:",

        collection_name="customer_support"

    )


    return vectorstore
