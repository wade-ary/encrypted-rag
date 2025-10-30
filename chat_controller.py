from agentic_function.mistral_agent import MistralAgent
from conversation_memory.memory_manager import ConversationMemory

def chat_loop():
    memory = ConversationMemory()

    while True:
        user_query = input("\nUser: ").strip()
        if user_query.lower() in ["exit", "quit"]:
            print("Chat ended.")
            break

        # Load recent context
        recent_turns = memory.get_last_turns(n=3)

        # Optionally format it for the model
        context = "\n".join(
            [f"User: {t['user_query']}\nAssistant: {t['response']}" for t in recent_turns]
        )

        # Pass context into refinement + summarization
        refined = refine_query(user_query, context=context)
        chunks = retrieve_chunks(refined)
        response = summarize(chunks, context=context)

        print(f"\nAssistant: {response}")

        memory.add_turn(user_query, response)

