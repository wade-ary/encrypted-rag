from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SummaryInterface(ABC):
    @abstractmethod
    def summarize(self, retrieved_data: List[Dict[str, Any]]) -> str:
        """
        Generate a readable summary from retrieved chunks and metadata.

        Args:
            retrieved_data (List[Dict[str, Any]]): 
                List of dictionaries containing 'chunk', 'score', 'doc_id', and other metadata.

        Returns:
            str: A human-readable summary synthesized from the top retrieved chunks.
        """
        pass