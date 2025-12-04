# reports_utils.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

OUT_DIR = os.path.join(os.getcwd(), "generated_reports")
os.makedirs(OUT_DIR, exist_ok=True)

def create_pdf_report_and_save(response_id, answers, user_email, summary_text):
    fname = f"report_{response_id}_{int(datetime.utcnow().timestamp())}.pdf"
    path = os.path.join(OUT_DIR, fname)
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(30*mm, height - 30*mm, "CareerAura AI — Partial Career Report")
    c.setFont("Helvetica", 10)
    c.drawString(30*mm, height - 37*mm, f"Report ID: {response_id}   Generated: {datetime.utcnow().isoformat()}")

    # Add summary
    c.setFont("Helvetica", 11)
    y = height - 50*mm
    lines = [
        "This is a partial report generated to give you initial insights based on your responses.",
        "",
        "Summary:",
        summary_text,
        "",
        "To receive a full, personalized report and a career guidance call, please click the link below or email us.",
        ""
    ]
    for line in lines:
        c.drawString(30*mm, y, line)
        y -= 8*mm

    # Contact link area (we will encode a safe link)
    base = os.getenv("APP_BASE_URL", "http://localhost:5173")
    contact_link = f"{base}/api/contact-report?report_id={response_id}&email={user_email or ''}"
    c.setFillColorRGB(0,0,0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30*mm, y, "To know more / contact us (click the URL below):")
    y -= 8*mm
    c.setFont("Helvetica", 9)
    # print link as text; many PDF viewers will make it clickable
    c.drawString(30*mm, y, contact_link)

    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(30*mm, 20*mm, "Partial report — contact us to unlock the full guidance.")

    c.save()
    return path

def send_email_with_attachment(to_email, subject, body, attachment_path=None):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    from_email = os.getenv("FROM_EMAIL")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    if attachment_path:
        with open(attachment_path, "rb") as f:
            data = f.read()
        # guess simple mime
        msg.add_attachment(data, maintype="application", subtype="pdf", filename=os.path.basename(attachment_path))

    # send
    with smtplib.SMTP(smtp_host, smtp_port) as s:
        s.starttls()
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)
