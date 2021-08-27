import pandas as pd
import numpy as np
import os
import re
from elasticsearch import Elasticsearch

'''
This file is used for preparing reranking model, but we are not using this.
'''
class Model:

    def __init__(self, judgmenet_file_path = " ", output_file_path = " "):
        self.judgmenet_file_path = judgmenet_file_path
        self.es = Elasticsearch(hosts=["localhost"])
        self.output_file_path = output_file_path
        self.doc_list = []
        #self.query_file_path = query_file_path

    def readfile(self):
        df = pd.read_csv(self.judgmenet_file_path, sep=" ",header = None)
        df.columns = ['query_id',
                      'sample',
                      'document_id',
                      'relevant_id']
        df['rev_status'] = np.where(df['relevant_id'] == 0, 'Non-Relevant', 'Relevant')
        rev_df = df[df['rev_status'] == 'Relevant']
        rev_df["group_id"] = rev_df.groupby(["query_id"]).grouper.group_info[0]
        rev_df = rev_df.groupby(["group_id"]).agg(lambda x: x.tolist())
        query_id_list = rev_df['query_id'].tolist()
        rev_status_list = rev_df['rev_status'].tolist()
        self.doc_list = rev_df['document_id'].tolist()

    def prepareTrainingModel(self, search_index):
        self.readfile()
        final_list = []
        for docs in self.doc_list:
            concat_string_list = list()
            for doc_id in docs:
                query_body = {
                    'query': {
                        'query_string': {
                            'default_field': "DOCNO",
                            'query': doc_id
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
            self.save(final_list)
            return final_list

    def prepareQueryModel(self, query_file_path, out_query_file_path):
        coloumn_list = ['sl.no', 'queryID',
                        'summary','summary_keyword','summary_keyword_expansion',
                        'description','description_keyword',
                        'note','note_keyword']
        df = pd.read_csv(query_file_path)
        column_list = []
        for name in coloumn_list:
            column_list.append(name)
        df.columns = column_list
        df = df.dropna()
        df['queryID'] = pd.to_numeric(df['queryID'])
        df.sort_values(by=['queryID'], ascending=True, inplace=True)
        df['summary_combined'] = df[['summary_keyword', 'summary_keyword_expansion']].agg(','.join, axis=1)
        summary_query_expansion = df['summary_combined'].tolist()
        summary_topic_id_list = df['queryID'].tolist()
        self.saveQueryModel(summary_topic_id_list,
                            summary_query_expansion,
                            out_query_file_path)

    def save(self, final_list):
        for doc_list, concat_list in zip(self.doc_list, final_list):
            for doc_id, concat_str in zip(doc_list, concat_list):
                mode = "a" if os.path.exists(self.output_file_path) else "w"
                with open(self.output_file_path, mode) as outfile:
                    outfile.write(str(doc_id) + '\n' + concat_str + '\n' + '\t' + '/' + '\n')

    def saveQueryModel(self, summary_topic_id_list, summary_query_expansion, out_query_file_path):
        for topic_id, concat_list in zip(summary_topic_id_list, summary_query_expansion):
            res = self.prepareConcatstr(concat_list)
            mode = "a" if os.path.exists(out_query_file_path) else "w"
            with open(out_query_file_path, mode) as outfile:
                outfile.write(str(topic_id) + '\t' + res + '\n')

    def load_data(self, res_file_path):
        df = pd.read_csv(res_file_path, delimiter="\t", header=None)
        df.columns = ['qid', 'doc_id', 'score', 'text']
        count = df.shape[0]
        return df.loc[:count, ['qid', 'doc_id', 'score', 'text']].dropna()

    def prepareresultantDoc(self, res_file_path, out_put_file):
        df = self.load_data(res_file_path)
        df = df.drop_duplicates(subset='doc_id', keep='first')
        doc_id_list = df['doc_id'].tolist()
        text_list = df['text'].tolist()
        self.saveresultantDoc(doc_id_list, text_list, out_put_file)

    def saveresultantDoc(self, doc_id_list, text_list, out_file_path):
        for doc_id, text in zip(doc_id_list, text_list):
            mode = "a" if os.path.exists(out_file_path) else "w"
            with open(out_file_path, mode) as outfile:
                outfile.write(str(doc_id) + '\t' + text + '\n')

    def prepareConcatstr(self, concat_str):
        outputstr = ""
        for res in concat_str.split(','):
            out = re.sub(r"^\s+|\s+$", "", res)
            if outputstr == "":
                outputstr = out
            else:
                outputstr = outputstr + ' ' + out
        return outputstr.lower()


#obj = Model('/home/junhua/trec/Trec2021/Data/2016_Quries/qrels-treceval-2016.txt',
               #'/home/junhua/trec/Trec2021/Output/Reranking_Traning_model_2016.txt')
#obj.prepareTrainingModel("2016-trec-precision-medicine-final")

#obj = Model()
#obj.prepareQueryModel('/home/junhua/trec/Trec2021/Data/2016_Quries/Manual_KeywordExtr_Query2016_.csv',
#                      '/home/junhua/trec/Trec2021/Output/qrels_2016.tsv')
#obj.prepareresultantDoc('/home/junhua/trec/Trec2021/Output/Summary_OR_2021-07-20T14:03:05.844488_Manual_KeywordExtr_Query2016_.csv',
#                        '/home/junhua/trec/Trec2021/Output/doc_res_2016.tsv')