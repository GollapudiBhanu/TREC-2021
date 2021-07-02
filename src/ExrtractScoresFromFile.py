import pandas as pd

class ExtractList:

    def __init__(self, source_file):
        self.source_file = source_file

    ''' 
        Description: Extract the query_id, doc_id and Score_list from the given source_file path.
        Return: 
            1.query_id_list: []
            2.doc_id_list: []
            3.score_list: []
    '''
    def extractScore(self):
        df = pd.read_csv(self.source_file, sep='\t')
        df.columns = ["query_id", "doc_id", "score"]
        df = df.dropna()
        df["group_id"] = df.groupby(["query_id"]).grouper.group_info[0]
        df = df.groupby(["group_id"]).agg(lambda x: x.tolist())
        doc_id_list = df['doc_id'].tolist()
        query_id_list = df['query_id'].tolist()
        score_list = df['score'].tolist()
        return (query_id_list,doc_id_list,score_list)

    ''' 
        Description: Extract the query_id, doc_id and Score_list from the given source_file path.
        Return: 
            1.query_id_list: []
            2.doc_id_list: []
            3.score_list: []
    '''
    def extractCombinedDocScores(self):
        df = pd.read_csv(self.source_file, sep='\t')
        df.columns = ["query_id", "doc_id", "score", "floatNumber"]
        df = df.dropna()
        df["group_id"] = df.groupby(["query_id"]).grouper.group_info[0]
        df = df.groupby(["group_id"]).agg(lambda x: x.tolist())
        doc_id_list = df['doc_id'].tolist()
        query_id_list = df['query_id'].tolist()
        score_list = df['score'].tolist()
        return (query_id_list, doc_id_list, score_list)

