import re
from typing import List

from data_ingestion.ingestion_interfaces import TextPreprocessor


class BasicPreprocessor(TextPreprocessor):
    """
    Basic implementation of the TextPreprocessor interface.
    Cleans raw text and splits it into uniform chunks for embedding.
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Args:
            chunk_size (int): Maximum characters per chunk.
            overlap (int): Number of overlapping characters between chunks.
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def clean(self, text: str) -> str:
        """
        Performs light cleaning: removes extra spaces, newlines, and special characters.

        Args:
            text (str): Raw text from loader.

        Returns:
            str: Cleaned text ready for chunking.
        """
        text = re.sub(r'\s+', ' ', text)  # normalize whitespace
        text = text.replace('\x00', '')   # remove null chars
        return text.strip()

    def chunk(self, text: str) -> List[str]:
        """
        Splits text into overlapping chunks for embedding.

        Args:
            text (str): Cleaned text.

        Returns:
            List[str]: List of text chunks.
        """
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += self.chunk_size - self.overlap
        return chunks
