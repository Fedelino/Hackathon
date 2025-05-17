import os
import cv2
import requests
from PIL import Image
from io import BytesIO
from together import Together

HUGGINGFACE_API_TOKEN = ""
HF_MODEL_URL = "https://api-inference.huggingface.co/models/nateraw/food"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
    "Content-Type": "image/jpeg"
}

client = Together(api_key="tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8")

messages = [{
    "role": "system",
    "content": (
        "You are a helpful cooking assistant. The user will give you observed ingredients or cooking steps. "
        "Guess what dish is being cooked and give a structured recipe. "
        "Structure the output into: Name of the Dish, Ingredients, and Steps. Do not add extra explanation."
    )
}]

def classify_image_from_frame(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    response = requests.post(HF_MODEL_URL, headers=HEADERS, data=img_bytes)
    response.raise_for_status()
    return response.json()

def summarize_labels(labels):
    frequency = {}
    for label in labels:
        name = label[0]['label'] if isinstance(label, list) and label else 'unknown'
        frequency[name] = frequency.get(name, 0) + 1
    return frequency

def infer_dish_from_labels(frequency: dict):
    items = ", ".join([f"{ingredient} ({count})" for ingredient, count in frequency.items()])
    prompt = f"Based on these observed ingredients: {items}, what dish is likely being cooked? Return the full recipe."

    messages.append({"role": "user", "content": prompt})
    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=messages,
        stream=True
    )

    assistant_reply = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        assistant_reply += content

    messages.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

if __name__ == "__main__":
    print("Accessing webcam...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot access webcam.")
        exit()

    labels = []
    frame_count = 0
    max_frames = 10

    print(f"Capturing {max_frames} frames. Press 'q' to quit early.")
    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Webcam Feed - Press 'q' to quit", frame)

        try:
            result = classify_image_from_frame(frame)
            labels.append(result)
            print(f"Frame {frame_count+1}: {result[0]['label']} ({result[0]['score']:.2f})")
        except Exception as e:
            print(f"Error on frame {frame_count+1}: {e}")

        frame_count += 1

        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("Summarizing and inferring dish...")
    freq = summarize_labels(labels)
    dish = infer_dish_from_labels(freq)
    print("\nLikely Dish:", dish)