import streamlit as st
from datetime import date, time as dtime
from auth import add_reminder, get_reminders, delete_reminder, toggle_reminder_done


def render_reminders_page():
    """
    Renders the Reminders page: add a reminder (medicine, appointment,
    or lifestyle), see upcoming/past reminders, mark done, or delete.
    These are in-app reminders only (no push notifications).
    """

    st.markdown("""
    <style>

    .reminders-header {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 0.3rem;
    }

    .reminders-icon {
        font-size: 2rem;
    }

    .reminders-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        color: #EAF2F5;
    }

    .reminders-subtitle {
        color: #8B95A8;
        font-size: 0.9rem;
        margin-bottom: 1.2rem;
    }

    .reminder-card {
        background: rgba(28, 34, 48, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.7rem;
    }

    .reminder-card.done {
        opacity: 0.55;
    }

    .reminder-title {
        font-weight: 700;
        color: #EAF2F5;
        font-size: 1rem;
    }

    .reminder-meta {
        color: #8B95A8;
        font-size: 0.8rem;
        margin-top: 0.15rem;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='reminders-header'>
            <div class='reminders-icon'>⏰</div>
            <div class='reminders-title'>Reminders</div>
        </div>
        <div class='reminders-subtitle'>
            Keep track of medicines, appointments, or healthy habits.
            (These show up here in the app — they don't send push
            notifications outside of it.)
        </div>
    """, unsafe_allow_html=True)

    username = st.session_state.get("username")

    # -----------------------------------
    # Add new reminder
    # -----------------------------------

    with st.expander("➕ Add a New Reminder", expanded=False):

        title = st.text_input("Title", placeholder="e.g. Take Metformin, Doctor Appointment")

        reminder_type = st.selectbox(
            "Type",
            ["💊 Medicine", "🩺 Appointment", "🧘 Lifestyle / Habit"]
        )

        col1, col2 = st.columns(2)

        with col1:
            reminder_date = st.date_input("Date", value=date.today())

        with col2:
            reminder_time = st.time_input("Time", value=dtime(hour=9, minute=0))

        notes = st.text_area("Notes (optional)", height=70)

        if st.button("Save Reminder", type="primary", use_container_width=True):

            if not title.strip():
                st.warning("Please enter a title for the reminder.")

            else:
                add_reminder(
                    username,
                    title.strip(),
                    reminder_type,
                    reminder_date,
                    reminder_time,
                    notes.strip()
                )

                st.success("✅ Reminder added.")
                st.rerun()

    st.markdown("---")

    # -----------------------------------
    # List reminders
    # -----------------------------------

    reminders = get_reminders(username)

    if len(reminders) == 0:
        st.info("No reminders yet. Add one above.")
        return

    pending = [r for r in reminders if not r["is_done"]]
    completed = [r for r in reminders if r["is_done"]]

    st.markdown("<div class='section-label'>📋 Upcoming</div>", unsafe_allow_html=True)

    if len(pending) == 0:
        st.caption("Nothing pending. 🎉")

    for r in pending:
        _render_reminder_card(r)

    if len(completed) > 0:

        st.markdown("---")
        st.markdown("<div class='section-label'>✅ Completed</div>", unsafe_allow_html=True)

        for r in completed:
            _render_reminder_card(r)


def _render_reminder_card(r):
    """Renders a single reminder card with mark-done and delete controls."""

    card_class = "reminder-card done" if r["is_done"] else "reminder-card"

    st.markdown(f"""
        <div class='{card_class}'>
            <div class='reminder-title'>{r["title"]}</div>
            <div class='reminder-meta'>{r["reminder_type"]} • {r["reminder_date"]} at {r["reminder_time"]}</div>
        </div>
    """, unsafe_allow_html=True)

    if r.get("notes"):
        st.caption(r["notes"])

    col1, col2 = st.columns(2)

    with col1:
        label = "↩️ Mark Pending" if r["is_done"] else "✅ Mark Done"

        if st.button(label, key=f"toggle_{r['id']}", use_container_width=True):
            toggle_reminder_done(r["id"], not r["is_done"])
            st.rerun()

    with col2:
        if st.button("🗑️ Delete", key=f"delete_reminder_{r['id']}", use_container_width=True):
            delete_reminder(r["id"])
            st.rerun()