import ollama
from agentic_workflow.agentic_interface import AgentInterface

class MistralAgent(AgentInterface):
    def __init__(self, model_name="mistral"):
        self.model = model_name

    def refine_query(self, query: str) -> str:
        prompt = f"Refine this query for document retrieval:\n\n{query}"
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

    def summarize(self, retrieved_data: list[dict]) -> str:
        context = "\n\n".join([chunk["chunk"] for chunk in retrieved_data])
        prompt = f"Summarize the following context:\n\n{context}"
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

    def classify_intent(self, query: str) -> str:
        prompt = f"Classify this query as 'factual', 'analytical', or 'exploratory':\n\n{query}"
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"].lower().strip()
