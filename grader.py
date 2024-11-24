from langchain_core.prompts import ChatPromptTemplate
from typing import Any
from langchain_core.documents.base import Document
from langchain_core.runnables.base import RunnableSequence


def grader(question: str, doc: Document, llm: Any) -> str:
    
    system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
    No further explanation Please just 'yes' or 'no'.
    """
    grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
    )
    grader_chain = grade_prompt | llm
    doc_ = doc
    return grader_chain.invoke({"question": question, "document": doc_})