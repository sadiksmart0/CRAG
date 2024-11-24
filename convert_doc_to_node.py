
from llama_index.core.schema import TextNode



def convert_doc_to_textnodes(retrieved: list) -> list:
    nodes = []
    for i, chunk in enumerate(retrieved):
        nodes.append(
            TextNode(
                text=chunk,
                #metadata=chunk.metadata,  # Preserve metadata from Document
                id_=str(i)  # Assign a unique ID for each node
            )
        )
    return nodes