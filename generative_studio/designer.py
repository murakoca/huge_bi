import requests
import json

class GenerativeStudio:
    def __init__(self, ollama_url="http://localhost:11434", model="mistral"):
        self.url = f"{ollama_url}/api/chat"
        self.model = model

    def generate_dashboard_plan(self, description, data_schema, feedback=None):
        system_msg = "Sen bir dashboard tasarım uzmanısın. Kullanıcının isteğine uygun bir JSON plan üret."
        if feedback:
            system_msg += f" Önceki plana şu yorum yapıldı: {feedback}. Düzelt."
        user_msg = f"Açıklama: {description}\nVeri Şeması: {json.dumps(data_schema)}"

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
            plan = json.loads(response.json()["message"]["content"])
            return plan
        except Exception as e:
            # Fallback basit plan
            return {
                "title": "Örnek Dashboard",
                "components": [{"type": "kpi", "title": "Toplam Satış", "query": "SELECT SUM(Sales) FROM Sales_with_Customers"}]
            }

    def refine_with_feedback(self, plan, feedback, data_schema):
        return self.generate_dashboard_plan(
            description=f"Önceki plan: {json.dumps(plan)}",
            data_schema=data_schema,
            feedback=feedback
        )