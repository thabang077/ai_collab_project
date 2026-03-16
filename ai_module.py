import requests

def ai_agent(question):
    url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["value"]
    else:
        return "AI service unavailable"