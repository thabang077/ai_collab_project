from ai4free import YouChat
 
def ask_ai(question):
    ai = YouChat()
    response = ai.ask(question)
    return ai.get_message(response)