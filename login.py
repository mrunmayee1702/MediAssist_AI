import streamlit as st
from auth import create_user, verify_login


def render_login_page():
    """
    Renders the login / signup screen.
    Sets st.session_state.logged_in, username, and user_profile on success.
    """

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --bg:          #05070C;
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
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ---------------- Keyframes ---------------- */

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes auroraDrift {
        0%   { transform: translate(0px, 0px) scale(1); }
        33%  { transform: translate(30px, -40px) scale(1.1); }
        66%  { transform: translate(-25px, 25px) scale(0.95); }
        100% { transform: translate(0px, 0px) scale(1); }
    }

    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes titleGlow {
        0%, 100% { filter: drop-shadow(0 0 6px rgba(45, 212, 191, 0.35)); }
        50%      { filter: drop-shadow(0 0 16px rgba(124, 58, 237, 0.45)); }
    }

    @keyframes spinRing {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
    }

    @keyframes sheen {
        0%   { transform: translateX(-120%) skewX(-15deg); }
        100% { transform: translateX(220%) skewX(-15deg); }
    }

    /* ---------------- Base surface + aurora ---------------- */

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: var(--bg) !important;
    }

    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background:
            radial-gradient(600px 400px at 15% 10%, rgba(45, 212, 191, 0.16), transparent 60%),
            radial-gradient(700px 500px at 85% 20%, rgba(124, 58, 237, 0.16), transparent 60%),
            radial-gradient(650px 450px at 50% 100%, rgba(236, 72, 153, 0.10), transparent 60%);
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
    }

    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stMarkdownContainer"] {
        color: var(--text) !important;
    }

    .block-container {
        position: relative;
        z-index: 1;
        padding-top: 3rem;
    }

    /* ---------------- Hero ---------------- */

    .login-avatar-ring {
        width: 64px;
        height: 64px;
        margin: 0 auto 0.9rem auto;
        border-radius: 50%;
        padding: 3px;
        background: conic-gradient(from 0deg, var(--accent), var(--accent-2), var(--accent-3), var(--amber), var(--accent));
        animation: spinRing 6s linear infinite;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .login-avatar-inner {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: var(--panel-solid);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.7rem;
    }

    .login-title {
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 2rem;
        background: linear-gradient(90deg, #ffffff 20%, var(--accent) 55%, var(--accent-2) 80%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: gradientShift 5s ease infinite, titleGlow 3.5s ease-in-out infinite, fadeInUp 0.6s ease both;
        margin-bottom: 0.2rem;
    }

    .login-subtitle {
        text-align: center;
        color: var(--text-dim) !important;
        font-size: 0.95rem;
        margin-bottom: 1.6rem;
        animation: fadeInUp 0.6s ease both;
        animation-delay: 0.05s;
    }

    /* ---------------- Card ---------------- */

    .st-key-login_card {
        background: var(--panel-2);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.2rem 2rem 1.6rem 2rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
        animation: fadeInUp 0.6s ease both;
        animation-delay: 0.1s;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    .st-key-login_card:hover {
        border-color: var(--border-glow);
        box-shadow: 0 20px 60px rgba(45, 212, 191, 0.12);
    }

    /* ---------------- Tabs ---------------- */

    div[data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid var(--border);
    }

    div[data-baseweb="tab-highlight"] {
        display: none;
    }

    div[data-baseweb="tab-border"] {
        display: none;
    }

    button[data-baseweb="tab"] {
        border-radius: 9px;
        color: var(--text-dim);
        font-weight: 600;
        transition: all 0.25s ease;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        color: #06110F !important;
    }

    button[data-baseweb="tab"] p {
        color: inherit !important;
    }

    /* ---------------- Inputs ---------------- */

    div[data-testid="stTextInput"] input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 10px !important;
        padding: 0.6rem 0.8rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-soft) !important;
    }

    div[data-testid="stTextInput"] label p {
        color: var(--text-dim) !important;
        font-size: 0.82rem !important;
        font-weight: 600;
    }

    /* ---------------- Buttons ---------------- */

    .stButton > button {
        position: relative;
        overflow: hidden;
        width: 100%;
        border-radius: 10px;
        font-weight: 700;
        padding: 0.65rem 1rem;
        margin-top: 0.5rem;
        transition: transform 0.18s ease, box-shadow 0.25s ease, filter 0.2s ease;
    }

    .stButton > button::after {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 40%; height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255,255,255,0.25), transparent);
        transform: translateX(-120%) skewX(-15deg);
    }

    .stButton > button:hover::after {
        animation: sheen 0.9s ease forwards;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        background-size: 200% auto;
        border: none;
        color: #06110F !important;
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.25);
    }

    .stButton > button[kind="primary"]:hover {
        filter: brightness(1.08);
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(45, 212, 191, 0.3);
    }

    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }

    /* ---------------- Alerts ---------------- */

    [data-testid="stAlert"] {
        border-radius: 10px;
        animation: fadeInUp 0.4s ease both;
    }

    /* ---------------- Footer ---------------- */

    .login-footer {
        text-align: center;
        color: var(--text-dim);
        font-size: 0.72rem;
        opacity: 0.6;
        margin-top: 1.4rem;
        letter-spacing: 0.03em;
    }

    </style>
    """, unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 1.3, 1])

    with center_col:

        login_card = st.container(key="login_card")

        with login_card:

            st.markdown("""
                <div class='login-avatar-ring'>
                    <div class='login-avatar-inner'>🩺</div>
                </div>
                <div class='login-title'>MediAssist AI</div>
                <div class='login-subtitle'>Sign in to continue to your health assistant</div>
            """, unsafe_allow_html=True)

            tab_login, tab_signup = st.tabs(["🔑 Login", "🆕 Sign Up"])

            # -----------------------------
            # Login tab
            # -----------------------------
            with tab_login:

                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")

                if st.button("Login", type="primary", use_container_width=True, key="login_btn"):

                    if not username or not password:
                        st.warning("Please enter both username and password.")

                    else:
                        success, user = verify_login(username, password)

                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = user["username"]
                            st.session_state.user_profile = user
                            st.rerun()

                        else:
                            st.error("Invalid username or password.")

            # -----------------------------
            # Sign up tab
            # -----------------------------
            with tab_signup:

                new_username = st.text_input("Choose a Username", key="signup_username")
                new_email = st.text_input("Email (optional)", key="signup_email")
                new_password = st.text_input("Choose a Password", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")

                if st.button("Create Account", type="primary", use_container_width=True, key="signup_btn"):

                    if not new_username or not new_password:
                        st.warning("Username and password are required.")

                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")

                    elif len(new_password) < 6:
                        st.warning("Password should be at least 6 characters.")

                    else:
                        success, message = create_user(new_username, new_password, new_email)

                        if success:
                            st.success(message + " Please login using the Login tab.")
                        else:
                            st.error(message)

        st.markdown(
            "<div class='login-footer'>MediAssist AI · Secure Health Companion</div>",
            unsafe_allow_html=True
        )