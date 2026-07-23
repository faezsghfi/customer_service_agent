
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import uuid



class ParentChildChunker:


    def __init__(
        self,
        parent_chunk_size=1500,
        child_chunk_size=400,
        chunk_overlap=50
    ):

        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=parent_chunk_size,
            chunk_overlap=100
        )


        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=child_chunk_size,
            chunk_overlap=chunk_overlap
        )



    def split_documents(self, documents):

        parents = []

        for doc in documents:

            parent_docs = self.parent_splitter.split_documents(
                [doc]
            )


            for parent in parent_docs:

                parent_id = str(uuid.uuid4())


                parent.metadata["parent_id"] = parent_id


                parents.append(
                    parent
                )



        children = []


        for parent in parents:


            child_docs = self.child_splitter.split_documents(
                [
                    parent
                ]
            )


            for child in child_docs:

                child.metadata["parent_id"] = (
                    parent.metadata["parent_id"]
                )


                child.metadata["chunk_id"] = str(
                    uuid.uuid4()
                )


                children.append(
                    child
                )


        return parents, children
