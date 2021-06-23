import pandas as pd


class ExtractQueries:
    def __init__(self, query_file_path):
        self.query_file_path = query_file_path
        self.query_frame = ""
        self.readfile()

    def readfile(self):
        self.query_frame = pd.read_csv(self.query_file_path)

    def getQueries(self):
        query_id_list = self.query_frame["QueryID"].tolist()
        query_list = self.query_frame["mtxt_keyword"].tolist()
        return query_id_list, query_list
