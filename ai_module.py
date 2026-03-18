from g4f.client import Client
<<<<<<< HEAD
 
def ask_ai(question, model_name="gpt-4"):
    client = Client()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": question}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: AI connection failed: {e}"
=======
 
def ask_ai(question, model_name="gpt-4"):
    client = Client()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": question}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: AI connection failed: {e}"
 
>>>>>>> ab0bbf9e552ced1ecd03e46d550ecb3fbab7b9e2
