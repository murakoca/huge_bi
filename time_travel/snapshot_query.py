from datetime import datetime
import pandas as pd

class TimeTravel:
    """Veri setlerinin anlık kopyalarını saklayarak geçmişe dönük sorgu imkânı sunar."""

    def __init__(self):
        self.snapshots = {}

    def save_snapshot(self, name, df):
        key = f"{name}_{datetime.now().isoformat()}"
        self.snapshots[key] = df.copy()

    def query_as_of(self, name, timestamp):
        key = f"{name}_{timestamp}"
        return self.snapshots.get(key, pd.DataFrame())