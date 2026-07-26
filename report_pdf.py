import re
from datetime import datetime
from fpdf import FPDF


def strip_emoji_for_display(text):
    """
    Removes emoji/symbols while keeping markdown formatting (###, **, -)
    intact, so it still renders nicely with st.markdown but looks clean
    and professional instead of emoji-heavy.
    """

    return re.sub(r"[^\x00-\xFF]", "", text)


def _parse_sections(markdown_text):
    """
    Splits AI markdown output (using ### headings) into a list of
    (heading, body) tuples.
    """

    parts = re.split(r"\n###\s+", "\n" + markdown_text.strip())
    sections = []

    for part in parts:
        part = part.strip()
        if not part:
            continue

        lines = part.split("\n", 1)
        heading = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""

        sections.append((heading, body))

    return sections


def _clean_heading(heading):
    """Removes emoji/symbols from a heading for a clean, professional look."""

    cleaned = re.sub(r"[^\x00-\x7F]+", "", heading).strip(" :-")
    return cleaned or heading


def _clean_body_for_pdf(body):
    """Strips markdown formatting and emoji so it renders cleanly in a PDF."""

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", body)
    text = re.sub(r"^\s*[-•]\s*", "- ", text, flags=re.MULTILINE)
    text = re.sub(r"[^\x00-\xFF]", "", text)
    return text


class ReportPDF(FPDF):

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(15, 92, 82)
        self.cell(0, 10, "MediAssist AI", ln=True, align="C")

        self.set_font("Helvetica", "", 10)
        self.set_text_color(110, 110, 110)
        self.cell(0, 6, "AI-Assisted Medical Report Analysis", ln=True, align="C")

        self.set_draw_color(45, 212, 191)
        self.set_line_width(0.6)
        self.line(15, 28, 195, 28)
        self.ln(8)

    def footer(self):
        self.set_y(-18)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 5, "AI-generated for educational purposes only. Not a medical diagnosis.", ln=True, align="C")
        self.cell(0, 5, f"Page {self.page_no()}", align="C")


def generate_report_pdf(analysis_text, patient_info=None, report_title="Medical Report Analysis", output_path="MediAssist_Report_Analysis.pdf"):
    """
    Builds a clean, hospital-style PDF from the AI's markdown analysis
    text. Returns the file path of the generated PDF.
    """

    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 8, report_title, ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)

    generated_on = datetime.now().strftime("%d %b %Y, %I:%M %p")
    info = patient_info or {}

    row1 = f"Name: {info.get('full_name') or info.get('username') or 'N/A'}    |    Age: {info.get('age') or 'N/A'}    |    Gender: {info.get('gender') or 'N/A'}"
    row2 = f"Blood Group: {info.get('blood_group') or 'N/A'}    |    Generated On: {generated_on}"

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 6, row1)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 6, row2)
    pdf.ln(4)

    pdf.set_draw_color(220, 220, 220)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(6)

    sections = _parse_sections(analysis_text)

    for heading, body in sections:

        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(15, 92, 82)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 7, _clean_heading(heading))
        pdf.ln(1)

        pdf.set_font("Helvetica", "", 10.5)
        pdf.set_text_color(30, 30, 30)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 6, _clean_body_for_pdf(body))
        pdf.ln(4)

    pdf.output(output_path)

    return output_path