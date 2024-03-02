import pandas as pd


class ExcelHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_excel(self, header=None, skiprows=2):
        return pd.read_excel(self.file_path, header=header, skiprows=skiprows)

    def extract_column_data(self, column_number):
        df = pd.read_excel(self.file_path, header=None, skiprows=2)
        df = df.drop(columns=[0])
        return df[column_number]
