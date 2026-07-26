import streamlit as st
from rag.rag_chat import get_ai_response

# ----------------------------------------
# Page Config
# ----------------------------------------

st.set_page_config(
    page_title="Medical Dictionary",
    page_icon="📖",
    layout="wide"
)

# ----------------------------------------
# CSS
# ----------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

.title{
    font-size:46px;
    font-weight:bold;
    color:white;
    text-align:center;
}

.subtitle{
    text-align:center;
    color:#9ca3af;
    font-size:18px;
    margin-bottom:35px;
}

.card{
    background:#1B1F2A;
    padding:20px;
    border-radius:18px;
    border:1px solid #313543;
    transition:0.3s;
}

.card:hover{
    border:1px solid #6C63FF;
    transform:translateY(-4px);
}

.stButton>button{
    width:100%;
    height:48px;
    border-radius:14px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# Header
# ----------------------------------------

st.markdown(
'<div class="title">📖 Medical Dictionary</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="subtitle">Search any medical term and get an easy-to-understand explanation.</div>',
unsafe_allow_html=True
)

# ----------------------------------------
# Feature Cards
# ----------------------------------------

c1,c2,c3=st.columns(3)

with c1:

    st.markdown("""
<div class="card">

### 🧠 AI Explanations

Easy Language

Medical Concepts

Clinical Meaning

</div>
""",unsafe_allow_html=True)

with c2:

    st.markdown("""
<div class="card">

### 🩺 Covers

Diseases

Blood Tests

Medicines

Anatomy

</div>
""",unsafe_allow_html=True)

with c3:

    st.markdown("""
<div class="card">

### 📚 Powered By

Llama 3.3

Medical Knowledge

RAG Support

</div>
""",unsafe_allow_html=True)

st.write("")
st.markdown("---")

# ----------------------------------------
# Search Box
# ----------------------------------------

term = st.text_input(
    "🔍 Search a Medical Term",
    placeholder="Example: Creatinine, Diabetes, CBC..."
)

# ----------------------------------------
# Popular Terms
# ----------------------------------------

st.markdown("### 🔥 Popular Medical Terms")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🩸 CBC"):
        term = "CBC"

    if st.button("🧪 Creatinine"):
        term = "Creatinine"

with c2:
    if st.button("🩺 Diabetes"):
        term = "Diabetes"

    if st.button("❤️ Blood Pressure"):
        term = "Blood Pressure"

with c3:
    if st.button("🧬 Thyroid"):
        term = "Thyroid"

    if st.button("🫀 Cholesterol"):
        term = "Cholesterol"

st.write("")

# ----------------------------------------
# Search
# ----------------------------------------

if st.button("🔍 Search"):

    if term.strip() == "":

        st.warning("Please enter a medical term.")

    else:

        prompt = f"""
Explain the medical term:

{term}

Answer using the following headings:

## Definition

## Causes

## Symptoms

## Diagnosis

## Treatment Overview

## Prevention

Explain everything in simple language.

Do not prescribe medicines.

If appropriate, recommend consulting a healthcare professional.
"""

        with st.spinner("Searching medical knowledge..."):

            answer = get_ai_response(prompt)

        st.success("Information Found")

        st.markdown("---")

        st.markdown(answer)

        st.markdown("---")

        st.info("""
📌 **Educational Purpose Only**

This information is intended for learning and general awareness.

It should not replace professional medical advice, diagnosis, or treatment.
""")