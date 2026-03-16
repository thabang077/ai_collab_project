from chat_history import ChatHistory
from metrics import Metrics
from ai_module import ai_agent

history = ChatHistory()
metrics = Metrics()

while True:

    user = input("You: ")

    history.add("user", user)
    metrics.add_message()
    metrics.add_tokens(user)

    response = ai_agent(user)

    print("AI:", response)

    history.add("assistant", response)
    metrics.add_tokens(response)

    if user == "exit":
        break