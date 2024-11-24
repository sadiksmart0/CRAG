from langchain_text_splitters import CharacterTextSplitter


def split_document(docs: list) -> list:
    text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=80,
    length_function=len
    )

    return text_splitter.split_documents(docs)