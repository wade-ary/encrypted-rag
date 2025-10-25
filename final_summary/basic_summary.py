from typing import Any, Dict, List
from final_summary.summary_interfaces import SummaryInterface
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID"),
    organization=os.getenv("OPENAI_ORG_ID")
)

class BasicSummary(SummaryInterface):
    def __init__(self, model: str = "gpt-4o"):
        self.model = model

    def summarize(self, retrieved_data: List[Dict[str, Any]]) -> str:
        """
        Summarize retrieved chunks into a readable paragraph using an LLM.
        """

        # Combine top retrieved chunks into one block of text
        combined_text = "\n\n".join([item.get("chunk", "") for item in retrieved_data])

        # Build a well-structured summarization prompt
        prompt = f"""
        You are an expert research assistant.

        Below are excerpts from multiple retrieved documents related to a user query.
        Write a clear, concise summary (3–5 sentences) that integrates the main insights,
        findings, or trends across these excerpts. Avoid repetition and use neutral,
        professional language.

        ---
        Retrieved Texts:
        {combined_text}

        ---
        Summary:
        """.strip()

        # Call the OpenAI chat model
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful summarization assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )

        summary = response.choices[0].message.content.strip()
        return summary
