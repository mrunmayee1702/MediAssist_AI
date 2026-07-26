import streamlit as st
from auth import update_profile, change_password, get_user_by_username


def render_profile_page():
    """
    Renders the user profile page: personal info form, medical info,
    privacy/password settings, and logout. Reads/writes data via auth.py (SQLite).
    """

    st.markdown("""
    <style>

    .profile-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .profile-avatar {
        width: 64px;
        height: 64px;
        min-width: 64px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2DD4BF, #7C3AED);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        box-shadow: 0 0 20px rgba(45, 212, 191, 0.35);
    }

    .profile-name {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.3rem;
        color: #EAF2F5;
    }

    .profile-username {
        color: #8B95A8;
        font-size: 0.85rem;
    }

    .section-label {
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #8B95A8;
        font-weight: 700;
        margin: 0.8rem 0 0.6rem 0;
    }

    </style>
    """, unsafe_allow_html=True)

    username = st.session_state.get("username")
    user = get_user_by_username(username)

    if user is None:
        st.error("Profile could not be loaded. Please log in again.")
        return

    # -----------------------------------
    # Header
    # -----------------------------------

    st.markdown(f"""
        <div class='profile-header'>
            <div class='profile-avatar'>👤</div>
            <div>
                <div class='profile-name'>{user.get("full_name") or username}</div>
                <div class='profile-username'>@{username}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # -----------------------------------
    # Personal information form
    # -----------------------------------

    st.markdown("<div class='section-label'>📝 Personal Information</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    gender_options = ["", "Male", "Female", "Other", "Prefer not to say"]
    blood_group_options = ["", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

    current_gender = user.get("gender") or ""
    current_blood_group = user.get("blood_group") or ""

    with col1:

        full_name = st.text_input("👤 Full Name", value=user.get("full_name") or "")

        age = st.number_input(
            "🎂 Age",
            min_value=0,
            max_value=120,
            value=int(user.get("age") or 0)
        )

        height = st.text_input("📏 Height (e.g. 170 cm)", value=user.get("height") or "")

        blood_group = st.selectbox(
            "🩸 Blood Group",
            blood_group_options,
            index=blood_group_options.index(current_blood_group) if current_blood_group in blood_group_options else 0
        )

        emergency_contact = st.text_input("📞 Emergency Contact", value=user.get("emergency_contact") or "")

    with col2:

        email = st.text_input("📧 Email ID", value=user.get("email") or "")

        gender = st.selectbox(
            "⚧ Gender",
            gender_options,
            index=gender_options.index(current_gender) if current_gender in gender_options else 0
        )

        weight = st.text_input("⚖️ Weight (e.g. 65 kg)", value=user.get("weight") or "")

        location = st.text_input("🌍 Location (Optional)", value=user.get("location") or "")

    st.markdown("<div class='section-label'>🩹 Medical Information</div>", unsafe_allow_html=True)
    st.caption("This helps MediAssist AI give you more relevant, personalized answers. It is never shared and never used to prescribe medicines.")

    med_col1, med_col2 = st.columns(2)

    with med_col1:
        medical_conditions = st.text_area(
            "🩹 Known Medical Conditions",
            value=user.get("medical_conditions") or "",
            placeholder="e.g. Diabetes, High Blood Pressure, Asthma",
            height=90
        )

    with med_col2:
        allergies = st.text_area(
            "🌿 Allergies",
            value=user.get("allergies") or "",
            placeholder="e.g. Penicillin, Peanuts, Dust",
            height=90
        )

    if st.button("💾 Save Profile", type="primary", use_container_width=True):

        update_profile(username, {
            "full_name": full_name,
            "email": email,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "blood_group": blood_group,
            "location": location,
            "emergency_contact": emergency_contact,
            "medical_conditions": medical_conditions,
            "allergies": allergies,
        })

        st.session_state.user_profile = get_user_by_username(username)
        st.success("✅ Profile updated successfully.")
        st.rerun()

    st.markdown("---")

    # -----------------------------------
    # Privacy & Data Settings (password change)
    # -----------------------------------

    with st.expander("🔒 Privacy & Data Settings"):

        st.markdown("**Change Password**")

        old_password = st.text_input("Current Password", type="password", key="profile_old_pwd")
        new_password = st.text_input("New Password", type="password", key="profile_new_pwd")
        confirm_new_password = st.text_input("Confirm New Password", type="password", key="profile_confirm_new_pwd")

        if st.button("Update Password", key="profile_update_pwd_btn"):

            if not old_password or not new_password:
                st.warning("Please fill in all password fields.")

            elif new_password != confirm_new_password:
                st.error("New passwords do not match.")

            elif len(new_password) < 6:
                st.warning("New password should be at least 6 characters.")

            else:
                success, message = change_password(username, old_password, new_password)

                if success:
                    st.success(message)
                else:
                    st.error(message)

    st.markdown("---")

    # -----------------------------------
    # Logout
    # -----------------------------------

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_profile = None
        st.session_state.messages = []
        st.session_state.history = {}
        st.session_state.current_chat_id = None
        st.session_state.page = "chat"
        st.rerun()