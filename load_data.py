from langchain_community.document_loaders import PyPDFLoader


def load_document(FILE_PATH: str) -> list:
    loader = PyPDFLoader(
        file_path=FILE_PATH,
        extract_images=True
    )
    
    return loader.load()