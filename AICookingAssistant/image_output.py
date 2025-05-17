import requests
from PIL import Image
from io import BytesIO
from keys import HUGGING_FACE_API_KEY

API_URL = "https://router.huggingface.co/hf-inference/models/nateraw/food"
HEADERS = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}",
    "Content-Type": "image/jpeg"
}


def food(image_path_or_file):
    """
    Accepts either:
    - a string file path
    - a Flask FileStorage object (uploaded image)
    Returns list of labels + scores
    """
    if isinstance(image_path_or_file, str):
        image = Image.open(image_path_or_file).convert("RGB")
    else:
        # file-like object (e.g., Flask upload)
        image = Image.open(BytesIO(image_path_or_file.read())).convert("RGB")
        image_path_or_file.seek(0)  # reset pointer so Flask can re-read if needed

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()

    response = requests.post(API_URL, headers=HEADERS, data=img_bytes)
    response.raise_for_status()
    return response.json()


# Leave the testing CLI block as-is
if __name__ == "__main__":
    image_path = input("🖼 Enter the path to your food image: ").strip()
    try:
        result = food(image_path)
        print("\n🍽️ Detected Food Items:")
        for item in result:
            print(f"- {item['label']}: {item['score'] * 100:.2f}%")
    except FileNotFoundError:
        print("❌ File not found. Please check the path.")
    except Exception as e:
        print("❌ Error:", e)
