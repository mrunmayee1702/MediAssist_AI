import streamlit as st
import time
import uuid
from rag.rag_chat import get_ai_response
from report_analysis.pdf_reader import extract_text_from_pdf
from report_analysis.medicine_identifier import identify_medicine
import speech_recognition as sr
from auth import init_db, build_profile_context, get_user_by_username
from login import render_login_page
from user_profile import render_profile_page
from symptom_checker import render_symptom_checker_page
from reminders import render_reminders_page
from report_page import render_report_analysis_page
from prescription_page import render_prescription_page


# ---------------------------------------
# Typing Animation Helper
# ---------------------------------------


def stream_words(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.025)




def transcribe_audio(audio_file):


    recognizer = sr.Recognizer()


    try:


        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)


        return recognizer.recognize_google(audio)


    except sr.UnknownValueError:
        return None


    except sr.RequestError:
        st.error("Speech recognition service unavailable.")
        return None


# ---------------------------------------
# Page Config
# ---------------------------------------


st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------
# Session State
# ---------------------------------------


if "messages" not in st.session_state:
    st.session_state.messages = []


if "report_analysis" not in st.session_state:
    st.session_state.report_analysis = ""


if "page" not in st.session_state:
    st.session_state.page = "chat"


if "medicine_result" not in st.session_state:
    st.session_state.medicine_result = ""


# history is a dict: {chat_id: {"id", "title", "messages": [...]}}
if "history" not in st.session_state:
    st.session_state.history = {}


# tracks which saved conversation the current chat belongs to (None = unsaved/new)
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if "username" not in st.session_state:
    st.session_state.username = None


if "user_profile" not in st.session_state:
    st.session_state.user_profile = None


if "language" not in st.session_state:
    st.session_state.language = "English"




# ---------------------------------------
# Login Gate
# ---------------------------------------


init_db()


if not st.session_state.logged_in:
    render_login_page()
    st.stop()




# ---------------------------------------
# Helpers: save + continue conversations
# ---------------------------------------


def save_current_chat():
    """Persist (create or update) the current conversation in history."""
    if not st.session_state.messages:
        return


    if st.session_state.current_chat_id is None:
        st.session_state.current_chat_id = str(uuid.uuid4())


    first_user_msg = next(
        (m["content"] for m in st.session_state.messages if m["role"] == "user"),
        "New Chat"
    )


    st.session_state.history[st.session_state.current_chat_id] = {
        "id": st.session_state.current_chat_id,
        "title": first_user_msg[:40],
        "messages": st.session_state.messages.copy()
    }




def ask_question(question):
    """Append the user's question, stream the AI's answer, and save the chat."""
    st.session_state.messages.append({"role": "user", "content": question})


    # Build patient profile context so the AI can personalize its answer
    user = get_user_by_username(st.session_state.username)
    profile_context = build_profile_context(user)
    language = st.session_state.get("language", "English")


    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_ai_response(question, profile_context, language)
        answer = st.write_stream(stream_words(answer))


    st.session_state.messages.append({"role": "assistant", "content": answer})


    save_current_chat()
    st.rerun()




# ---------------------------------------
# CSS
# ---------------------------------------


