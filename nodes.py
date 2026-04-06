"""
nodes.py — All LangGraph node functions and routing logic.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from tavily import TavilyClient

from config import model
from cache import get_cache, set_cache
from States import AgnentState, Research_Questions, Evaluate_research
from Prompts import create_question_prompt, create_research_document_prompt, evaluate_research_prompt


# Check Cache 
def check_cache(state: AgnentState):
    query = state["user_query"]

    print("Checking Cache query :", query)
    cached = get_cache(query)

    print("=" * 50, "CACHE RESULT", "=" * 50)
    print(cached)

    if cached:
        return {
            "research_chunk": cached["research_chunk"],
            "cache_hit": True,
        }

    return {"cache_hit": False}


# Cache Router
def cache_router(state: AgnentState):
    if state.get("cache_hit"):
        return "create_doc"
    return "create_questions"


# Create Research Questions 
def create_questions(state: AgnentState):
    """Creates focused research questions from the user's topic."""

    prompt = [
        SystemMessage(content=create_question_prompt),
        HumanMessage(content=state["user_query"]),
    ]

    question_generator = model.with_structured_output(Research_Questions)
    print("=" * 50, "QUESTIONS", "=" * 50, flush=True)
    result = question_generator.invoke(prompt)
    print(result.questions)  # type: ignore

    return {
        "research_question": result.questions,  # type: ignore
        "retry_question": state.get("retry_question", 0) + 1,
        "retry_document": state.get("retry_document", 0),
    }


# Tavily Research 
def tavily_research(state: AgnentState):
    """Scrapes the web using Tavily for each research question."""

    tavily = TavilyClient()
    research_chunk = []

    print("\n\n", "=" * 50, "RESEARCH CHUNK", "=" * 50)
    print("Fetching results from web...")

    for question in state["research_question"]:
        result = tavily.search(
            query=question,
            search_depth="advanced",
            max_results=1,
            include_answer=False,
            include_raw_content=True,
        )
        for i, item in enumerate(result.get("results", [])):
            if item.get("content"):
                # Truncate content to 5000 characters to save tokens
                truncated_content = item['content'][:5000]
                research_chunk.append(
                    f"SOURCE {i}: {item['url']}\n"
                    f"TITLE: {item['title']}\n"
                    f"CONTENT: \n{truncated_content}"
                )
                print(
                    f"SOURCE: {item['url']}\n"
                    f"TITLE:  {item['title']}\n"
                    f"CONTENT (preview): {truncated_content[:100]}.....\n"
                )

    set_cache(
        query=state["user_query"],  # type: ignore
        value={"research_chunk": research_chunk},
    )

    return {"research_chunk": research_chunk}


# Create Document
def create_doc(state: AgnentState):
    """Streams a research document from the collected research chunks."""

    print("Creating research document...")
    prompt = [
        SystemMessage(content=create_research_document_prompt),
        HumanMessage(content="\n\n---\n\n".join(state["research_chunk"])),
    ]

    print("=" * 50, "RESEARCH DOCUMENT", "=" * 50)
    generated_doc = ""
    for chunk in model.stream(prompt):
        if chunk.content:
            generated_doc += chunk.content  # type: ignore
            yield {"final_doc": chunk.content}  # stream individual tokens

    # Final yield: full document + increment retry counter
    yield {
        "final_doc": generated_doc,
        "retry_document": state.get("retry_document", 0) + 1,
    }


# Evaluate Reasearch
def evaluate_research(state: AgnentState):
    """Evaluates the research document quality using structured LLM output."""

    print("\n\n" + "=" * 50, "EVALUATION", "=" * 50)
    print("Evaluating research document...")

    prompt = [
        SystemMessage(content=evaluate_research_prompt),
        HumanMessage(content=f"""
            TOPIC :
            {state["user_query"]}

            RESEARCH DOCUMENT:
            {state["final_doc"]}
        """),
    ]

    evaluation_model = model.with_structured_output(Evaluate_research)

    try:
        result = evaluation_model.invoke(prompt)

        # Compute overall_score 
        overall_score = round(0.5 * result.relevance_score + 0.5 * result.coverage_score, 2)

        print(f"Relevance Score  : {result.relevance_score}")
        print(f"Coverage Score   : {result.coverage_score}")
        print(f"Overall Score    : {overall_score}")
        print(f"Improvement Type : {result.improvement_type}")  
        print(f"Suggestion       : {result.improvement_suggestion}")

        return {
            "overall_score": overall_score,
            "improvement_type": result.improvement_type, 
            "improvement_suggestion": result.improvement_suggestion, 
        }

    except Exception as e:
        print(f"Error during evaluation: {e}")
        return {
            "overall_score": 0.0,
            "improvement_type": "no_improvement",
            "improvement_suggestion": str(e),
        }


# Router
def router(state: AgnentState):
    improvement_type = state.get("improvement_type", "no_improvement")
    overall_score    = state.get("overall_score", 0)

    if improvement_type == "no_improvement" or overall_score >= 0.7:
        return "end"

    if state.get("retry_question", 0) >= 3 or state.get("retry_document", 0) >= 3:
        return "end"

    if improvement_type == "rewrite_questions":
        return "rewrite_questions"

    if improvement_type == "rewrite_document":
        return "regenerate_doc"

    return "end"
