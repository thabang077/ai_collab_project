from ai_module import ask_ai

def main():
    print("AI CLI Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            continue  

        print("AI is thinking...\n")

        response = ask_ai(user_input)

        print("🤖 AI:", response)
        print()

if __name__ == "__main__":
    main()