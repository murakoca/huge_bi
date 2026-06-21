import pandas as pd
from sqlalchemy import create_engine

class SQLConnector:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
    def get_data(self, query):
        return pd.read_sql(query, self.engine)