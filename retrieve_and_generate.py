from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.graph_vectorstores.base import GraphVectorStoreRetriever


def retrieve_and_generate(question: str, context: list, local_llm):
    context_string = "\n".join(context)
    prompt = ChatPromptTemplate.from_template("""You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context: {context} to answer the question: {question}. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise."""
    )

    rag_chain = (
        # {"context": context_string, "question": RunnablePassthrough()}
        prompt
        | local_llm
        | StrOutputParser()
        )
    
    return rag_chain.invoke({
        "context": context_string,
        "question": question
    })