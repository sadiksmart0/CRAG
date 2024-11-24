from typing import List
from typing_extensions import TypedDict
from pprint import pprint

from langgraph.graph import END, StateGraph, START
from langchain_ollama import OllamaLLM
from llama_index.core.node_parser import SentenceSplitter

from load_data import load_document
from split_text import split_document
from grader import grader
from retrieve_and_generate import retrieve_and_generate
from embed import embed_and_store, retrieve_docs_from_db
from rephrase_query import rephrase
from db_setup import create_keyspace
from convert_doc_to_node import convert_doc_to_textnodes
from web_search import web_search

from pydantic import BaseModel, Field
from langchain.schema import Document
from langchain_openai import ChatOpenAI

import getpass
import os


def _set_env(key: str):
    if key not in os.environ:
        os.environ[key] = getpass.getpass(f"ENTER YOUR {key}:")


_set_env("TAVILY_API_KEY")
_set_env("MISTRAL_API_KEY")
_set_env("LANGCHAIN_API_KEY")
_set_env("LANGCHAIN_ENDPOINT")


# export MISTRAL_API_KEY="MISTRAL_API_KEY" #To access local llm
# export TAVILY_API_KEY="TAVILY_API_KEY"   #To Search the web
# export LANGCHAIN_TRACING_V2=true         #Set up LangSmith Tracing
# export LANGCHAIN_API_KEY="LANGCHAIN_API_KEY" #Explore langchain
# export LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

FILE_PATH="/Users/abubakarmuktar/Documents/RAG_Projects/CRAG/Data/CRAG.pdf"
KEY_SPACE="rag_project"



local_llm = OllamaLLM(
    model="mistral:instruct",
    temperature=0.7
)


class GraphState(TypedDict):
    question: str
    generation: str
    web_search: str
    documents: List[str]



#-------------------------------- GRAPH NODES   -----------------------------------------#

# retrieve docs related to query
def retrieve(state):
    print("<----------------------RETRIEVE----------------------------->")
    question = state["question"]
    documents = [doc.page_content for doc in docs]
    
    return {"documents": documents, "question": question}


# generate response/answer
def generate(state):
    print("<----------------------GENERATE----------------------------->")
    question = state["question"]
    documents = [doc.page_content for doc in docs]
    generation = retrieve_and_generate(question=question, context=documents, local_llm=local_llm)

    return {"documents": documents, "question": question, "generation": generation}


# grade retrieved chunks for relevance
def grade_documents(state):
    print("<----------------------GRADE DOCUMENT----------------------------->")
    question = state["question"]
    documents = [doc.page_content for doc in docs]

    relevant_docs, irrelevant_docs = [], []
    web_search = "No"

    for doc in documents:
        score = grader(question=question, doc=doc, llm=local_llm).strip().lower()
        if score == "no":
            print(score)
            print("<---Comment: Document is not Relevant------>")
            irrelevant_docs.append(doc)
        else:
            print(score)
            print("<---Comment: Document is Relevant---------->")
            relevant_docs.append(doc)

    web_search = "Yes" if not relevant_docs else "No" # Set web_search to "Yes" if no relevant documents

    print(f"{len(relevant_docs)} RELEVANT DOCS \n{len(irrelevant_docs)} IRRELEVANT DOCS")
    
    return {"documents": relevant_docs, "question": question, "web_search": web_search}


# Refining to remove noise from relevant docs
def refine_knowledge(state):
    question = state["question"]
    document = state["documents"]
    print("<-------------REFINING KNOWLEDGE----------->")
    nodes = convert_doc_to_textnodes(document)
    splitter = SentenceSplitter(
    chunk_size=200,
    chunk_overlap=15,
    )
    refined_strips = splitter.get_nodes_from_documents(nodes)
    
    return {"documents": refined_strips, "question": question}


# Agent Rephrase question/query
def rephrase_query(state):
    print("<--------------------REPHRASING QUERY------------------------------->")
    question = state["question"]
    documents = state["documents"]
    rephrased_question = rephrase(question, local_llm=local_llm) # Rephrase question

    return {"documents": documents, "question": rephrased_question}
    

# Search the web
def search_web(state):
    print("<----------------------SEARCHING THE WEB----------------------------->")
    question = state["question"]
    documents = state["documents"]
    docs = web_search({"query": question}) 
    search_result = "\n".join([doc["content"] for doc in docs])
    search_result = Document(page_content=search_result)
    documents.append(search_result)
    
    return {"documents": documents, "question": question}


# No relevant doc, We will rephrase then re-generate.
# We have relevant documents, refine them to remove noise
def decide_to_generate(state):
    print("<----------------------GENERATION DECISION-------------------------->")
    question = state["question"]
    web_search = state["web_search"]
    document = state["documents"]
    
    if web_search == "Yes":
        print("\n---REPHRASING QUESTION FOR WEB SEARCH---\n") 
        return "rephrase_query"
    else:
        print("\n---REFINING RELEVANT DOCUMENT TO REMOVE NOISE---\n")
        return "refine_knowledge"
    


#-------------------------------- MAIN  -----------------------------------------#

from cassandra.cluster import Cluster


cluster = Cluster(["127.0.0.1"])
session = cluster.connect()



question = "Who wrote or authored this Corrective Retrieval Augmented Generation paper ?"

exist = create_keyspace(KEY_SPACE, session)
docs = load_document(FILE_PATH=FILE_PATH)
chunks = split_document(docs=docs)

if not exist:
    embed_and_store(chunks=chunks,
                    keyspace=KEY_SPACE,
                    )

docs = retrieve_docs_from_db(question=question, session=session)

# web_search_tool = web_search
workflow = StateGraph(GraphState)




# NODE DEFINITION
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("rephrase_query", rephrase_query)
workflow.add_node("search_web", search_web)
workflow.add_node("refine_knowledge", refine_knowledge)


# BUILD GRAPH

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents", 
    decide_to_generate,
    {
     "rephrase_query": "rephrase_query",
     "refine_knowledge": "refine_knowledge",
    },
    )
workflow.add_edge("refine_knowledge", "generate")
workflow.add_edge("rephrase_query", "search_web")
workflow.add_edge("search_web", "generate")
workflow.add_edge("generate", END)

# COMPILE APP
app = workflow.compile()


#-------------------------------- GRAPH WORKFLOW  -----------------------------------------#

# Run
inputs = {
    "question": question,
    "documents": [],  # Initialize as an empty list or provide relevant documents
    "web_search": "No",  # Default value
    "generation": None  # Default value
}
for output in app.stream(inputs):
    for key, value in output.items():
        pprint(f"Node '{key}':")
    pprint("\n------------------\n")

# Final generation
pprint(value["generation"])