import pandas as pd
import os

class FolderConnector:
    def __init__(self, folder_path):
        self.folder_path = folder_path
    def get_data(self, file_pattern="*.csv"):
        import glob
        files = glob.glob(os.path.join(self.folder_path, file_pattern))
        df_list = [pd.read_csv(f) for f in files]
        return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()