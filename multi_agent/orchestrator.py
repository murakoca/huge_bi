from langchain_ollama import ChatOllama
from multi_agent.agents import DataPrepAgent, AnalysisAgent, VisualizationAgent
import json

class BIOrchestrator:
    def __init__(self, model="mistral", base_url="http://localhost:11434"):
        self.llm = ChatOllama(model=model, base_url=base_url, temperature=0)
        self.agents = {
            'dataprep': DataPrepAgent('DataPrep', self.llm),
            'analysis': AnalysisAgent('Analysis', self.llm),
            'visualization': VisualizationAgent('Visualization', self.llm)
        }

    def execute_pipeline(self, user_request, data_context):
        steps = self._plan_steps(user_request)
        result = {}
        for step in steps:
            agent_name = step['agent']
            task = step['task']
            result[agent_name] = self.agents[agent_name].process(task, data_context)
        return self._compile_response(result)

    def _plan_steps(self, request):
        # Sabit bir plan döndürüyoruz, LLM ile de yapılabilir.
        return [
            {"agent": "dataprep", "task": "Eksik verileri doldur"},
            {"agent": "analysis", "task": "Bölgelere göre toplam satış"},
            {"agent": "visualization", "task": "Çubuk grafik oluştur"}
        ]

    def _compile_response(self, result):
        return {"steps": result, "summary": "İşlem tamamlandı."}