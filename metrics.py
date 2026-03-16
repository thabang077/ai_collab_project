class Metrics:

    def __init__(self):
        self.messages = 0
        self.tokens = 0

    def add_message(self):
        self.messages += 1

    def add_tokens(self, text):
        self.tokens += len(text.split())

    def report(self):
        return {
            "messages": self.messages,
            "tokens": self.tokens
        }