import importlib
from collections import defaultdict
from typing import Callable, Dict, List

class DataflowDAG:
    def __init__(self):
        self.steps: Dict[str, Callable] = {}
        self.dependencies: Dict[str, List[str]] = defaultdict(list)

    def add_step(self, name: str, func: Callable, depends_on: List[str] = None):
        self.steps[name] = func
        if depends_on:
            self.dependencies[name] = depends_on

    def execute(self):
        executed = set()
        while len(executed) < len(self.steps):
            for step_name, func in self.steps.items():
                if step_name in executed:
                    continue
                deps = self.dependencies.get(step_name, [])
                if all(d in executed for d in deps):
                    print(f"Veri akışı adımı çalışıyor: {step_name}")
                    func()
                    executed.add(step_name)
        print("Veri akışı tamamlandı.")