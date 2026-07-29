import base64
import re
from chatbot.groq_chat import client


def extract_prescription_info(image_file, language="English"):
    """
    Reads a doctor's prescription from an uploaded image and extracts
    it into simple, structured information. This only explains what the
    doctor already wrote — it never adds, changes, or recommends
    anything of its own.

    `image_file` is a Streamlit UploadedFile object.
    """

    image_bytes = image_file.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    mime_type = image_file.type or "image/jpeg"

    prompt = f"""
You are MediAssist AI's Prescription Explainer. You are given a photo of
a doctor's handwritten or printed prescription. Your job is ONLY to read
and explain what the doctor already wrote — you do not add, suggest, or
change anything.

Respond in {language}.

Read the image carefully, but keep your reasoning brief and move quickly
to your final answer — don't over-analyze small handwriting details at
length; give your best reasonable reading and proceed.

Respond in exactly this format:

### 📅 Date

The date on the prescription, if visible. If not visible, say "Not visible on the prescription".

### 💊 Medicines Prescribed

For each medicine, give ONE compact block like this (no extra filler text):

**1. Medicine Name**
- Frequency: explain any shorthand in simple language (OD = once a day, BD = twice a day, TDS = three times a day, QID = four times a day, HS = at bedtime, SOS = only if needed, PRN = as needed). Only state what's actually written.
- Food: before food / after food / with food / not specified — only what's written.
- Duration: how many days, if written; otherwise "Not specified".

Repeat this block for each medicine. Keep it tight — no repeated paragraphs.

### 🧪 Recommended Tests

List any lab tests or investigations the doctor has written (e.g. blood test, X-ray, sugar test), as short bullet points. If none, say so in one line.

### 📝 Doctor's Other Instructions

Any other notes or advice, in 2-3 short bullet points max. If none, say so in one line.

### ⚠️ Disclaimer

One short paragraph: this is only a plain-language reading of what's written on the image, may contain errors especially with unclear handwriting, always follow the original prescription and confirm anything unclear with your doctor or pharmacist.

STRICT RULES:
1. NEVER add a medicine, dosage, frequency, or instruction that isn't
   actually visible on the prescription.
2. NEVER suggest alternative medicines or additional treatment.
3. If the image is unclear or not a prescription, say so clearly instead
   of guessing.
4. Do not diagnose the condition being treated unless the diagnosis is
   explicitly written on the prescription.
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
        temperature=0.2,
        max_tokens=3000,
        reasoning_format="hidden",
    )

    content = response.choices[0].message.content

    # If the model's internal reasoning got cut off before it ever
    # closed the <think> tag (ran out of tokens mid-thought), don't
    # show that raw reasoning to the user — show a clean message instead.
    if "<think>" in content and "</think>" not in content:
        return (
            "⚠️ I couldn't finish reading this prescription clearly in one go. "
            "Please try again — a clearer, well-lit, straight-on photo usually "
            "works best."
        )

    # Remove any reasoning wrapper some vision models emit (<think>...</think>)
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

    if not content:
        return (
            "⚠️ I couldn't extract a clear reading from this prescription image. "
            "Please try again with a clearer photo."
        )

    return content


def build_prescription_followup_system_prompt(extracted_info, language="English"):
    """
    System prompt used for follow-up questions about a prescription
    that's already been read and explained. Uses the extracted text
    as context instead of re-sending the image each time.
    """

    return f"""
You are MediAssist AI's Prescription Explainer, continuing a conversation
with a user about a prescription you already read for them.

Respond in {language}.

Here is what was extracted from their prescription earlier:

{extracted_info}

Answer the user's follow-up questions about this prescription in simple
language, using only the information above.

STRICT RULES:
1. NEVER add a medicine, dosage, frequency, or instruction that wasn't
   in the extracted information above.
2. NEVER suggest alternative medicines, additional treatment, or tell
   the user to take/stop/change anything.
3. If asked something the extracted information doesn't cover, say so
   clearly and suggest asking their doctor or pharmacist.
4. Do not diagnose any condition.
"""