from langchain_ollama import OllamaEmbeddings
from langchain_community.graph_vectorstores.extractors import KeybertLinkExtractor
from langchain_community.graph_vectorstores.links import add_links
from langchain_community.graph_vectorstores import CassandraGraphVectorStore
import tqdm


# Local Embedding 
embedding = OllamaEmbeddings(model="mistral:instruct")

# link documents 
#extractor = KeybertLinkExtractor()
# for chunk in tqdm(chunks):
#     add_links(chunk, extractor.extract_one(chunk))
# print(f"<----{len(chunks)} Documents Link Completed---->")

def embed_and_store(chunks: list, keyspace: str, table_name: str, db_check: bool):
    vector_store = None
    
    if not db_check:
        print("--------Embedding and Storing To DB ---------------")
        vector_store = CassandraGraphVectorStore.from_documents(
            embedding=embedding,
            documents=chunks,
            keyspace=keyspace,
            table_name=table_name
            )
        
    return vector_store
            

def retrieve_docs_from_db(question: str, session) -> list:
    print("-------- Fetching Similar Dcocument from DB ---------------")
    vector_store = CassandraGraphVectorStore(
            embedding=embedding,
            session=session,
            keyspace="rag_project",
            table_name="document_table")
    
    docs = vector_store.similarity_search(
        query=question,
        K=5,
        )
    
    return docs





# retriever = vector_store.as_retriever(
#         search_type="similarity",
#         search_kwargs={"k":5}
#     )








        