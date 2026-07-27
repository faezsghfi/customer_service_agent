
from app.models.llm import get_llm

from app.rag.loader import load_documents
from app.rag.cleaner import clean_documents
from app.rag.chunker import (
    chunk_documents,
    get_parent_context
)

from app.rag.embeddings import get_embedding_model
from app.rag.vectorstore import create_vectorstore
from app.rag.bm25 import create_bm25_retriever

from app.rag.hybrid import reciprocal_rank_fusion
from app.rag.reranker import rerank
from app.rag.guardrail import validate_context
from app.rag.prompt import RAG_PROMPT
from app.core.logger import (
    section,
    thought,
    action,
    observation,
    success,
    error,
)


_vectorstore = None
_bm25 = None



def initialize_rag():

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


    children = chunk_documents(
        cleaned_docs
    )


    embedding_model = get_embedding_model()


    _vectorstore = create_vectorstore(
        children,
        embedding_model
    )


    _bm25 = create_bm25_retriever(
        children
    )



def run_rag(query):


    initialize_rag()

    section("RAG PIPELINE")
    thought("Searching knowledge base")
    observation(f"Question: {query}")

    action("Dense Retrieval")
    dense_results = _vectorstore.similarity_search(query,k=5)
    observation(f"Dense documents: {len(dense_results)}")

    action("Sparse Retrieval (BM25)")
    sparse_results = _bm25.invoke(query)
    observation(f"Sparse documents: {len(sparse_results)}")

    action("Hybrid Fusion")
    hybrid_results = reciprocal_rank_fusion(dense_results,sparse_results)
    observation(f"Hybrid documents: {len(hybrid_results)}")

    action("Reranking")
    ranked_results = rerank(query,hybrid_results,top_k=3)
    observation(f"Top documents: {len(ranked_results)}")

    action("Building Context")
    parent_ids = []
    child_context = []


    for item in ranked_results:


        if isinstance(item, dict):

            doc = item["document"]

        else:

            doc = item


        parent_id = doc.metadata.get(
            "parent_id"
        )


        if parent_id:

            parent_ids.append(
                parent_id
            )

        else:

            child_context.append(
                doc.page_content
            )



    if parent_ids:

        context = get_parent_context(
            parent_ids
        )

    else:

        context = child_context

    observation(f"Context chunks: {len(context)}")


    action("Input Guardrail")
    validation = validate_context(
        context
    )

  
    # --------------------------
    # Support different guardrail outputs
    # --------------------------

    if isinstance(validation, dict):

        if not validation.get("allowed", False):

            error("Context rejected")

            return {
                "answer": "اطلاعات کافی در پایگاه دانش موجود نیست.",
                "context": []
            }

        success("Context accepted")
        final_context = context

    else:

        # guardrail returned string

        final_context = validation



    messages = RAG_PROMPT.format_messages(context=final_context,question=query)

    action("Generating Answer")
    llm = get_llm()

    response = llm.invoke(messages)
    success("Answer generated")

    success("RAG Pipeline Finished")
    return {
        "answer": response.content,
        "context": context
    }
