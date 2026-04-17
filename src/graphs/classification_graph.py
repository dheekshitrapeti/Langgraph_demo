
from langgraph.graph import StateGraph, END
from src.nodes.classification_nodes import extract_text, classify_document


def build_classification_graph():
    g = StateGraph(dict)

    g.add_node("extract_text", extract_text)
    g.add_node("classify", classify_document)

    g.set_entry_point("extract_text")

    g.add_edge("extract_text", "classify")
    g.add_edge("classify", END)

    return g.compile()


classification_graph = build_classification_graph()