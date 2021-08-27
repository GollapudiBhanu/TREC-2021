import pandas as pd
from QueryExpansion import ExapnsionScore_2016
from elasticsearch import Elasticsearch
from pandas.core.common import flatten

'''
This file is used to extract the concat string for the provided documnet id.

input_file_path: input file path 
out_file_path: output file path, where you need to save the concat string.

'''
class ExrtractText:

    def __init__(self, input_file_path, out_file_path):
        self.input_file_path = input_file_path
        self.out_file_path = out_file_path
        self.es = Elasticsearch(hosts=["localhost"])


    def readfile(self):
        df = pd.read_csv(self.input_file_path, sep=",")
        df.columns = ['query_id',
                      'document_id',
                      'score']
        df["group_id"] = df.groupby(["query_id"]).grouper.group_info[0]
        df = df.groupby(["group_id"]).agg(lambda x: x.tolist())
        query_id_list = df['query_id'].tolist()
        doc_list = df['document_id'].tolist()
        score_list = df['score'].tolist()
        return doc_list, query_id_list, score_list


    def readfile_1(self):
        df = pd.read_csv(self.input_file_path, sep="\t",header = None)
        #df = pd.read_csv(self.input_file_path, sep=",")
        print(df.head(10))
        df.columns = ['query_id',
                      'document_id',
                      'Pseudoscore',
                      'score']

        df["group_id"] = df.groupby(["query_id"]).grouper.group_info[0]
        df = df.groupby(["group_id"]).agg(lambda x: x.tolist())
        query_id_list = df['query_id'].tolist()
        doc_list = df['document_id'].tolist()
        score_list = df['score'].tolist()

        return doc_list, query_id_list, score_list



    def prepareTrainingModel(self, doc_list, search_index):
        final_list = []
        for doc_id in doc_list:
            concat_string_list = list()
            for doc in doc_id:
                query_body = {
                    'query': {
                        'query_string': {
                            'default_field': "DOCNO",
                            'query': doc
                        }
                    }
                }
                query_result = self.es.search(index=search_index, body=query_body, size=1)
                if query_result is not None:
                    for res in query_result['hits']['hits']:
                        concat_string_list.append(res['_source']['concat_string'])
                else:
                    concat_string_list.append(None)
            final_list.append(concat_string_list)
        return final_list

    def prepareTrainingModel_1(self, doc_list, search_index):
        final_list = []
        for docs in doc_list:
            concat_string_list = list()
            for doc_id in docs:
                query_body = {
                    'query': {
                        'query_string': {
                            'default_field': "url",
                            'query': 'httpsclinicaltrialsgovshow'+str(doc_id)
                        }
                    }
                }
                query_result = self.es.search(index=search_index, body=query_body, size=1)
                if query_result is not None:
                    for res in query_result['hits']['hits']:
                        concat_string_list.append(res['_source']['concat_string'])
                else:
                    concat_string_list.append(None)
            final_list.append(concat_string_list)
        return final_list

    def getQueryExpansionText(self):
        results = self.readfile()
        doc_list = results[0]
        query_id_list = results[1]
        score_list = results[2]
        concat_str_list = self.prepareTrainingModel_1(doc_list, '2016-trec-precision-medicine-final')
        concat_str_list = list(flatten(concat_str_list))
        data = {'query_id': query_id_list,
                'Document_id': doc_list,
                'Score': score_list,
                'Concat_string': concat_str_list}
        df = pd.DataFrame(data)
        df.to_csv(self.out_file_path, index=False)

    def getQueryExpansionText_1(self, search_index):
        results = self.readfile_1()
        doc_list = results[0]
        query_id_list = results[1]
        score_list = results[2]
        #if it is 2021 or 2016o or 2019 dependes on the year we need to enable the below lines.
        #concat_str_list = self.prepareTrainingModel_1(doc_list, '2021-trec-precision-medicine-final') #2021 or 2019 enable this
        concat_str_list = self.prepareTrainingModel(doc_list, search_index) #if it is 2016  we need to enable this.
        flaten_str_list = list(flatten(concat_str_list))
        flatten_doc_list =  list(flatten(doc_list))
        flatten_query_id_list = list(flatten(query_id_list))
        flatten_score_list = list(flatten(score_list))
        data = {'query_id': flatten_query_id_list,
                'Document_id': flatten_doc_list,
                'Score': flatten_score_list,
                'Concat_string': flaten_str_list}
        df = pd.DataFrame(data)
        df.to_csv(self.out_file_path, index=False)



#obj = ExrtractText('/home/junhua/trec/Trec2021/Output/2016QueryOutput/2016Reranking/Bhanu-All_merge.csv',
#                   '/home/junhua/trec/Trec2021/Output/2016QueryOutput/2016Reranking/Bhanu-All_merge_concatstring.csv')
#obj.getQueryExpansionText_1()
