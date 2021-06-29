import pandas as pd

class GetQuery_2016:

    def __init__(self, query_file_path):
        self.query_file_path = query_file_path

    def getQueryListWithId(self):
        df = pd.read_csv(self.query_file_path)
        df.columns = ['sl.no', 'queryID', 'summary', 'summary_keyword', 'description', 'description_keyword', 'note' , 'note_keyword']
        queryid_list = df['queryID'].tolist()
        sum_query_list = df['summary_keyword'].tolist()
        des_query_list = df['description_keyword'].tolist()
        note_query_list = df['note_keyword'].tolist()
        return (queryid_list, sum_query_list, des_query_list, note_query_list)

    def getMetamapQueryListWithId(self):
        df = pd.read_csv(self.query_file_path)
        df.columns = ['sl.no', 'queryID', 'query_concept', 'extended_concept']
        queryid_list = df['queryID'].tolist()
        metamap_query_list = df['query_concept'].tolist()
        extended_query_list = df['extended_concept'].tolist()
        return (queryid_list, metamap_query_list, extended_query_list)


    def getFilteredMetamapQueryListWithId(self):
        df = pd.read_csv(self.query_file_path)
        df.columns = ['sl.no', 'queryID', 'query_concept', 'extended_concept', 'query_concept_filtered']
        queryid_list = df['queryID'].tolist()
        metamap_query_list = df['query_concept'].tolist()
        extended_query_list = df['extended_concept'].tolist()
        filtred_query_list = df['query_concept_filtered'].tolist()
        return (queryid_list, filtred_query_list)

    def getNERQueriesList(self, column_names_list):
        df = pd.read_csv(self.query_file_path)
        column_list = []
        for name in column_names_list:
            column_list.append(name)
        df.columns = column_list
        final_query_list = []
        df = df.dropna()
        print(df.head(100))
        for name in column_list:
            out_list = df[name].tolist()
            final_query_list.append(out_list)
        return tuple(final_query_list)
