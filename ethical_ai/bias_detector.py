from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric
import pandas as pd

def measure_bias(df: pd.DataFrame, label_col: str, protected_col: str, favorable_label=1, unfavorable_label=0):
    """
    Korunan bir özelliğe göre ayrım yanlılığını ölçer.
    Döndürülen sözlük: disparate_impact, mean_difference
    """
    dataset = BinaryLabelDataset(
        df=df,
        label_names=[label_col],
        protected_attribute_names=[protected_col],
        favorable_label=favorable_label,
        unfavorable_label=unfavorable_label
    )
    privileged_groups = [{protected_col: favorable_label}]
    unprivileged_groups = [{protected_col: unfavorable_label}]
    metric = BinaryLabelDatasetMetric(
        dataset,
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )
    return {
        'disparate_impact': round(metric.disparate_impact(), 4),
        'mean_difference': round(metric.mean_difference(), 4)
    }