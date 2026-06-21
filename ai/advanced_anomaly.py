import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor

class AdvancedAnomalyDetector:
    def __init__(self, method='isolation_forest', **kwargs):
        self.method = method
        self.params = kwargs
        self.model = None
        self._init_model()

    def _init_model(self):
        if self.method == 'isolation_forest':
            self.model = IsolationForest(contamination=self.params.get('contamination', 0.05),
                                        random_state=42)
        elif self.method == 'one_class_svm':
            self.model = OneClassSVM(nu=self.params.get('contamination', 0.05),
                                     kernel='rbf', gamma='scale')
        elif self.method == 'elliptic_envelope':
            self.model = EllipticEnvelope(contamination=self.params.get('contamination', 0.05),
                                          random_state=42)
        elif self.method == 'lof':
            self.model = LocalOutlierFactor(novelty=True,
                                            contamination=self.params.get('contamination', 0.05))
        else:
            raise ValueError(f"Bilinmeyen yöntem: {self.method}")

    def fit_predict(self, df: pd.DataFrame):
        """Sayısal sütunları alır ve anomali etiketlerini döndürür (-1: anomali, 1: normal)."""
        # Sadece sayısal sütunları seç
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return pd.Series([1]*len(df))  # anomali yok
        self.model.fit(numeric_df)
        preds = self.model.predict(numeric_df)
        return pd.Series(preds, index=df.index)

    def detect_anomalies(self, df: pd.DataFrame):
        preds = self.fit_predict(df)
        return df[preds == -1]