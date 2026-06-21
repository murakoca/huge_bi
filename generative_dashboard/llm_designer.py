import requests
import json

class LLMDashboardDesigner:
    def __init__(self, ollama_url="http://localhost:11434", model="mistral"):
        self.url = f"{ollama_url}/api/chat"
        self.model = model

    def generate_layout(self, user_prompt: str, schema: dict) -> dict:
        system_msg = """
        Sen bir iş zekası dashboard tasarımcısısın. 
        Verilen veri şemasına ve kullanıcı isteğine göre bir JSON çıktısı üret.
        Çıktı şu formatta olmalı:
        {
          "title": "Dashboard Başlığı",
          "components": [
            {"type": "kpi", "title": "...", "query": "..."},
            {"type": "bar_chart", "title": "...", "x": "...", "y": "...", "query": "..."}
          ]
        }
        Sadece geçerli JSON döndür, başka metin ekleme.
        """
        user_msg = f"Şema: {json.dumps(schema)}\nKullanıcı isteği: {user_prompt}"

        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    "format": "json",
                    "stream": False
                },
                timeout=60
            )
            data = response.json()
            plan = json.loads(data["message"]["content"])
            return plan
        except Exception:
            # Fallback
            return {
                "title": "Otomatik Dashboard",
                "components": [
                    {"type": "kpi", "title": "Toplam Satış", "query": "SELECT SUM(Sales) FROM Sales_with_Customers"},
                    {"type": "bar_chart", "title": "Ürün Satışları", "x": "Product", "y": "Sales", "query": "SELECT Product, SUM(Sales) AS Sales FROM Sales_with_Customers GROUP BY Product"}
                ]
            }