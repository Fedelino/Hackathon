from together import Together

client = Together(api_key="tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8")


def call_llm(user_input: str, context: str = ""):
    """
    Sends a user input to the LLM and returns the streamed response.
    Adds context to the system message dynamically.
    """
    if user_input.lower() in ["quit", "exit", "stop"]:
        return "Session ended."

    # Create a fresh messages list for each call
    system_content = (
        "You are a helpful cooking assistant. The user will ask questions, "
        "respond with short and clear answers. No longer than 2 sentences."
    )
    if context:
        system_content += f" For context, here is the dish that the user is cooking: {context}"

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_input},
    ]

    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=messages,
        stream=True,
    )

    assistant_reply = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        assistant_reply += content

    return assistant_reply
