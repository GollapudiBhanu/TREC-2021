import pandas as pd
from pandas.core.common import flatten

'''
This file is used to find the number of relevant documents form output file, using TREC judgement file.
'''
class IR_Recall:

    def __init__(self, trec_file, source_file_1, source_file_2 = ""):
        self.trec_file = trec_file
        self.and_source_file = source_file_1
        self.or_source_file = source_file_2
        self.trec_retrieval = list()
        self.and_results = list()
        self.or_results = list()
        self.retrieveTRECResults()
        self.retrieveANDresults()
        self.retrieveORresults()

    '''
        Find the relevant documnet id's of TREC judgement file.
    '''
    def retrieveTRECResults(self):
        trecRetrieval_df = pd.read_csv(self.trec_file, sep = ' ', header=None)
        trecRetrieval_df.columns = ["query_id", "sample_id", "doc_id", "relevant_id"]
        trecRetrieval_df = trecRetrieval_df.groupby(["query_id"]).agg(lambda x: x.tolist())
        doc_id_list = trecRetrieval_df['doc_id'].tolist()
        rev_score_list = trecRetrieval_df['relevant_id'].tolist()

        for rev_score_list, doc_id_list in zip(rev_score_list, doc_id_list):
            out_put = list()
            for rev_score, doc_id in zip(rev_score_list, doc_id_list):
                if rev_score == 1:
                    out_put.append(str(doc_id).strip())
                elif rev_score == 2:
                    out_put.append(str(doc_id).strip())
            self.trec_retrieval.append(out_put)

    '''
            Find the relevant documnet id's of AND result file.
    '''
    def retrieveANDresults(self):
        retrieval_df = pd.read_csv(self.and_source_file, sep='\t')
        retrieval_df.columns = ["query_id", "doc_id", "score", 'Bm25score', 'Text']
        retrieval_df = retrieval_df.groupby(["query_id"]).agg(lambda x: x.tolist())
        #retrieval_df_1 = retrieval_df.groupby(["query_id"]).agg(lambda x: x.tolist()[:1001]).reset_index()
        and_results = retrieval_df['doc_id'].tolist()
        #and_results_1 = retrieval_df_1['doc_id'].tolist()
        #print(len(and_results_1[0]))
        for and_res in and_results:
            out_put = list()
            for and_r in and_res:
                #out_put.append(str(and_r).upper().strip())
                out_put.append(str(and_r).strip())
            self.and_results.append(out_put[:1000])
            print("###############")
            print(len(self.and_results))
        self.calucalteANDRecall()

    '''
        Find the relevant documnet id's of OR result file.
    '''
    def retrieveORresults(self):
        retrieval_df = pd.read_csv(self.or_source_file, sep='\t')
        retrieval_df.columns = ["query_id", "doc_id", "score"]
        retrieval_df = retrieval_df.groupby(["query_id"]).agg(lambda x: x.tolist())
        retrieval_df.to_csv("BHAnu.csv")
        or_results = retrieval_df['doc_id'].tolist()
        for index, or_res in enumerate(or_results):
            out_put = list()
            for and_r in or_res:
                out_put.append(and_r.upper().strip())
            self.or_results.append(out_put)
        self.calucalteORRecall()

    '''
        If you want find the AND recall, we need to call this method.
    '''
    def calucalteANDRecall(self):
        results = list()
        trec_res = self.trec_retrieval[1]
        and_res = list(flatten(self.and_results[1]))
        set_out = set(trec_res)
        and_out = set(and_res)
        intersection = set.intersection(set_out, and_out)
        num = len(intersection)
        print(num)
        '''
        for treclist, and_list in zip(trec_res, and_res):
            set_out = set(treclist)
            and_out = set(and_list)
            intersection = set.intersection(set_out,and_out)
            num = len(intersection)
            denm = len(set_out)
            if denm == 0:
                results.append(num)
            else:
                res = num / denm
                results.append(res)
        '''
        print("**************** Combine results ***********************")
        print(results)

    '''
        If you want find the OR recall, we need to call this method.
    '''
    def calucalteORRecall(self):
        results = list()
        index = 0
        print(len(self.or_results))
        for treclist, or_list in zip(self.trec_retrieval, self.or_results):
            index += 1
            set_out = set(treclist)
            or_out = set(or_list)
            intersection = set.intersection(set_out, or_out)
            num = len(intersection)
            denm = len(set_out)
            if num == 0 or denm == 0:
                results.append(0)
            else:
                res = num / denm
                results.append(res)
        print("**************** OR results ***********************")
        print(results)

#obj = IR_Recall('/home/junhua/trec/Trec2021/Data/2016_Quries/qrels-treceval-2016.txt',
#                '/home/junhua/trec/Trec2021/Output/2016QueryOutput/Summary_COMBINED_2021-07-20T14_03_05.844488_Manual_KeywordExtr_Query2016_.csv')
#combined_BoolQuery_scores_2019.csv
#obj = IR_Recall('/home/junhua/trec/Trec2021/Data/2019_quries/qrels-treceval-trials.csv', '/home/junhua/trec/Trec2021/Output/combined_BoolQuery_scores_2019.csv')
