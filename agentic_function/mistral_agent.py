import ollama
from agentic_function.agentic_interface import AgentInterface

class MistralAgent(AgentInterface):
    def __init__(self, model_name="mistral"):
        self.model = model_name

    def refine_query(self, query: str, context: str = "") -> str:
        prompt = f"""
        You are a retrieval assistant. 
        Refine the user query based on previous conversation context to make it clearer and more specific.
        Keep the user’s intent consistent, but improve clarity and precision for document search.

        Conversation context:
        {context}

        User query:
        {query}

        Return only the refined query, nothing else.
        """
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()

    def summarize(self, retrieved_data: list[dict], context: str = "") -> str:
        retrieved_text = "\n\n".join(chunk["chunk"] for chunk in retrieved_data)

        prompt = f"""
        You are a summarization assistant.
        Use the conversation context and the retrieved text to generate a concise, relevant answer.
        Focus on accuracy and stay aligned with the user’s latest intent.

        Conversation context:
        {context}

        Retrieved text:
        {retrieved_text}

        Return only the final summary, nothing else.
        """
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()

    def classify_intent(self, query: str) -> str:
        prompt = f"Classify this query as 'factual', 'analytical', or 'exploratory':\n\n{query}"
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"].lower().strip()