st.markdown("""
<style>


@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');


:root {


    --bg:          #05070C;
    --bg-2:        #090C14;
    --panel:       rgba(22, 27, 39, 0.55);
    --panel-2:     rgba(28, 34, 48, 0.55);
    --panel-solid: #12151f;
    --border:      rgba(255, 255, 255, 0.08);
    --border-glow: rgba(45, 212, 191, 0.45);
    --text:        #EAF2F5;
    --text-dim:    #8B95A8;
    --accent:      #2DD4BF;
    --accent-2:    #7C3AED;
    --accent-3:    #EC4899;
    --accent-soft: rgba(45, 212, 191, 0.14);
    --amber:       #FBBF24;
    --amber-soft:  rgba(251, 191, 36, 0.14);
}


html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text);
}


/* ---------------- Keyframes ---------------- */


@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}


@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}


@keyframes pulseRing {
    0%   { box-shadow: 0 0 0 0 rgba(45, 212, 191, 0.45); }
    70%  { box-shadow: 0 0 0 12px rgba(45, 212, 191, 0); }
    100% { box-shadow: 0 0 0 0 rgba(45, 212, 191, 0); }
}


@keyframes shimmerLine {
    0%   { background-position: -300px 0; }
    100% { background-position: 300px 0; }
}


@keyframes floatIcon {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50%      { transform: translateY(-4px) rotate(3deg); }
}


@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}


@keyframes auroraDrift {
    0%   { transform: translate(0px, 0px) scale(1); }
    33%  { transform: translate(30px, -40px) scale(1.1); }
    66%  { transform: translate(-25px, 25px) scale(0.95); }
    100% { transform: translate(0px, 0px) scale(1); }
}


@keyframes glowPulse {
    0%, 100% { opacity: 0.55; }
    50%      { opacity: 1; }
}


@keyframes borderTravel {
    0%   { background-position: 0% 0%; }
    100% { background-position: 200% 0%; }
}


@keyframes titleGlow {
    0%, 100% { filter: drop-shadow(0 0 6px rgba(45, 212, 191, 0.35)); }
    50%      { filter: drop-shadow(0 0 16px rgba(124, 58, 237, 0.45)); }
}


@keyframes sheen {
    0%   { transform: translateX(-120%) skewX(-15deg); }
    100% { transform: translateX(220%) skewX(-15deg); }
}


@keyframes spinRing {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}


@keyframes dotPulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.35; transform: scale(0.75); }
}


/* ---------------- Base surfaces ---------------- */


.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {
    background: var(--bg) !important;
}


/* Aurora background layer */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background:
        radial-gradient(600px 400px at 12% 8%, rgba(45, 212, 191, 0.16), transparent 60%),
        radial-gradient(700px 500px at 88% 15%, rgba(124, 58, 237, 0.16), transparent 60%),
        radial-gradient(650px 450px at 50% 95%, rgba(236, 72, 153, 0.10), transparent 60%);
    animation: auroraDrift 14s ease-in-out infinite;
}


[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 42px 42px;
    mask-image: radial-gradient(circle at 50% 0%, black, transparent 75%);
}


header[data-testid="stHeader"] {
    background: rgba(5, 7, 12, 0.6) !important;
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border);
}


[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {
    border-top: 1px solid var(--border);
    background: linear-gradient(180deg, transparent, rgba(5,7,12,0.9) 40%) !important;
}


.block-container {
    padding-top: 1.8rem;
    max-width: 900px;
    animation: fadeIn 0.6s ease both;
    position: relative;
    z-index: 1;
}


/* ---------------- Sidebar ---------------- */


section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(13, 16, 24, 0.97), rgba(9, 12, 20, 0.97));
    border-right: 1px solid var(--border);
    box-shadow: 4px 0 30px rgba(0,0,0,0.35);
}


section[data-testid="stSidebar"] .block-container {
    padding-top: 1.6rem;
    animation: fadeIn 0.5s ease both;
}


/* Hide Streamlit's auto-generated multipage nav (pages/ folder links) —
   only the custom sidebar buttons below should be visible. */
[data-testid="stSidebarNav"] {
    display: none !important;
}


.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.5rem;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3), var(--accent));
    background-size: 300% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: fadeInUp 0.5s ease both, gradientShift 6s linear infinite;
}


/* ---------------- Sidebar signature look ---------------- */


/* ---------------- Sidebar signature look ---------------- */


.sidebar-logo-wrap {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.2rem;
    animation: fadeInUp 0.5s ease both;
}


.sidebar-avatar-ring {
    width: 46px;
    height: 46px;
    min-width: 46px;
    border-radius: 50%;
    padding: 2px;
    background: conic-gradient(from 0deg, var(--accent), var(--accent-2), var(--accent-3), var(--amber), var(--accent));
    animation: spinRing 5s linear infinite;
    display: flex;
    align-items: center;
    justify-content: center;
}


.sidebar-avatar-inner {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: var(--panel-solid);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
}


.sidebar-brand-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 800;
    font-size: 1.2rem;
    line-height: 1.15;
    background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3), var(--accent));
    background-size: 300% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 4s ease infinite;
}


.sidebar-tagline {
    font-size: 0.7rem;
    color: var(--text-dim);
    letter-spacing: 0.02em;
}


.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--accent-soft);
    border: 1px solid rgba(45, 212, 191, 0.3);
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-size: 0.7rem;
    color: var(--accent);
    font-weight: 600;
    margin: 0.7rem 0 0.1rem 0;
    animation: fadeInUp 0.5s ease both;
    animation-delay: 0.08s;
}


.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--accent);
    animation: dotPulse 1.6s ease-in-out infinite;
}


.menu-label {
    font-size: 0.66rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-dim);
    font-weight: 700;
    margin: 1rem 0 0.4rem 0.3rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}


.menu-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}


/* ---- Nav rail buttons ---- */


section[data-testid="stSidebar"] .stButton>button {
    position: relative;
    border-radius: 10px !important;
    border: 1px solid transparent !important;
    padding-left: 0.9rem !important;
    margin-left: 4px;
    transition: background 0.18s ease, border-color 0.18s ease, transform 0.18s ease, box-shadow 0.25s ease;
}


/* colored glow chip that sits to the left of the button, outside it —
   this is the "highlighted" accent piece, brought back and reworked */
.nav-chip { position: relative; }
.nav-chip::before {
    content: "";
    position: absolute;
    left: -4px;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 60%;
    border-radius: 4px;
    background: var(--rail-color, var(--accent));
    opacity: 0.55;
    box-shadow: 0 0 10px 1px var(--rail-color, var(--accent));
    transition: opacity 0.2s ease, height 0.2s ease, box-shadow 0.2s ease;
}
.nav-chip:hover::before { opacity: 1; height: 72%; }


.nav-rail-new_chat        { --rail-color: var(--accent); }
.nav-rail-history         { --rail-color: var(--accent-3); }
.nav-rail-report          { --rail-color: var(--amber); }
.nav-rail-medicine        { --rail-color: #F87171; }
.nav-rail-prescription    { --rail-color: var(--accent-2); }
.nav-rail-symptom_checker { --rail-color: #38BDF8; }
.nav-rail-reminders       { --rail-color: #FB7185; }
.nav-rail-profile         { --rail-color: #A78BFA; }


.nav-chip button {
    background: color-mix(in srgb, var(--rail-color) 8%, var(--panel-2)) !important;
    border-color: color-mix(in srgb, var(--rail-color) 18%, transparent) !important;
}
.nav-chip button:hover {
    background: color-mix(in srgb, var(--rail-color) 16%, var(--panel-2)) !important;
    border-color: color-mix(in srgb, var(--rail-color) 45%, transparent) !important;
    transform: translateX(3px);
}


/* Active page: full glow treatment — this is the attractive highlight */
.nav-chip.nav-rail-active::before {
    opacity: 1;
    height: 80%;
    box-shadow: 0 0 16px 3px var(--rail-color, var(--accent));
    animation: dotPulse 1.8s ease-in-out infinite;
}
.nav-chip.nav-rail-active button {
    background: color-mix(in srgb, var(--rail-color) 22%, var(--panel-2)) !important;
    border-color: color-mix(in srgb, var(--rail-color) 60%, transparent) !important;
    color: #fff !important;
    font-weight: 700 !important;
    box-shadow: 0 0 20px -4px var(--rail-color, var(--accent)), inset 0 0 0 1px rgba(255,255,255,0.08);
}
/* ---------------- Headings / text ---------------- */


h1, h2, h3 {
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    animation: fadeInUp 0.5s ease both;
}


h1 {
    background: linear-gradient(90deg, #ffffff 20%, var(--accent) 55%, var(--accent-2) 80%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: fadeInUp 0.5s ease both, gradientShift 5s ease infinite, titleGlow 3.5s ease-in-out infinite;
    text-align: left !important;
    margin: 0 0 0.2rem 0 !important;
    letter-spacing: -0.01em;
}


/* AI-generated markdown output (chat bubbles, symptom checker, report
   analysis, prescription explainer) uses ### (h3) headings on purpose
   so it doesn't get the big glowing h1 treatment above — keeps it
   looking clean/professional. */
[data-testid="stChatMessageContent"] h3 {
    font-size: 1.05rem !important;
    margin-top: 0.9rem !important;
    margin-bottom: 0.3rem !important;
}


[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stMarkdownContainer"],
[data-testid="stCaptionContainer"] {
    color: var(--text) !important;
}


.subtitle-caption {
    color: var(--text-dim) !important;
    animation: fadeInUp 0.6s ease both;
    animation-delay: 0.05s;
    text-align: left !important;
    margin: 0;
    font-size: 0.95rem;
    letter-spacing: 0.01em;
}


[data-testid="stHeadingWithActionElements"] {
    text-align: left !important;
    justify-content: flex-start !important;
}


/* ---------------- Buttons ---------------- */


.stButton>button {
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    width: 100%;
    background: var(--panel-2);
    backdrop-filter: blur(14px);
    border: 1px solid var(--border);
    color: var(--text);
    font-weight: 500;
    padding: 0.65rem 1rem;
    transition: transform 0.18s ease, box-shadow 0.25s ease, border-color 0.2s ease, background 0.2s ease;
}


.stButton>button::after {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 40%; height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.12), transparent);
    transform: translateX(-120%) skewX(-15deg);
}


.stButton>button:hover::after {
    animation: sheen 0.9s ease forwards;
}


.stButton>button:hover {
    border-color: var(--accent);
    background: var(--accent-soft);
    color: var(--accent);
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(45, 212, 191, 0.2), 0 0 0 1px rgba(45, 212, 191, 0.25) inset;
}


.stButton>button:active {
    transform: translateY(0px) scale(0.97);
}


section[data-testid="stSidebar"] .stButton>button {
    text-align: left;
    background: transparent;
    border: none;
    border-left: 2px solid transparent;
    border-radius: 8px;
}


section[data-testid="stSidebar"] .stButton>button:hover {
    border-left: 2px solid var(--accent);
    background: var(--accent-soft);
    transform: translateX(4px);
    box-shadow: none;
}


.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    background-size: 200% auto;
    border: none;
    color: #06110F;
    font-weight: 700;
    box-shadow: 0 8px 24px rgba(124, 58, 237, 0.25);
}


.stButton>button[kind="primary"]:hover {
    animation: pulseRing 1.4s ease infinite, gradientShift 2.5s ease infinite;
    filter: brightness(1.08);
    transform: translateY(-3px);
}


/* Suggested-question buttons: staggered entrance */
div[data-testid="column"] .stButton {
    animation: fadeInUp 0.5s ease both;
}


div[data-testid="column"]:nth-of-type(1) .stButton:nth-of-type(1) { animation-delay: 0.05s; }
div[data-testid="column"]:nth-of-type(1) .stButton:nth-of-type(2) { animation-delay: 0.15s; }
div[data-testid="column"]:nth-of-type(2) .stButton:nth-of-type(1) { animation-delay: 0.10s; }
div[data-testid="column"]:nth-of-type(2) .stButton:nth-of-type(2) { animation-delay: 0.20s; }


/* ---------------- Chat ---------------- */


.stChatMessage {
    border-radius: 16px;
    border: 1px solid var(--border);
    background: var(--panel-2);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 0.6rem 0.5rem;
    margin-bottom: 0.7rem;
    box-shadow: 0 6px 22px rgba(0, 0, 0, 0.25);
    animation: fadeInUp 0.4s ease both;
    transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
}


.stChatMessage:hover {
    border-color: var(--border-glow);
    box-shadow: 0 10px 30px rgba(45, 212, 191, 0.12);
    transform: translateY(-1px);
}


[data-testid="stChatMessage"] p,
[data-testid="stChatMessageContent"] p {
    color: var(--text) !important;
    line-height: 1.6;
}


[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, var(--amber), #f97316) !important;
    box-shadow: 0 0 14px rgba(251, 191, 36, 0.45);
    transition: transform 0.2s ease;
}


[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
    box-shadow: 0 0 14px rgba(45, 212, 191, 0.45);
    animation: floatIcon 3s ease-in-out infinite;
}


[data-testid="stChatInput"] {
    border-radius: 16px;
    border: 1px solid var(--border);
    background: var(--panel-2);
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}


[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent);
    box-shadow: 0 0 0 4px var(--accent-soft), 0 0 20px rgba(45, 212, 191, 0.25);
}


/* ---------------- File uploader ---------------- */


[data-testid="stFileUploader"] {
    border-radius: 14px;
    padding: 0.6rem;
    background: var(--panel-2);
    backdrop-filter: blur(14px);
    border: 1.5px dashed rgba(45, 212, 191, 0.35);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}


[data-testid="stFileUploader"]:hover {
    border-color: var(--accent);
    box-shadow: 0 0 24px rgba(45, 212, 191, 0.15);
}


/* ---------------- Expander ---------------- */


.streamlit-expanderHeader {
    border-radius: 12px !important;
    background: var(--panel-2) !important;
    border: 1px solid var(--border) !important;
    backdrop-filter: blur(14px);
}


/* ---------------- Text area ---------------- */


textarea {
    background: var(--panel-2) !important;
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    backdrop-filter: blur(14px);
}


/* ---------------- Alerts ---------------- */


[data-testid="stAlert"] {
    border-radius: 12px;
    background: var(--accent-soft) !important;
    border: 1px solid rgba(45, 212, 191, 0.3);
    color: var(--text) !important;
    animation: fadeInUp 0.4s ease both;
    box-shadow: 0 0 20px rgba(45, 212, 191, 0.12);
}


/* ---------------- Spinner ---------------- */


[data-testid="stSpinner"] * {
    color: var(--accent) !important;
}


/* ---------------- Divider: animated shimmer line ---------------- */


hr {
    border: none;
    height: 2px;
    margin: 1.6rem 0;
    background: linear-gradient(90deg, transparent, var(--accent), var(--accent-2), var(--accent-3), transparent);
    background-size: 400px 2px;
    background-repeat: no-repeat;
    animation: shimmerLine 3.5s ease-in-out infinite;
    opacity: 0.8;
}


/* ---------------- Scrollbar ---------------- */


::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
    border-radius: 10px;
}


/* ---------------- Welcome screen ---------------- */


.welcome-heading {
    text-align: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.9rem;
    background: linear-gradient(90deg, var(--text), var(--accent), var(--accent-2), var(--text));
    background-size: 300% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-top: 0.8rem;
    animation: fadeInUp 0.5s ease both, gradientShift 6s linear infinite;
}


.suggested-label {
    color: var(--text-dim);
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 0.78rem;
    margin: 1.3rem 0 0.7rem 0;
    animation: fadeInUp 0.5s ease both;
    position: relative;
    padding-left: 1.1rem;
}


.suggested-label::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 10px 2px rgba(45, 212, 191, 0.7);
    transform: translateY(-50%);
    animation: glowPulse 1.8s ease-in-out infinite;
}


.version-tag {
    color: var(--text-dim);
    font-size: 0.75rem;
    opacity: 0.7;
    letter-spacing: 0.03em;
}


/* ---------------- ECG signature divider ---------------- */


.ecg-wrap {
    width: 100%;
    height: 30px;
    margin: 8px 0 20px 0;
    overflow: hidden;
    opacity: 0.9;
}


.ecg-wrap svg {
    width: 100%;
    height: 100%;
    display: block;
}


.ecg-base {
    stroke: rgba(255, 255, 255, 0.09);
}


.ecg-pulse {
    stroke: url(#ecgGrad);
    stroke-dasharray: 90 900;
    animation: ecgMove 3.4s linear infinite;
    filter: drop-shadow(0 0 5px rgba(45, 212, 191, 0.55));
}


@keyframes ecgMove {
    from { stroke-dashoffset: 900; }
    to   { stroke-dashoffset: -900; }
}


/* ---------------- Audio input (mic) ---------------- */


[data-testid="stAudioInput"] {
    border-radius: 14px;
    padding: 0.6rem;
    background: var(--panel-2);
    backdrop-filter: blur(14px);
    border: 1.5px dashed rgba(124, 58, 237, 0.35);
}


[data-testid="stAudioInput"]:hover {
    border-color: var(--accent-2);
    box-shadow: 0 0 20px rgba(124, 58, 237, 0.2);
}


</style>
""", unsafe_allow_html=True)


