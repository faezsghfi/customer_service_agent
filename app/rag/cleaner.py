

def clean_documents(documents):

    cleaned = []

    for doc in documents:

        text = doc.page_content

        text = text.replace(
            "\n\n\n",
            "\n"
        )

        text = text.strip()


        doc.page_content = text

        cleaned.append(doc)


    return cleaned
