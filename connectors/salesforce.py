import pandas as pd

class SalesforceConnector:
    def __init__(self, username, password, security_token):
        # simple-salesforce kütüphanesi ile bağlantı
        pass

    def get_data(self, soql_query):
        # Demo: boş DataFrame
        return pd.DataFrame({'Id': ['001xx'], 'Name': ['Demo Account']})