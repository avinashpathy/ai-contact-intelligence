from langgraph.graph import (
    StateGraph
)

from ..agents.planner import planner_agent
from ..agents.retriever import retriever_agent
from ..agents.summarizer import summarizer_agent
from ..models.state import ContactState


graph = StateGraph(
    ContactState
)

graph.add_node(
    "planner",
    planner_agent
)

graph.add_node(
    "retriever",
    retriever_agent
)

graph.add_node(
    "summarizer",
    summarizer_agent
)

graph.set_entry_point(
    "planner"
)

graph.add_edge(
    "planner",
    "retriever"
)

graph.add_edge(
    "retriever",
    "summarizer"
)

workflow = (
    graph.compile()
)