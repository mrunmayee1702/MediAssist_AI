from chatbot.groq_chat import client
from rag.retriever import retrieve_context


# ---------------------------------------------------
# Intent Classification
# ---------------------------------------------------

def classify_message(message):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": """
You are an intent classifier.

Classify the user's message into ONLY one category.

Return ONLY one word.

Possible categories:

CASUAL
MEDICAL
NON_MEDICAL

Examples:

Hi -> CASUAL
Hello -> CASUAL
Thank you -> CASUAL
Bye -> CASUAL

What is diabetes? -> MEDICAL
Explain CBC Report -> MEDICAL
What are symptoms of dengue? -> MEDICAL

Who is Virat Kohli? -> NON_MEDICAL
Write Python code -> NON_MEDICAL
Tell me a joke -> NON_MEDICAL
"""
            },

            {
                "role": "user",
                "content": message
            }

        ]

    )

    return response.choices[0].message.content.strip().upper()


# ---------------------------------------------------
# Main Chat Function
# ---------------------------------------------------

def get_ai_response(question, profile_context="", language="English"):

    intent = classify_message(question)

    # ------------------------------------------------
    # Casual Conversation
    # ------------------------------------------------

    if intent == "CASUAL":

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role": "system",
                    "content": f"""
You are MediAssist AI.

You are a friendly AI medical assistant.

Behave naturally like ChatGPT.

If the user greets you,
greet them warmly.

If the user thanks you,
reply politely.

If the user says goodbye,
wish them well.

Keep responses short and friendly.

Respond in {language}.
"""
                },

                {
                    "role": "user",
                    "content": question
                }

            ]

        )

        return response.choices[0].message.content

    # ------------------------------------------------
    # Non Medical
    # ------------------------------------------------

    if intent == "NON_MEDICAL":

        return """
I'm MediAssist AI 🩺

I'm designed specifically to help with medical and healthcare-related topics.

You can ask me about:

• Diseases
• Symptoms
• Medical Reports
• Blood Tests
• Lab Reports
• Nutrition
• Human Anatomy
• General Healthcare

Feel free to ask any medical question.
"""

    # ------------------------------------------------
    # Medical Query
    # ------------------------------------------------

    docs = retrieve_context(question)

    context = ""

    if len(docs) > 0:

        for doc in docs:

            context += doc["text"] + "\n\n"

    # ------------------------------------------------
    # Patient profile context (from Profile page)
    # ------------------------------------------------

    profile_block = f"\nPatient Context:\n{profile_context}\n" if profile_context else ""

    # ------------------------------------------------
    # Final Prompt
    # ------------------------------------------------

    prompt = f"""
You are MediAssist AI, an intelligent AI-powered medical assistant.

Your goal is to provide accurate, reliable, and easy-to-understand medical information.

Respond in {language}.

You have access to:

1. Your own general medical knowledge.
2. Additional medical reference material (if provided below).
3. Basic patient profile context (if provided below), such as age,
   known conditions, or allergies.

Instructions:

• Always answer medical and healthcare-related questions, even if no reference material is available.
• Use your own medical knowledge as the primary source of information.
• If the reference material is relevant, use it to improve or expand your answer.
• Never depend entirely on the reference material.
• If the reference material is unrelated or incomplete, ignore it and answer using your own medical knowledge.
• If patient profile context is provided, use it to make your answer more relevant
  (e.g. mention if something is especially important given a known condition or allergy),
  but do not repeat the whole profile back to the user and do not diagnose based on it.
• Explain concepts in simple language.
• Be conversational, friendly, and professional.
• Structure answers using ### sub-headings and bullet points when helpful (avoid top-level # headings).
• If the user asks follow-up questions, continue the conversation naturally.
• Never mention:
  - PDFs
  - Context
  - Retrieved documents
  - Knowledge base
  - Internal sources
• Never say:
  - "I couldn't find information."
  - "The knowledge base does not contain..."
• Never invent medical facts.
• Never diagnose diseases.
• Never prescribe medicines.
• Recommend consulting a qualified healthcare professional whenever appropriate.

Reference Material (may or may not be useful):

{context}
{profile_block}
User Question:

{question}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": question
            }
        ]

    )

    return response.choices[0].message.content