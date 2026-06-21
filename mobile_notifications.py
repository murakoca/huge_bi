# Gerçek FCM için firebase-admin kullanılır.
# Burada sadece print ile simüle ediyoruz.
def send_push_notification(user_token, title, body):
    print(f"FCM Gönderildi -> {user_token}: {title} - {body}")

# Zamanlanmış yenileme sonrası bildirim:
def notify_report_ready(user, report_name):
    send_push_notification(user, "Rapor Hazır", f"{report_name} güncellendi.")