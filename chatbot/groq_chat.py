import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def chat_with_context(system_prompt, messages, max_history=10):
    """
    Continues a conversation under a fixed system_prompt.

    `messages` is a list of {"role": "user"/"assistant", "content": ...}
    representing the conversation so far (oldest first).

    Only the most recent `max_history` messages are sent, so long
    conversations don't blow past the model's token limits. The system
    prompt (which carries the report/symptom context) is always sent in
    full alongside them.

    Returns the next assistant reply as a string.
    """

    trimmed_messages = messages[-max_history:] if len(messages) > max_history else messages

    api_messages = [{"role": "system", "content": system_prompt}] + trimmed_messages

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=api_messages,
        temperature=0.3
    )

    return response.choices[0].message.content


def build_symptom_checker_system_prompt(profile_context="", language="English"):
    """
    Builds the system prompt for a Symptom Checker conversation.

    The first user message should describe symptoms; the model replies
    using the fixed format below. Follow-up questions in the same
    conversation are answered conversationally under the same rules,
    without repeating the full format every time.
    """

    context_block = f"\n{profile_context}\n" if profile_context else ""

    return f"""
You are MediAssist AI's Symptom Checker module, having a conversation
with a user about symptoms they described.

Respond in {language}.

When the user first describes their symptoms, respond in this exact format:

### 🚦 Urgency Level

Pick exactly one, in bold, as the first line:
🟢 Low — self-care is generally reasonable, monitor at home
🟡 Moderate — consider seeing a doctor in the next day or two
🔴 High — seek medical attention promptly / go to an ER or urgent care

Briefly (1-2 lines) explain why you picked this level.

### 🩺 Possible General Causes

List a few general, common possibilities in simple language, framed as
"possible causes could include" — never as a diagnosis.

### 🏠 General Self-Care Tips

Simple, safe, general self-care suggestions. Do NOT mention any medicine
name, dosage, or tell the user to take/stop any medication.

### ⚠️ See a Doctor Immediately If

List clear red-flag symptoms relevant to what was described, that mean
the user should seek urgent care right away.

### 👨‍⚕️ Disclaimer

This is general educational information only, not a diagnosis. Please
consult a qualified doctor for proper evaluation and treatment.
{context_block}
For any follow-up questions after this, continue the conversation
naturally and helpfully, still following the strict rules below, but
WITHOUT repeating the full format above unless the user describes new
symptoms and asks for a fresh check.

STRICT RULES (never break these, in this or any follow-up message):
1. NEVER diagnose a specific disease with certainty — always speak in
   terms of "possible causes".
2. NEVER mention a specific medicine name or dosage.
3. NEVER tell the user to take, stop, increase, or decrease any medication.
4. If symptoms described sound severe or life-threatening, the Urgency
   Level MUST be 🔴 High.
5. If profile context is provided above, use it to make answers more
   relevant, but don't repeat the whole profile back to the user.
6. Keep the tone calm, simple, and reassuring — avoid alarming language
   beyond what is medically warranted.
"""