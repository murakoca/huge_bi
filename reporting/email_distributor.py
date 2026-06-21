import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

SMTP_SERVER = "smtp.office365.com"  # veya smtp.gmail.com
SMTP_PORT = 587
SENDER = "reports@yourdomain.com"
PASSWORD = "your_password"

def send_report_email(recipient, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.send_message(msg)
    print(f"E‑posta gönderildi: {recipient}")

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    lambda: send_report_email("ceo@company.com", "Günlük Satış Raporu", "<h1>Rapor ektedir</h1>", "report.pdf"),
    'cron', hour=8, minute=0
)
scheduler.start()