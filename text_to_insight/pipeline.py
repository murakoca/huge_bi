from chat_bi.bot_core import ChatBI
from ai.report_writer import ReportWriter
import pandas as pd

class TextToInsight:
    def __init__(self, model, chat_bi: ChatBI, writer: ReportWriter):
        self.model = model
        self.chat = chat_bi
        self.writer = writer

    def process(self, question):
        response = self.chat.process(question)
        if response.get('action') == 'run_query':
            df = self.model.query(response['params']['sql'])
        else:
            df = pd.DataFrame()
        insight = self.writer.summarize(df) if not df.empty else "Veri bulunamadı."
        return {
            'data': df.head().to_dict(),
            'insight': insight,
            'suggested_chart': 'bar' if df.shape[1] > 1 else 'kpi'
        }