

from app.models.llm import get_llm

from app.rag.loader import load_documents
from app.rag.cleaner import clean_documents
from app.rag.chunker import chunk_documents
from app.rag.embeddings import get_embedding_model

from app.rag.vectorstore import create_vectorstore
from app.rag.bm25 import create_bm25_retriever

from app.rag.hybrid import reciprocal_rank_fusion
from app.rag.reranker import rerank
from app.rag.guardrail import validate_context

from app.rag.prompt import RAG_PROMPT



_vectorstore = None
_bm25 = None



def initialize_rag():
    """
    Initialize RAG components once.
    """


    global _vectorstore
    global _bm25


    if _vectorstore is not None:
        return


    docs = load_documents(
        "data/knowledge_base.pdf"
    )


    cleaned_docs = clean_documents(
        docs
    )


    chunks = chunk_documents(
    cleaned_docs
)


    embedding_model = get_embedding_model()


    _vectorstore = create_vectorstore(
        chunks,
        embedding_model
    )


    _bm25 = create_bm25_retriever(
        chunks
    )



def run_rag(query):

    """
    Complete RAG pipeline.
    """


    initialize_rag()


    dense_results = _vectorstore.similarity_search(
        query,
        k=5
    )


    sparse_results = _bm25.invoke(
        query
    )


    hybrid_results = reciprocal_rank_fusion(
        dense_results,
        sparse_results
    )


    ranked_results = rerank(
        query,
        hybrid_results,
        top_k=3
    )


    validation = validate_context(
        ranked_results
    )


    if not validation["allowed"]:

        return (
            "اطلاعات کافی در پایگاه دانش موجود نیست."
        )


    context = "\n\n".join(
        validation["context"]
    )


    prompt = RAG_PROMPT.format(
        context=context,
        question=query
    )


    llm = get_llm()


    response = llm.invoke(
        prompt
    )


    return response.content
