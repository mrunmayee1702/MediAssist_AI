import streamlit as st
from chatbot.groq_chat import chat_with_context, build_symptom_checker_system_prompt
from auth import get_user_by_username, build_profile_context


def render_symptom_checker_page():
    """
    Renders the Symptom Checker as a mini chat: the user describes
    symptoms, gets a structured urgency-based response, and can keep
    asking follow-up questions in the same conversation.
    """

    st.markdown("""
    <style>

    .symptom-header {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 0.3rem;
    }

    .symptom-icon {
        font-size: 2rem;
    }

    .symptom-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        color: #EAF2F5;
    }

    .symptom-subtitle {
        color: #8B95A8;
        font-size: 0.9rem;
        margin-bottom: 1.2rem;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='symptom-header'>
            <div class='symptom-icon'>🧭</div>
            <div class='symptom-title'>Symptom Checker</div>
        </div>
        <div class='symptom-subtitle'>
            Describe how you're feeling to get a general urgency level and
            information — not a diagnosis. You can keep asking follow-up
            questions afterwards.
        </div>
    """, unsafe_allow_html=True)

    if "symptom_messages" not in st.session_state:
        st.session_state.symptom_messages = []

    if "symptom_system_prompt" not in st.session_state:
        st.session_state.symptom_system_prompt = ""

    # -----------------------------------
    # Starting screen (no active check yet)
    # -----------------------------------

    if len(st.session_state.symptom_messages) == 0:

        symptoms = st.text_area(
            "Describe your symptoms",
            placeholder="e.g. I've had a fever and sore throat for 2 days, and I feel very tired.",
            height=120
        )

        if st.button("🔍 Check Symptoms", type="primary", use_container_width=True):

            if not symptoms.strip():
                st.warning("Please describe your symptoms first.")

            else:
                username = st.session_state.get("username")
                user = get_user_by_username(username)
                profile_context = build_profile_context(user)
                language = st.session_state.get("language", "English")

                system_prompt = build_symptom_checker_system_prompt(profile_context, language)
                st.session_state.symptom_system_prompt = system_prompt

                with st.spinner("Analyzing your symptoms..."):
                    first_reply = chat_with_context(
                        system_prompt,
                        [{"role": "user", "content": symptoms.strip()}]
                    )

                st.session_state.symptom_messages = [
                    {"role": "user", "content": symptoms.strip()},
                    {"role": "assistant", "content": first_reply}
                ]

                st.rerun()

        return

    # -----------------------------------
    # Active conversation
    # -----------------------------------

    for msg in st.session_state.symptom_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    follow_up = st.chat_input("Ask a follow-up question...")

    if follow_up:

        st.session_state.symptom_messages.append({"role": "user", "content": follow_up})

        with st.chat_message("user"):
            st.markdown(follow_up)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chat_with_context(
                    st.session_state.symptom_system_prompt,
                    st.session_state.symptom_messages
                )
            st.markdown(reply)

        st.session_state.symptom_messages.append({"role": "assistant", "content": reply})
        st.rerun()

    st.markdown("---")

    if st.button("🔄 New Symptom Check"):
        st.session_state.symptom_messages = []
        st.session_state.symptom_system_prompt = ""
        st.rerun()