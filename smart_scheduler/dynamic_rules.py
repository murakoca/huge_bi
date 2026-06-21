from datetime import datetime
from model.semantic_model import SemanticModel

def get_dynamic_recipients(model: SemanticModel) -> list:
    """
    Veriye göre kimlere rapor gideceğini belirle.
    Örn: EU bölgesinde satışı düşük olanların yöneticileri.
    """
    df = model.query("SELECT Region, SUM(Sales) as Total FROM Sales_with_Customers GROUP BY Region")
    recipients = []
    for _, row in df.iterrows():
        if row['Total'] < 5000:
            recipients.append(f"manager_{row['Region'].lower()}@company.com")
    return recipients