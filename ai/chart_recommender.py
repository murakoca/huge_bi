import pandas as pd
import numpy as np

class ChartRecommender:
    """
    Veri setindeki sütun tiplerine ve istatistiklere göre en uygun grafik tipini önerir.
    """
    @staticmethod
    def _detect_types(df: pd.DataFrame) -> dict:
        types = {}
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                types[col] = 'numeric'
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                types[col] = 'datetime'
            else:
                types[col] = 'categorical'
        return types

    @staticmethod
    def recommend(df: pd.DataFrame, target_col: str = None) -> list:
        """
        Öneri listesi döner: her eleman {'chart_type': ..., 'x': ..., 'y': ..., 'reason': ...}
        """
        types = ChartRecommender._detect_types(df)
        numeric_cols = [c for c, t in types.items() if t == 'numeric']
        cat_cols = [c for c, t in types.items() if t == 'categorical']
        datetime_cols = [c for c, t in types.items() if t == 'datetime']

        recommendations = []
        # 1. Zaman serisi varsa çizgi grafiği
        if datetime_cols and numeric_cols:
            for dcol in datetime_cols:
                for ncol in numeric_cols:
                    recommendations.append({
                        'chart_type': 'line',
                        'x': dcol,
                        'y': ncol,
                        'reason': f"Zaman serisi ({dcol}) ve sayısal ({ncol}) bulundu."
                    })
        # 2. Kategorik vs sayısal → çubuk grafik
        if cat_cols and numeric_cols:
            for ccol in cat_cols:
                if df[ccol].nunique() <= 20:  # çok fazla kategori olmasın
                    for ncol in numeric_cols:
                        recommendations.append({
                            'chart_type': 'bar',
                            'x': ccol,
                            'y': ncol,
                            'reason': f"Kategorik ({ccol}) ve sayısal ({ncol})."
                        })
        # 3. Tek sayısal → histogram
        if numeric_cols:
            for ncol in numeric_cols:
                recommendations.append({
                    'chart_type': 'histogram',
                    'x': ncol,
                    'reason': f"Tek sayısal sütun ({ncol})."
                })
        # 4. İki sayısal → scatter
        if len(numeric_cols) >= 2:
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    recommendations.append({
                        'chart_type': 'scatter',
                        'x': numeric_cols[i],
                        'y': numeric_cols[j],
                        'reason': f"İki sayısal sütun ({numeric_cols[i]} vs {numeric_cols[j]})."
                    })
        # 5. Kategorik vs kategorik → heatmap (pivot)
        if len(cat_cols) >= 2 and len(numeric_cols) >= 1:
            recommendations.append({
                'chart_type': 'heatmap',
                'x': cat_cols[0],
                'y': cat_cols[1] if len(cat_cols) > 1 else cat_cols[0],
                'z': numeric_cols[0],
                'reason': "Kategorik ve sayısal sütunlarla ısı haritası."
            })
        # 6. Pasta grafik (tek kategorik, tek sayısal, az kategori)
        if cat_cols and numeric_cols:
            for ccol in cat_cols:
                if df[ccol].nunique() <= 10:
                    recommendations.append({
                        'chart_type': 'pie',
                        'names': ccol,
                        'values': numeric_cols[0],
                        'reason': f"Az sayıda kategori ({ccol}) ile oran gösterimi."
                    })
        return recommendations