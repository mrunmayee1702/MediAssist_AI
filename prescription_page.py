import streamlit as st
from datetime import datetime
from report_analysis.prescription_reader import (
    extract_prescription_info,
    build_prescription_followup_system_prompt,
)
from chatbot.groq_chat import chat_with_context


def render_prescription_page():
    """
    Renders the Prescription Explainer page: upload a photo of a
    prescription, get it explained in plain language inside a clean
    prescription-style card, and ask follow-up questions about it.
    """

    st.markdown("""
    <style>

    .prescription-header {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 0.3rem;
    }

    .prescription-icon {
        font-size: 2rem;
    }

    .prescription-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        color: #EAF2F5;
    }

    .prescription-subtitle {
        color: #8B95A8;
        font-size: 0.9rem;
        margin-bottom: 1.2rem;
    }

    /* ---------------- Prescription card (dark theme, matches app) ---------------- */

    .st-key-prescription_card {
        background: rgba(28, 34, 48, 0.55);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        padding: 1.6rem 1.8rem 1.2rem 1.8rem;
        box-shadow: 0 6px 22px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1rem;
    }

    .rx-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.6rem;
        margin-bottom: 0.8rem;
    }

    .rx-card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        color: #2DD4BF !important;
    }

    .rx-card-meta {
        font-size: 0.78rem;
        color: #8B95A8 !important;
        text-align: right;
    }

    .st-key-prescription_card h3 {
        color: #2DD4BF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.4rem !important;
        animation: none !important;
    }

    .st-key-prescription_card p,
    .st-key-prescription_card li,
    .st-key-prescription_card span,
    .st-key-prescription_card strong {
        color: #EAF2F5 !important;
        font-size: 0.9rem !important;
        line-height: 1.55 !important;
    }

    .st-key-prescription_card strong {
        color: #2DD4BF !important;
    }

    .st-key-prescription_card ul {
        margin-top: 0.1rem !important;
        margin-bottom: 0.4rem !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='prescription-header'>
            <div class='prescription-icon'>📋</div>
            <div class='prescription-title'>Prescription Explainer</div>
        </div>
        <div class='prescription-subtitle'>
            Upload a clear photo of your doctor's prescription. MediAssist AI
            will explain the medicines, timings, and instructions in simple
            language — it only reads what's written, never adds anything.
        </div>
    """, unsafe_allow_html=True)

    if "prescription_messages" not in st.session_state:
        st.session_state.prescription_messages = []

    if "prescription_system_prompt" not in st.session_state:
        st.session_state.prescription_system_prompt = ""

    # -----------------------------------
    # Upload + extract
    # -----------------------------------

    if len(st.session_state.prescription_messages) == 0:

        prescription_image = st.file_uploader(
            "Upload Prescription Image",
            type=["jpg", "jpeg", "png"],
            key="prescription_image_uploader"
        )

        if prescription_image:
            st.image(prescription_image, caption="Uploaded Prescription", width=300)

        if st.button("📖 Explain Prescription", type="primary", use_container_width=True):

            if prescription_image is None:
                st.warning("Please upload a prescription image first.")

            else:
                language = st.session_state.get("language", "English")

                with st.spinner("Reading your prescription..."):
                    extracted_info = extract_prescription_info(prescription_image, language)

                system_prompt = build_prescription_followup_system_prompt(extracted_info, language)
                st.session_state.prescription_system_prompt = system_prompt

                st.session_state.prescription_messages = [
                    {"role": "assistant", "content": extracted_info}
                ]

                st.rerun()

        return

    # -----------------------------------
    # Result card (first message) + follow-up conversation
    # -----------------------------------

    username = st.session_state.get("username", "")
    generated_on = datetime.now().strftime("%d %b %Y, %I:%M %p")

    rx_card = st.container(key="prescription_card")

    with rx_card:

        st.markdown(f"""
            <div class='rx-card-header'>
                <div class='rx-card-title'>📋 Prescription Summary</div>
                <div class='rx-card-meta'>@{username}<br>{generated_on}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(st.session_state.prescription_messages[0]["content"])

    # Any follow-up Q&A after the first message shows as a normal chat
    follow_up_history = st.session_state.prescription_messages[1:]

    for msg in follow_up_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    follow_up = st.chat_input("Ask a question about this prescription...")

    if follow_up:

        st.session_state.prescription_messages.append({"role": "user", "content": follow_up})

        with st.chat_message("user"):
            st.markdown(follow_up)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chat_with_context(
                    st.session_state.prescription_system_prompt,
                    st.session_state.prescription_messages
                )
            st.markdown(reply)

        st.session_state.prescription_messages.append({"role": "assistant", "content": reply})
        st.rerun()

    st.markdown("---")

    if st.button("🔄 Explain a New Prescription"):
        st.session_state.prescription_messages = []
        st.session_state.prescription_system_prompt = ""
        st.rerun()