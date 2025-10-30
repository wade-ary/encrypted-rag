from abc import ABC, abstractmethod

class AgentInterface(ABC):
    @abstractmethod
    def refine_query(self, query: str, context) -> str:
        pass

    @abstractmethod
    def summarize(self, retrieved_data: list[dict], context) -> str:
        pass

    @abstractmethod
    def classify_intent(self, query: str) -> str:
        pass
