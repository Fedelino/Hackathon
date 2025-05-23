from together import Together

client = Together(api_key="tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8")

messages = [
    {"role": "system",
     "content": "You are a helpful cooking assistant. The user will either give the name of a recipe or ingredients "
                "that they have. Give a detailed, structured complete recipe."
                "Structure the recipe into sections (respect the order): Name of the dish, Ingredients, and Steps. "
                "Do not give any other information, just the essentials."}, ]


def ask_llm(user_input: str):
    """
    Sends a user input to the LLM and prints the streamed response.

    Assumes `client` and `messages` are defined globally.
    """
    if user_input.lower() in ["quit", "exit", "stop"]:
        return "Session ended."

    messages.append({"role": "user", "content": user_input})

    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=messages,
        stream=True,
    )

    assistant_reply = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        assistant_reply += content

    messages.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply


# print(ask_llm("Can you give me a recipe for spaghetti carbonara?"))
