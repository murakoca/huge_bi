class SharePointConnector:
    def __init__(self, site_url, username, password):
        self.site_url = site_url
        # Gerçek bağlantı için office365-rest-python-client kullanılır.
    def get_list(self, list_name):
        # Dummy data
        import pandas as pd
        return pd.DataFrame({"ID": [1], "Title": ["Demo"]})