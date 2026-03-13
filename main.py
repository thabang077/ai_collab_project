from ai_module import ask_ai
 
def main():
    print("Welcome to AI4Free CLI! Type 'exit' to quit.")
    while True:
        question = input("You: ")
        if question.lower() == "exit":
            break
        answer = ask_ai(question)
        print("AI:", answer)
 
if __name__ == "__main__":
    main()