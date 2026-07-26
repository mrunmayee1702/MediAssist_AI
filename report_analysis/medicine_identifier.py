import os
import base64
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def identify_medicine(image_file):
    """
    Identify a medicine from an uploaded image (strip/box/label/pill)
    and explain what it's commonly used for.
    `image_file` is a Streamlit UploadedFile object.
    """

    image_bytes = image_file.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    mime_type = image_file.type or "image/jpeg"

    prompt = """
You are MediAssist AI, helping a user identify a medicine from a photo
(packaging, strip, label, or pill/tablet itself).

Look at the image carefully and respond in this exact format:

# 💊 Medicine Identified

Name of the medicine (brand name and generic/salt name if visible or identifiable).
If you cannot confidently identify it, say so clearly instead of guessing.

# 🩺 Commonly Used For

Explain, in simple language, what condition(s) or disease(s) this medicine is
typically used to treat.

# 📋 General Information

Mention typical form (tablet/syrup/capsule) and any general usage notes visible
on the packaging (e.g. dosage printed on strip), without prescribing or
recommending a dose yourself.

# ⚠ Disclaimer

Image-based identification can be inaccurate, especially for loose pills without
packaging. This is not a substitute for pharmacist or doctor confirmation.
Do NOT take, stop, or change any medication based on this alone — please confirm
with a pharmacist or doctor before use.
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    content = response.choices[0].message.content

    # Remove reasoning (<think>...</think>)
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

    return content