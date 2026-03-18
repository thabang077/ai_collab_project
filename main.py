import json
from datetime import datetime

class ChatHistory:
    def __init__(self):
        self.history = []
        self.total_messages = 0

    def add(self, role, content):
        message = {
            "role": role,
            "content": content,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(message)
        self.total_messages += 1

    def show(self):
        if not self.history:
            print("No chat history.\n")
            return
        
        print("\n--- Chat History ---")
        for msg in self.history:
            print(f"[{msg['time']}] {msg['role'].upper()}: {msg['content']}")
        print()

    def save_txt(self, filename="chat_history.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for msg in self.history:
                f.write(f"[{msg['time']}] {msg['role']}: {msg['content']}\n")
        print(f"Saved to {filename}\n")

    def save_json(self, filename="chat_history.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4)
        print(f"Saved to {filename}\n")

    def metrics(self):
        user_msgs = len([m for m in self.history if m["role"] == "user"])
        ai_msgs   = len([m for m in self.history if m["role"] == "ai"])

        print("\n--- Metrics ---")
        print(f"Total messages: {self.total_messages}")
        print(f"User messages : {user_msgs}")
        print(f"AI messages   : {ai_msgs}\n")

    def clear(self):
        self.history = []
        self.total_messages = 0
        print("Chat history cleared.\n")


# ✅ Simple AI response function (you can replace with API later)
def ai_response(user_input):
    return f"AI Response: You said '{user_input}'"


if __name__ == "__main__":
    chat = ChatHistory()
    
    while True:
        user_input = input("Enter command: ").strip()

        if user_input.lower() == "exit":
            print("Exiting...")
            break

        elif user_input.lower() == "history":
            chat.show()

        elif user_input.lower() == "save txt":
            chat.save_txt()

        elif user_input.lower() == "save json":
            chat.save_json()

        elif user_input.lower() == "metrics":
            chat.metrics()

        elif user_input.lower() == "clearhistory":
            chat.clear()
        elif user_input.lower() == "help":
                    print("""
        Available commands:
        - history : Show chat history
        - metrics : Show usage stats
        - save txt : Save chat to TXT
        - save json : Save chat to JSON
        - exit    : Exit program
        """)

        else:
            # ✅ Add user message
            chat.add("user", user_input)

            # ✅ Generate AI response
            response = ai_response(user_input)

            # ✅ Add AI message
            chat.add("ai", response)

            # ✅ PRINT OUTPUT (important)
            print(response)