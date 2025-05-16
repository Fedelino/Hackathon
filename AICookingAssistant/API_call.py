import requests


def ask_llm(user_input):
    system_prompt = (
        "You are a helpful and concise cooking assistant. "
        "Respond with **only one short, clear instruction at a time**. "
        "Wait for the user to ask for the next step before continuing."
    )

    full_prompt = f"{system_prompt}\nUser: {user_input}\nAssistant:"

    response = requests.post(
        "https://api.together.xyz/inference",
        headers={
            "Authorization": f"Bearer YOUR_API_KEY",  # Replace with your actual key
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  # or another instruction-tuned model
            "prompt": full_prompt,
            "max_tokens": 200,
            "temperature": 0.6,
        }
    )

    return response.json()["output"]["choices"][0]["text"].strip()
