
from langchain_community.document_loaders import PyPDFLoader


def load_documents(path):

    loader = PyPDFLoader(path)

    documents = loader.load()

    return documents
