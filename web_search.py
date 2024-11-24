
from langchain_community.tools.tavily_search import TavilySearchResults



def web_search(question):
    search_engine = TavilySearchResults(
    max_results=4,
    search_depth="advanced")

    return search_engine.invoke(question)