# ---------------------------------------
# Sidebar
# ---------------------------------------


with st.sidebar:


    st.markdown("""
        <div class='sidebar-logo-wrap'>
            <div class='sidebar-avatar-ring'>
                <div class='sidebar-avatar-inner'>🩺</div>
            </div>
            <div>
                <div class='sidebar-brand-title'>MediAssist AI</div>
                <div class='sidebar-tagline'>Your Health Companion</div>
            </div>
        </div>
        <div class='status-pill'><span class='status-dot'></span>AI Assistant Online</div>
    """, unsafe_allow_html=True)


    st.markdown("---")


    nav_items = [
        ("✦ New Chat", "chat", "sidebar_new_chat"),
        ("🕘 History", "history", "sidebar_history"),
    ]


    tools_items = [
        ("🧾 Report Analysis", "report", "sidebar_report"),
        ("💊 Medicine Identifier", "medicine", "sidebar_medicine"),
        ("🗂️ Prescription Explainer", "prescription", "sidebar_prescription"),
        ("🩻 Symptom Checker", "symptom_checker", "sidebar_symptom_checker"),
        ("⏰ Reminders", "reminders", "sidebar_reminders"),
    ]


    account_items = [
        ("🪪 Profile", "profile", "sidebar_profile"),
    ]


    def render_nav_button(label, target_page, key):
        is_active = st.session_state.page == target_page
        rail = f"nav-rail-{key.replace('sidebar_', '')}"
        css_class = f"nav-chip {rail}" + (" nav-rail-active" if is_active else "")
        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        clicked = st.button(label, key=key, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if clicked:
            if target_page == "chat":
                st.session_state.messages = []
                st.session_state.current_chat_id = None
                st.session_state.report_analysis = ""
            st.session_state.page = target_page
            st.rerun()


    st.markdown("<div class='menu-label'>Conversation</div>", unsafe_allow_html=True)
    for label, target_page, key in nav_items:
        render_nav_button(label, target_page, key)


    st.markdown("<div class='menu-label'>Health Tools</div>", unsafe_allow_html=True)
    for label, target_page, key in tools_items:
        render_nav_button(label, target_page, key)


    st.markdown("<div class='menu-label'>Account</div>", unsafe_allow_html=True)
    for label, target_page, key in account_items:
        render_nav_button(label, target_page, key)


# ---------------------------------------
# Header
# ---------------------------------------


st.title("🩺 MediAssist AI")


st.markdown("<div class='subtitle-caption'>AI Medical Report Analysis &amp; Health Guidance</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="ecg-wrap">
    <svg viewBox="0 0 800 40" preserveAspectRatio="none">
        <defs>
            <linearGradient id="ecgGrad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0"/>
                <stop offset="50%" stop-color="#2DD4BF" stop-opacity="1"/>
                <stop offset="100%" stop-color="#7C3AED" stop-opacity="0"/>
            </linearGradient>
        </defs>
        <path class="ecg-base" fill="none" stroke-width="2"
            d="M0,20 L40,20 L48,20 L56,6 L64,34 L72,14 L80,20 L120,20 L128,16 L136,20 L160,20 L200,20 L208,20 L216,6 L224,34 L232,14 L240,20 L280,20 L288,16 L296,20 L320,20 L360,20 L368,20 L376,6 L384,34 L392,14 L400,20 L440,20 L448,16 L456,20 L480,20 L520,20 L528,20 L536,6 L544,34 L552,14 L560,20 L600,20 L608,16 L616,20 L640,20 L680,20 L688,20 L696,6 L704,34 L712,14 L720,20 L760,20 L768,16 L776,20 L800,20"/>
        <path class="ecg-pulse" fill="none" stroke-width="2.4"
            d="M0,20 L40,20 L48,20 L56,6 L64,34 L72,14 L80,20 L120,20 L128,16 L136,20 L160,20 L200,20 L208,20 L216,6 L224,34 L232,14 L240,20 L280,20 L288,16 L296,20 L320,20 L360,20 L368,20 L376,6 L384,34 L392,14 L400,20 L440,20 L448,16 L456,20 L480,20 L520,20 L528,20 L536,6 L544,34 L552,14 L560,20 L600,20 L608,16 L616,20 L640,20 L680,20 L688,20 L696,6 L704,34 L712,14 L720,20 L760,20 L768,16 L776,20 L800,20"/>
    </svg>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------
# Report Analysis Page
# ---------------------------------------
if st.session_state.page == "report":


    render_report_analysis_page(report_text)




# ---------------------------------------
# Medicine Identifier Page
# ---------------------------------------


if st.session_state.page == "medicine":


    st.subheader("💊 Medicine Identifier")
    st.caption("Upload a clear photo of the medicine strip, box, label, or pill.")


    medicine_image = st.file_uploader(
        "Upload Medicine Image",
        type=["jpg", "jpeg", "png"],
        key="medicine_image_uploader"
    )


    if medicine_image:
        st.image(medicine_image, caption="Uploaded Image", width=300)


    if st.button("🔍 Identify Medicine", type="primary"):


        if medicine_image is None:
            st.warning("Please upload an image first.")
        else:
            with st.spinner("Analyzing Medicine Image..."):
                st.session_state.medicine_result = identify_medicine(medicine_image)


    if st.session_state.medicine_result != "":


        st.markdown("---")
        st.markdown(st.session_state.medicine_result)
        st.markdown("---")




# ---------------------------------------
# Prescription Explainer Page
# ---------------------------------------


if st.session_state.page == "prescription":


    render_prescription_page()




# ---------------------------------------
# Symptom Checker Page
# ---------------------------------------


if st.session_state.page == "symptom_checker":


    render_symptom_checker_page()




# ---------------------------------------
# Reminders Page
# ---------------------------------------


if st.session_state.page == "reminders":


    render_reminders_page()




# ---------------------------------------
# Chat Page
# ---------------------------------------


if st.session_state.page == "chat":


    # -----------------------------------
    # Welcome Screen
    # -----------------------------------


    if len(st.session_state.messages) == 0:


        st.markdown(
            "<div class='welcome-heading'>How can I help you today?</div>",
            unsafe_allow_html=True
        )


    st.write("")


    st.markdown(
        "<div class='suggested-label'>💡 Suggested Questions</div>",
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:


        if st.button("🩸 Explain CBC Report"):
            ask_question("Explain CBC Report")


        if st.button("🩺 What is Diabetes?"):
            ask_question("What is Diabetes?")


    with col2:


        if st.button("🧪 What is Creatinine?"):
            ask_question("What is Creatinine?")


        if st.button("🦟 Symptoms of Dengue?"):
            ask_question("Symptoms of Dengue")


    # -----------------------------------
    # Chat History
    # -----------------------------------


    for message in st.session_state.messages:


        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # -----------------------------------
    # Voice Input
    # -----------------------------------


    if "mic_key_counter" not in st.session_state:
        st.session_state.mic_key_counter = 0


    st.markdown(
        "<div class='suggested-label'>🎤 Ask By Voice</div>",
        unsafe_allow_html=True
    )


    audio = st.audio_input(
        "Speak",
        key=f"mic_{st.session_state.mic_key_counter}"
    )


    if audio:


        with st.spinner("🎧 Listening..."):
            voice = transcribe_audio(audio)


        if voice:


            st.session_state.mic_key_counter += 1


            with st.chat_message("user"):
                st.markdown(voice)


            ask_question(voice)


        else:
            st.warning("Couldn't understand your voice.")


    # -----------------------------------
    # Chat Input
    # -----------------------------------


    prompt = st.chat_input("Ask a medical question...")


    if prompt:


        with st.chat_message("user"):
            st.markdown(prompt)


        ask_question(prompt)




# ---------------------------------------
# History Page
# ---------------------------------------


if st.session_state.page == "history":


    st.header("🕘 Chat History")


    if len(st.session_state.history) == 0:
        st.info("No chat history available.")


    else:


        # newest conversations first
        for chat_id in reversed(list(st.session_state.history.keys())):


            chat = st.session_state.history[chat_id]


            with st.expander(f"💬 {chat['title']}"):


                for msg in chat["messages"]:
                    role_label = "👤 You" if msg["role"] == "user" else "🤖 MediAssist AI"
                    st.markdown(f"**{role_label}:**")
                    st.write(msg["content"])


                col1, col2 = st.columns(2)


                with col1:
                    if st.button("▶️ Continue Chat", key=f"continue_{chat_id}", use_container_width=True):
                        st.session_state.messages = chat["messages"].copy()
                        st.session_state.current_chat_id = chat_id
                        st.session_state.page = "chat"
                        st.rerun()


                with col2:
                    if st.button("🗑️ Delete", key=f"delete_history_{chat_id}", use_container_width=True):
                        del st.session_state.history[chat_id]
                        if st.session_state.current_chat_id == chat_id:
                            st.session_state.messages = []
                            st.session_state.current_chat_id = None
                        st.rerun()




# ---------------------------------------
# Profile Page
# ---------------------------------------


if st.session_state.page == "profile":


    render_profile_page()

