"""
graph.py — Assembles and compiles the LangGraph research agent.
Import `app` from this module in Frontend.py or Research_agent.py.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from States import AgnentState
from nodes import (
    check_cache,
    cache_router,
    create_questions,
    tavily_research,
    create_doc,
    evaluate_research,
    router,
)


graph = StateGraph(AgnentState)

graph.add_node("check_cache", check_cache)
graph.add_node("create_questions", create_questions)
graph.add_node("tavily", tavily_research)
graph.add_node("create_doc", create_doc)
graph.add_node("evaluate_research", evaluate_research)


graph.add_edge(START, "check_cache")

graph.add_conditional_edges(
    "check_cache",
    cache_router,
    {
        "create_doc": "create_doc",
        "create_questions": "create_questions",
    },
)

graph.add_edge("create_questions", "tavily")
graph.add_edge("tavily", "create_doc")
graph.add_edge("create_doc", "evaluate_research")

graph.add_conditional_edges(
    "evaluate_research",
    router,
    {
        "rewrite_questions": "create_questions",
        "regenerate_doc": "create_doc",
        "end": END,
    },
)


checkpointer = InMemorySaver()
app = graph.compile(checkpointer=checkpointer)
