import streamlit as st
from rag.rag_chat import get_ai_response

# ---------------------------------------
# Page Config
# ---------------------------------------

st.set_page_config(
    page_title="AI Chat",
    page_icon="💬",
    layout="wide"
)

# ---------------------------------------
# Session State
# ---------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------
# CSS
# ---------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:1.5rem;
}

.main{
    background:#0E1117;
}

.title{
    font-size:45px;
    font-weight:bold;
    color:white;
    text-align:center;
}

.subtitle{
    text-align:center;
    color:#9ca3af;
    font-size:18px;
    margin-bottom:30px;
}

.question-card{

    background:#1B1F2A;
    border-radius:18px;
    padding:18px;
    border:1px solid #2f3544;
    transition:.3s;
    margin-bottom:15px;

}

.question-card:hover{

    border:1px solid #6C63FF;
    transform:translateY(-4px);

}

.chat-box{

    background:#171B25;
    padding:15px;
    border-radius:18px;

}

.stChatMessage{

    border-radius:15px;

}

.stButton>button{

    width:100%;
    height:50px;
    border-radius:14px;
    border:none;
    font-weight:bold;

}

hr{
    border:1px solid #2c3242;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# Header
# ---------------------------------------

st.markdown(
'<div class="title">💬 AI Medical Chat</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="subtitle">Ask any medical question and get AI-powered health guidance.</div>',
unsafe_allow_html=True
)

# ---------------------------------------
# Suggested Questions
# ---------------------------------------

if len(st.session_state.messages)==0:

    st.markdown("## 💡 Popular Questions")

    col1,col2=st.columns(2)

    with col1:

        if st.button("🩸 Explain CBC Report"):
            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":"Explain CBC Report"
                }
            )

        if st.button("🩺 What is Diabetes?"):
            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":"What is Diabetes?"
                }
            )

        if st.button("❤️ Symptoms of Heart Attack"):
            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":"Symptoms of Heart Attack"
                }
            )

    with col2:

        if st.button("🧪 Explain Creatinine Test"):
            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":"Explain Creatinine Test"
                }
            )

        if st.button("🦟 Symptoms of Dengue"):
            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":"Symptoms of Dengue"
                }
            )

        if st.button("🧬 What is Thyroid?"):
            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":"What is Thyroid?"
                }
            )

st.markdown("---")

# ---------------------------------------
# Display Chat History
# ---------------------------------------

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user", avatar="🧑"):

            st.markdown(message["content"])

    else:

        with st.chat_message("assistant", avatar="🩺"):

            st.markdown(message["content"])


# ---------------------------------------
# Generate AI Response for Suggested Questions
# ---------------------------------------

if (
    len(st.session_state.messages) > 0
    and st.session_state.messages[-1]["role"] == "user"
):

    if (
        len(st.session_state.messages) == 1
        or st.session_state.messages[-2]["role"] == "assistant"
    ):

        with st.chat_message("assistant", avatar="🩺"):

            with st.spinner("🧠 Thinking..."):

                answer = get_ai_response(
                    st.session_state.messages[-1]["content"]
                )

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


st.markdown("---")

st.markdown(
"""
### 💡 Tips

- Ask about diseases
- Explain blood reports
- Upload medical reports
- Ask follow-up questions
- Learn medical terms
"""
)

# ---------------------------------------
# Chat Input
# ---------------------------------------

prompt = st.chat_input(
    "💬 Ask anything about health, diseases, reports or symptoms..."
)

if prompt:

    # User Message

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user", avatar="🧑"):

        st.markdown(prompt)

    # AI Reply

    with st.chat_message("assistant", avatar="🩺"):

        with st.spinner("🧠 MediAssist AI is thinking..."):

            answer = get_ai_response(prompt)

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

st.write("")

# ---------------------------------------
# Bottom Buttons
# ---------------------------------------

col1,col2,col3=st.columns(3)

with col1:

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages=[]

        st.rerun()

with col2:

    if st.button("💬 New Chat"):

        st.session_state.messages=[]

        st.rerun()

with col3:

    st.download_button(

        "📥 Download Chat",

        data="\n\n".join(
            [
                f"{m['role'].upper()} : {m['content']}"
                for m in st.session_state.messages
            ]
        ),

        file_name="chat_history.txt",

        mime="text/plain"

    )

st.write("")
st.write("")

st.markdown("---")

st.caption(
    "🩺 MediAssist AI • Powered by Llama 3.3 + RAG • Educational Use Only"
)