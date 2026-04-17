# src/graphs/extraction_graph.py
from langgraph.graph import StateGraph, END
from src.models.state import ExtractionState
from src.nodes.extraction_nodes import *

def build_graph():
    g = StateGraph(ExtractionState)

    g.add_node("identify", identify_invoice_page)
    g.add_node("detach", detach_invoice_page)
    g.add_node("extract", extract_invoice_details)
    g.add_node("fallback", fallback_extract)

    g.set_entry_point("identify")

    g.add_edge("identify", "detach")
    g.add_edge("detach", "extract")

    g.add_conditional_edges(
        "extract",
        extraction_router,
        {
            "fallback": "fallback",
            "end": END,
        },
    )

    g.add_edge("fallback", END)

    return g.compile()

extraction_graph = build_graph()