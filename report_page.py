import streamlit as st
from datetime import datetime
from report_analysis.pdf_reader import extract_text_from_pdf
from report_analysis.analyzer import (
    build_report_analysis_system_prompt,
    build_report_comparison_system_prompt,
)
from chatbot.groq_chat import chat_with_context
from auth import get_user_by_username, build_profile_context
from report_pdf import strip_emoji_for_display, generate_report_pdf


def render_report_analysis_page(report_text):
    """
    Renders the Report Analysis page: analyze the uploaded report (or
    compare it with a previous one) in a clean, professional report
    card, let the user download it as a PDF, and continue asking
    follow-up questions about it below.

    `report_text` is the text already extracted from the sidebar upload.
    """

    st.markdown("""
    <style>

    .st-key-report_analysis_card {
        background: rgba(28, 34, 48, 0.55);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        padding: 1.6rem 1.8rem 1.2rem 1.8rem;
        box-shadow: 0 6px 22px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1rem;
    }

    .report-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.6rem;
        margin-bottom: 0.8rem;
    }

    .report-card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        color: #2DD4BF !important;
    }

    .report-card-meta {
        font-size: 0.78rem;
        color: #8B95A8 !important;
        text-align: right;
    }

    .st-key-report_analysis_card h3 {
        color: #2DD4BF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.4rem !important;
        animation: none !important;
    }

    .st-key-report_analysis_card p,
    .st-key-report_analysis_card li,
    .st-key-report_analysis_card span,
    .st-key-report_analysis_card strong {
        color: #EAF2F5 !important;
        font-size: 0.9rem !important;
        line-height: 1.55 !important;
    }

    .st-key-report_analysis_card strong {
        color: #2DD4BF !important;
    }

    </style>
    """, unsafe_allow_html=True)

    if "report_messages" not in st.session_state:
        st.session_state.report_messages = []

    if "report_system_prompt" not in st.session_state:
        st.session_state.report_system_prompt = ""

    if "show_compare_uploader" not in st.session_state:
        st.session_state.show_compare_uploader = False

    if report_text != "":

        with st.expander("📄 Extracted Report"):
            st.text_area("Report Content", report_text, height=250)

    username = st.session_state.get("username")
    user = get_user_by_username(username)
    profile_context = build_profile_context(user)
    language = st.session_state.get("language", "English")

    col1, col2 = st.columns(2)

    with col1:
        analyze_clicked = st.button("🧠 Analyze Report", type="primary", use_container_width=True)

    with col2:
        compare_clicked = st.button("📊 Compare with Previous Report", use_container_width=True)

    if compare_clicked:
        st.session_state.show_compare_uploader = True

    # -----------------------------------
    # Compare with a previous report
    # -----------------------------------

    if st.session_state.show_compare_uploader:

        with st.expander("📎 Upload the Previous Report to Compare", expanded=True):

            old_report_file = st.file_uploader(
                "Choose the older PDF report",
                type=["pdf"],
                key="old_report_uploader"
            )

            if st.button("Run Comparison", type="primary", key="run_comparison_btn"):

                if report_text == "":
                    st.warning("Please upload the current report from the sidebar first.")

                elif old_report_file is None:
                    st.warning("Please upload the previous report to compare with.")

                else:
                    old_report_text = extract_text_from_pdf(old_report_file)

                    system_prompt = build_report_comparison_system_prompt(
                        old_report_text, report_text, profile_context, language
                    )
                    st.session_state.report_system_prompt = system_prompt

                    with st.spinner("Comparing reports..."):
                        first_reply = chat_with_context(
                            system_prompt,
                            [{"role": "user", "content": "Please compare these two reports."}]
                        )

                    st.session_state.report_messages = [
                        {"role": "user", "content": "Please compare these two reports."},
                        {"role": "assistant", "content": first_reply}
                    ]

                    st.session_state.show_compare_uploader = False
                    st.rerun()

    # -----------------------------------
    # Single report analysis
    # -----------------------------------

    if analyze_clicked:

        if report_text == "":
            st.warning("Please upload a medical report PDF from the sidebar first.")

        else:
            system_prompt = build_report_analysis_system_prompt(report_text, profile_context, language)
            st.session_state.report_system_prompt = system_prompt

            with st.spinner("Analyzing Medical Report..."):
                first_reply = chat_with_context(
                    system_prompt,
                    [{"role": "user", "content": "Please give me the full analysis of this report."}]
                )

            st.session_state.report_messages = [
                {"role": "user", "content": "Please give me the full analysis of this report."},
                {"role": "assistant", "content": first_reply}
            ]

            st.rerun()

    # -----------------------------------
    # Professional report card + PDF download
    # -----------------------------------

    if len(st.session_state.report_messages) > 1:

        st.markdown("---")

        analysis_content = st.session_state.report_messages[1]["content"]
        generated_on = datetime.now().strftime("%d %b %Y, %I:%M %p")

        report_card = st.container(key="report_analysis_card")

        with report_card:

            st.markdown(f"""
                <div class='report-card-header'>
                    <div class='report-card-title'>🧾 Medical Report Analysis</div>
                    <div class='report-card-meta'>@{username}<br>{generated_on}</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(strip_emoji_for_display(analysis_content))

        pdf_path = generate_report_pdf(
            analysis_content,
            patient_info=user,
            report_title="Medical Report Analysis"
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download as PDF",
                data=f.read(),
                file_name="MediAssist_Report_Analysis.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # -----------------------------------
        # Follow-up conversation (everything after the first exchange)
        # -----------------------------------

        follow_up_history = st.session_state.report_messages[2:]

        for msg in follow_up_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        follow_up = st.chat_input("Ask a question about this report...")

        if follow_up:

            st.session_state.report_messages.append({"role": "user", "content": follow_up})

            with st.chat_message("user"):
                st.markdown(follow_up)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    reply = chat_with_context(
                        st.session_state.report_system_prompt,
                        st.session_state.report_messages
                    )
                st.markdown(reply)

            st.session_state.report_messages.append({"role": "assistant", "content": reply})
            st.rerun()

        st.markdown("---")

        if st.button("🔄 Start New Report Analysis"):
            st.session_state.report_messages = []
            st.session_state.report_system_prompt = ""
            st.rerun()