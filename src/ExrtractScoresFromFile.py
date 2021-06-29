import pandas as pd

class ExtractList:

    def __init__(self, source_file):
        self.source_file = source_file

    def extractScore(self):
        df = pd.read_csv(self.source_file, sep='\t')
        df.columns = ["query_id", "doc_id", "score"]
        df = df.dropna()
        df["group_id"] = df.groupby(["query_id"]).grouper.group_info[0]
        df = df.groupby(["group_id"]).agg(lambda x: x.tolist())
        doc_id_list = df['doc_id'].tolist()
        query_id_list = df['query_id'].tolist()
        score_list = df['score'].tolist()
        return query_id_list,doc_id_list,score_list


