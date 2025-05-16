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
            "Authorization": "tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8",
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


user_input = "Start making spaghetti carbonara"
response = ask_llm(user_input)
print(response)
