import requests
import json

class ChatBI:
    """
    LangChain kullanmadan, doğrudan Ollama REST API ile çalışan sohbet asistanı.
    """
    def __init__(self, model="mistral", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.context = [
            {"role": "system", "content": (
                "Sen bir iş zekası sohbet asistanısın. "
                "Kullanıcı sorularını JSON olarak yanıtla. "
                "Format: {\"action\": \"...\", \"params\": {...}, \"reply\": \"...\"}"
            )}
        ]

    def process(self, user_input):
        messages = self.context + [{"role": "user", "content": user_input}]
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={"model": self.model, "messages": messages, "stream": False},
                timeout=30
            )
            data = response.json()
            content = data["message"]["content"]
            return json.loads(content)
        except Exception as e:
            # Fallback – basit bir yanıt
            return {"action": None, "reply": f"Bir sorun oluştu: {str(e)}"}

    def execute_action(self, action, params, model):
        if action == "run_query":
            df = model.query(params['sql'])
            return df.head(10).to_markdown()
        elif action == "create_chart":
            import plotly.express as px
            df = model.query(params['sql'])
            if params['type'] == 'bar':
                fig = px.bar(df, x=params['x'], y=params['y'], title=params['title'])
            else:
                fig = px.line(df, x=params['x'], y=params['y'], title=params['title'])
            fig.write_html("static/last_chart.html")
            return "Grafik oluşturuldu."
        return "İşlem tamam."