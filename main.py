"""
Research_agent.py — Terminal entry point for the research agent.
Run:  py Research_agent.py

For the Streamlit UI, run:  streamlit run Frontend.py
"""

from graph import app


if __name__ == "__main__":

    query = input("Enter research query: ").strip()
    if not query:
        query = "Best coffee shops in India"

    config = {"configurable": {"thread_id": "user-session-1"}}
    initial_state = {"user_query": query}

    print("\n" + "=" * 50 + " STREAMING DOCUMENT " + "=" * 50)


    for message_chunk, metadata in app.stream(
        initial_state,
        config=config,
        stream_mode="messages",
    ):
        if message_chunk.content:
            print(message_chunk.content, end="", flush=True)

    
    print("\n\n" + "=" * 50 + " FINAL STATE " + "=" * 50)
    final_state = app.get_state(config).values
    print("Overall Score    :", final_state.get("overall_score"))
    print("Improvement Type :", final_state.get("improvement_type"))
    suggestion = final_state.get("improvement_suggestion")
    if suggestion:
        print("Suggestion       :", suggestion)