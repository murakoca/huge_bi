import requests
import pandas as pd

class ReportWriter:
    def __init__(self, ollama_url="http://localhost:11434", model="mistral"):
        self.url = f"{ollama_url}/api/chat"
        self.model = model

    def summarize(self, df: pd.DataFrame, prompt_template: str = None) -> str:
        stats = {}
        if 'Sales' in df.columns:
            stats['toplam_satis'] = df['Sales'].sum()
        if 'Quantity' in df.columns:
            stats['ortalama_miktar'] = df['Quantity'].mean()
        if 'Product' in df.columns and 'Sales' in df.columns:
            stats['en_cok_satan'] = df.groupby('Product')['Sales'].sum().idxmax()

        prompt = prompt_template or "Aşağıdaki satış verisini bir yönetici için özetleyen kısa bir paragraf yaz:\n"
        prompt += str(stats)
        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False
                },
                timeout=30
            )
            data = response.json()
            return data["message"]["content"].strip()
        except Exception as e:
            # Fallback
            if stats.get('toplam_satis'):
                return f"Bu dönemde toplam satış ${stats['toplam_satis']:,.2f} olarak gerçekleşti. En çok satan ürün {stats.get('en_cok_satan', 'bilinmiyor')} oldu."
            return "Veri özeti oluşturulamadı."