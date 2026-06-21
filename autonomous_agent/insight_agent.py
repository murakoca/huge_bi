import schedule
import time
from ai.report_writer import ReportWriter
from reporting.email_distributor import send_report_email

class InsightAgent:
    """Belirli aralıklarla veriyi analiz edip içgörü raporu gönderen otonom ajan."""

    def __init__(self, model, writer: ReportWriter = None, recipients=None):
        self.model = model
        self.writer = writer or ReportWriter()
        self.recipients = recipients or ["admin@company.com"]

    def analyze(self):
        """Veriyi sorgulayıp özet çıkarır ve e-posta ile gönderir."""
        try:
            df = self.model.query("SELECT * FROM Sales_with_Customers")
            insight = self.writer.summarize(df)
            for recipient in self.recipients:
                send_report_email(recipient, "Otomatik İçgörü Raporu", insight)
            print("İçgörü raporu gönderildi.")
        except Exception as e:
            print(f"İçgörü ajanı hatası: {e}")

    def run(self, interval_hours=1):
        """Zamanlanmış görevi başlatır (arka planda çalışır)."""
        schedule.every(interval_hours).hours.do(self.analyze)
        while True:
            schedule.run_pending()
            time.sleep(60)