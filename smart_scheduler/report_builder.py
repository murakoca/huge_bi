from reporting.email_distributor import send_report_email

def build_personalized_report(user, df):
    html = f"<h1>Merhaba {user}</h1><p>Kişiselleştirilmiş özetiniz:</p>{df.to_html()}"
    return html

def distribute_smart_reports(model):
    recipients = get_dynamic_recipients(model)
    for r in recipients:
        # Her alıcı için özel veri
        region = r.split('_')[1].split('@')[0].upper()
        df = model.query(f"SELECT * FROM Sales_with_Customers WHERE Region='{region}'")
        body = build_personalized_report(r, df)
        send_report_email(r, "Haftalık Bölge Raporu", body)