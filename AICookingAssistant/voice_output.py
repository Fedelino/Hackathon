import requests


def ask_llm(prompt):
    response = requests.post(
        "https://api.together.xyz/inference",
        headers={
            "Authorization": f"Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.6,
        }
    )
    return response.json()["output"]["choices"][0]["text"].strip()
