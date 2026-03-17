import requests

def ai_agent(question):
    url = "https://api.chucknorris.io/jokes/random"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return data["value"]
        else:
            return "AI service unavailable"

    except Exception as e:
        return "Error connecting to AI service"