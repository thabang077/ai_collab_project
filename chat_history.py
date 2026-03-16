import json
from datetime import datetime

class ChatHistory:

    def __init__(self):
        self.history = []

    def add(self, role, message):
        self.history.append({
            "role": role,
            "message": message,
            "time": str(datetime.now())
        })

    def get(self):
        return self.history

    def save_json(self, filename="chat_history.json"):
        with open(filename, "w") as f:
            json.dump(self.history, f, indent=4)

    def export_txt(self, filename="chat_history.txt"):
        with open(filename, "w") as f:
            for chat in self.history:
                f.write(f"{chat['role']}: {chat['message']}\n")