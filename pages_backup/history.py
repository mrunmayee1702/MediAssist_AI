import streamlit as st

st.set_page_config(
    page_title="Chat History",
    page_icon="🕘",
    layout="wide"
)

st.markdown("""
<style>
.block-container{ padding-top:2rem; }
.title{ font-size:45px; font-weight:bold; color:white; text-align:center; }
.subtitle{ text-align:center; color:#9ca3af; font-size:18px; margin-bottom:30px; }
.history-card{
    background:#1B1F2A; padding:18px; border-radius:18px;
    border:1px solid #313543; margin-bottom:15px; transition:.3s;
}
.history-card:hover{ border:1px solid #6C63FF; }
.role{ color:#6C63FF; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🕘 Chat History</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">View and continue your previous conversations with MediAssist AI.</div>',
    unsafe_allow_html=True
)
st.markdown("---")

# shared state (same keys as app.py)
if "history" not in st.session_state:
    st.session_state.history = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

search = st.text_input("🔍 Search History")

history = st.session_state.history

if len(history) == 0:
    st.info("No chat history available.")
else:
    if search:
        filtered_ids = [
            cid for cid, chat in history.items()
            if search.lower() in chat["title"].lower()
            or any(search.lower() in m["content"].lower() for m in chat["messages"])
        ]
    else:
        filtered_ids = list(history.keys())

    for chat_id in reversed(filtered_ids):

        chat = history[chat_id]

        st.markdown(f"""
<div class="history-card">
<div class="role">💬 {chat['title']}</div>
</div>
""", unsafe_allow_html=True)

        with st.expander("View conversation"):
            for msg in chat["messages"]:
                role_label = "You" if msg["role"] == "user" else "MediAssist AI"
                st.markdown(f"**{role_label}:** {msg['content']}")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("▶️ Continue Chat", key=f"page_continue_{chat_id}", use_container_width=True):
                st.session_state.messages = chat["messages"].copy()
                st.session_state.current_chat_id = chat_id
                st.switch_page("app.py")  # change "app.py" if your main file has a different name

        with c2:
            if st.button("🗑️ Delete", key=f"page_delete_{chat_id}", use_container_width=True):
                del st.session_state.history[chat_id]
                if st.session_state.current_chat_id == chat_id:
                    st.session_state.messages = []
                    st.session_state.current_chat_id = None
                st.rerun()

st.write("")

if st.button("🗑️ Clear All History"):
    st.session_state.history = {}
    st.session_state.messages = []
    st.session_state.current_chat_id = None
    st.success("History Cleared Successfully.")
    st.rerun()

st.markdown("---")
st.caption("🩺 MediAssist AI • Chat History")