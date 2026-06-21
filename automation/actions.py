from reporting.email_distributor import send_report_email
from mobile_notifications import send_push_notification

def action_send_email(recipient, subject, body):
    send_report_email(recipient, subject, body)

def action_notify(user_token, title, message):
    send_push_notification(user_token, title, message)

def action_refresh_model(model):
    # veri yenileme
    pass