from reporting.email_distributor import send_report_email
from mobile_notifications import send_push_notification

def notify_email(recipient, subject, message):
    send_report_email(recipient, subject, message)

def notify_push(user_token, title, body):
    send_push_notification(user_token, title, body)

# Kullanım: alert.add_alert('dusuk_satis', "SELECT * FROM Sales WHERE Sales < 100", lambda df: notify_email("admin@...", "Düşük Satış Uyarısı", str(df)))