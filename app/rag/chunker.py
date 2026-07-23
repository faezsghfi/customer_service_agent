
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import uuid



_parent_store = {}



def chunk_documents(documents):


    parent_splitter = RecursiveCharacterTextSplitter(

        chunk_size=1500,

        chunk_overlap=200,

        separators=[
            "\n\n",
            "\n",
            "##",
            "#",
            " "
        ]

    )


    child_splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=100,

        separators=[
            "\n\n",
            "\n",
            "##",
            "#",
            " "
        ]

    )


    parents = parent_splitter.split_documents(
        documents
    )


    children = []


    for parent in parents:


        parent_id = str(uuid.uuid4())


        parent.metadata["parent_id"] = parent_id


        # ذخیره Parent
        _parent_store[parent_id] = parent.page_content



        child_chunks = child_splitter.split_documents(
            [
                parent
            ]
        )


        for child in child_chunks:


            child.metadata["parent_id"] = parent_id


            children.append(child)



    return children



def get_parent_context(parent_ids):


    results = []


    for pid in parent_ids:


        if pid in _parent_store:

            results.append(
                _parent_store[pid]
            )


    return results
