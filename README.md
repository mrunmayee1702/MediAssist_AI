# 🩺 MediAssist AI

<p align="center">
  <h3 align="center">AI-Powered Medical Assistant for Report Analysis & Health Guidance</h3>

  <p align="center">
    An intelligent healthcare assistant built using Artificial Intelligence, Retrieval-Augmented Generation (RAG), Groq LLM, and Vision AI to simplify medical information and provide personalized healthcare guidance.
  </p>
</p>

---

## 📖 About the Project

MediAssist AI is an AI-powered healthcare assistant designed to help users understand medical reports, identify medicines, analyze symptoms, and receive personalized healthcare guidance.

The system combines **Large Language Models (LLMs)**, **Retrieval-Augmented Generation (RAG)**, **FAISS Vector Database**, and **Vision AI** to generate accurate, context-aware, and easy-to-understand medical responses.

> **Disclaimer:** MediAssist AI is developed for educational purposes and provides healthcare guidance only. It is **not intended to replace professional medical advice, diagnosis, or treatment.**

---

# ✨ Features

- 🔐 Secure User Authentication
- 🤖 AI Medical Chatbot
- 📄 Medical Report Upload & Analysis
- 📑 Medical Report Comparison
- 🧠 Retrieval-Augmented Generation (RAG)
- 💊 Medicine Identifier (Vision AI)
- 📋 Prescription Explainer
- 🩺 Symptom Checker
- 👤 Personalized Responses using Patient Profile
- 🔔 Medicine & Appointment Reminders
- 🕒 Conversation History
- 🌍 Multilingual Support (English, Hindi & Marathi)
- ⚡ Fast AI Response Generation
- 🔒 Secure Data Handling

---

# 🏗️ System Architecture

```
                    User
                      │
                      ▼
            Streamlit Web Application
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
 Medical Chat   Report Analysis   Medicine Identifier
      │               │                │
      ▼               ▼                ▼
    Groq LLM      PDF Processing      Qwen Vision
      │               │                │
      └───────────────┼────────────────┘
                      ▼
            AI Response Generation
                      │
                      ▼
               Display to User
```

---

# 🧠 RAG Workflow

```
Medical PDF
      │
      ▼
PyMuPDF
(Text Extraction)
      │
      ▼
Text Chunking
      │
      ▼
SentenceTransformer
(all-MiniLM-L6-v2)
      │
      ▼
FAISS Vector Database
      │
      ▼
Retrieve Relevant Context
      │
      ▼
Groq Llama-3.3-70B
      │
      ▼
Final AI Response
```

---

# 🤖 AI Models Used

| Model | Purpose |
|--------|----------|
| **Groq Llama-3.3-70B-Versatile** | Medical Chatbot, Report Analysis, Symptom Checker |
| **Qwen Vision** | Medicine Identifier |
| **SentenceTransformer (all-MiniLM-L6-v2)** | Text Embeddings |
| **FAISS** | Semantic Similarity Search |

---

# 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI & Machine Learning
- Groq Llama-3.3-70B
- Qwen Vision
- SentenceTransformer
- Retrieval-Augmented Generation (RAG)

### Database
- SQLite
- FAISS Vector Database

### Libraries
- PyMuPDF
- FAISS
- SentenceTransformers
- Pillow
- NumPy
- Pickle
- Python-dotenv

---

# 📂 Project Structure

```
MediAssist_AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── auth/
├── chatbot/
├── rag/
├── report_analysis/
├── medicine_identifier/
├── symptom_checker/
├── reminders/
├── profile/
├── vector_db/
├── database/
├── assets/
└── screenshots/
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/mrunmayee1702/MediAssist_AI.git
```

Go to the project folder

```bash
cd MediAssist_AI
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file and add:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
```

---

# ▶️ Run the Project

```bash
streamlit run app.py
```

---

# 📸 Screenshots

### 🔐 Login Page

_Add Screenshot_

---

### 🤖 Medical Chatbot

_Add Screenshot_

---

### 📄 Medical Report Analysis

_Add Screenshot_

---

### 💊 Medicine Identifier

_Add Screenshot_

---

### 🩺 Symptom Checker

_Add Screenshot_

---

### 🔔 Reminder Module

_Add Screenshot_

---

# 🚀 Future Scope

- OCR for Handwritten Prescriptions
- Voice-Based Medical Assistant
- Doctor Consultation Integration
- Mobile Application
- Cloud Deployment
- Wearable Device Integration
- Electronic Health Record (EHR) Support

---

# 👨‍💻 Contributors

- **Mrunmayee Shinde**
- Team Members

---

# 📄 License

This project is developed for educational purposes only.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
