import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class GoogleAnalyticsConnector:
    def __init__(self, view_id=None, credentials=None):
        self.view_id = view_id
        # Gerçek bağlantı: google-analytics-data kütüphanesi

    def get_data(self, start_date, end_date, metrics, dimensions):
        # Demo veri üret
        dates = pd.date_range(start_date, end_date)
        data = []
        for d in dates:
            data.append({
                'date': d.strftime('%Y-%m-%d'),
                'sessions': np.random.randint(100, 500),
                'bounceRate': np.random.uniform(0.3, 0.7)
            })
        return pd.DataFrame(data)