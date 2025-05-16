from together import Together

client = Together(api_key="tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8")

messages = [
    {"role": "system", "content": "You are a helpful cooking assistant. Give only one short and clear "
                                  "step at a time, suitable for a user who is busy cooking and has no "
                                  "hands free."},
]

print("Cooking Assistant is ready. Say something")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["quit", "exit", "stop"]:
        break

    messages.append({"role": "user", "content": user_input})

    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=messages,
        stream=True,
    )

    print("Assistant: ", end="", flush=True)
    assistant_reply = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        assistant_reply += content

    print("\n")
    messages.append({"role": "assistant", "content": assistant_reply})
