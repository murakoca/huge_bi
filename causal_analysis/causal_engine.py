import dowhy
from dowhy import CausalModel
import pandas as pd

def analyze_cause(df: pd.DataFrame, treatment: str, outcome: str, graph: str):
    model = CausalModel(
        data=df,
        treatment=treatment,
        outcome=outcome,
        graph=graph
    )
    identified_estimand = model.identify_effect()
    causal_estimate = model.estimate_effect(identified_estimand,
                                            method_name="backdoor.linear_regression")
    return {
        'estimate': causal_estimate.value,
        'interpretation': str(causal_estimate)
    }