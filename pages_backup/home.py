import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.block-container{
    padding-top:2rem;
}

.title{
    font-size:58px;
    font-weight:700;
    text-align:center;
    color:white;
}

.subtitle{
    text-align:center;
    color:#9ca3af;
    font-size:22px;
    margin-bottom:40px;
}

.card{
    background:#1B1F2A;
    padding:25px;
    border-radius:18px;
    border:1px solid #313543;
    transition:.3s;
    height:230px;
}

.card:hover{
    border:1px solid #4F46E5;
    transform:translateY(-5px);
}

.feature{
    font-size:23px;
    color:white;
    font-weight:bold;
}

.text{
    color:#c9c9c9;
    font-size:16px;
}

.metric{
    background:#171B25;
    border-radius:15px;
    padding:20px;
    text-align:center;
}

.metric h2{
    color:#6C63FF;
    margin:0;
}

.metric p{
    color:white;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🩺 MediAssist AI</div>', unsafe_allow_html=True)

st.markdown(
'<div class="subtitle">AI Medical Report Analysis & Intelligent Healthcare Assistant</div>',
unsafe_allow_html=True)

st.markdown("## 🚀 Features")

col1,col2,col3=st.columns(3)

with col1:

    st.markdown("""
<div class="card">
<div class="feature">💬 AI Chatbot</div>
<br>
<div class="text">
Ask unlimited medical questions.

✔ Diseases

✔ Symptoms

✔ Blood Tests

✔ Nutrition

✔ Health Guidance
</div>
</div>
""",unsafe_allow_html=True)

with col2:

    st.markdown("""
<div class="card">
<div class="feature">📄 Report Analysis</div>
<br>
<div class="text">

Upload blood reports and laboratory reports.

✔ AI Analysis

✔ Summary

✔ Abnormal Values

✔ Recommendations

</div>
</div>
""",unsafe_allow_html=True)

with col3:

    st.markdown("""
<div class="card">
<div class="feature">📖 Medical Dictionary</div>
<br>
<div class="text">

Search medical terms instantly.

✔ Easy Explanation

✔ Causes

✔ Symptoms

✔ Normal Ranges

</div>
</div>
""",unsafe_allow_html=True)

st.write("")
st.write("")

st.markdown("## 📊 MediAssist Overview")

m1,m2,m3,m4=st.columns(4)

with m1:
    st.markdown("""
<div class="metric">
<h2>30+</h2>
<p>Medical PDFs</p>
</div>
""",unsafe_allow_html=True)

with m2:
    st.markdown("""
<div class="metric">
<h2>AI</h2>
<p>Powered by Llama 3.3</p>
</div>
""",unsafe_allow_html=True)

with m3:
    st.markdown("""
<div class="metric">
<h2>24/7</h2>
<p>Available</p>
</div>
""",unsafe_allow_html=True)

with m4:
    st.markdown("""
<div class="metric">
<h2>RAG</h2>
<p>Knowledge Base</p>
</div>
""",unsafe_allow_html=True)

st.write("")
st.write("")

st.markdown("## ⚙️ How It Works")

st.markdown("""
### 1️⃣ Ask a Medical Question

Use the AI chatbot to ask any healthcare-related question.

---

### 2️⃣ Upload Medical Report

Upload CBC, Blood Test, Kidney Function, Liver Function, or any PDF report.

---

### 3️⃣ Get AI Analysis

Receive an easy-to-understand explanation along with important findings.

---

### 4️⃣ Continue the Conversation

Ask follow-up questions naturally like ChatGPT.
""")

st.write("")
st.success("💙 Your Intelligent Healthcare Companion")