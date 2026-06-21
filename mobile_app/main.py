from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.network.urlrequest import UrlRequest

class MiniPowerBIApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.layout = MDCard()
        self.label = MDLabel(text="Veri yükleniyor...", halign="center")
        self.layout.add_widget(self.label)
        self.load_data()
        return self.layout

    def load_data(self):
        UrlRequest("http://your-server:8050/api/summary", on_success=self.update_label)

    def update_label(self, request, result):
        self.label.text = f"Toplam Satış: ${result['total_sales']:,.2f}"

if __name__ == '__main__':
    MiniPowerBIApp().run()