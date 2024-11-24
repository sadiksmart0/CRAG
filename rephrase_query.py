
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Any


def rephrase(question: str, local_llm: Any):
    # Prompt
    system = """You are a question rephraser that converts an input question to a better version that is optimized \n 
     for web search. Look at the input and try to reason about the underlying semantic intent / meaning."""
    re_write_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "Here is the initial question: \n\n {question} \n Formulate an improved question.",
        ),
    ]
    )

    question_rewriter = re_write_prompt | local_llm | StrOutputParser()
    
    return question_rewriter.invoke({"question": question})