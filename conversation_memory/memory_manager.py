import json
from datetime import datetime
from pathlib import Path

class ConversationMemory:
    def __init__(self, path="conversation_memory/conversation.json"):
        self.path = Path(path)
        if not self.path.exists():
            self._save({"conversation": []})

    def _load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def add_turn(self, user_query, response):
        data = self._load()
        turn = {
            "turn_id": len(data["conversation"]) + 1,
            "user_query": user_query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        data["conversation"].append(turn)
        self._save(data)

    def get_last_turns(self, n=3):
        return self._load()["conversation"][-n:]