import pandas as pd

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

    def retrieveTRECResults(self):
        trecRetrieval_df = pd.read_csv(self.trec_file)
        trecRetrieval_df.columns = ["query_id", "sample_id", "doc_id", "relevant_id"]
        trecRetrieval_df = trecRetrieval_df.groupby(["query_id"]).agg(lambda x: x.tolist())
        doc_id_list = trecRetrieval_df['doc_id'].tolist()
        rev_score_list = trecRetrieval_df['relevant_id'].tolist()

        print(len(rev_score_list))
        for rev_score_list, doc_id_list in zip(rev_score_list, doc_id_list):
            out_put = list()
            for rev_score, doc_id in zip(rev_score_list, doc_id_list):
                if rev_score == 1:
                    out_put.append(doc_id.strip())
            self.trec_retrieval.append(out_put)

    def retrieveANDresults(self):
        retrieval_df = pd.read_csv(self.and_source_file, sep='\t')
        retrieval_df.columns = ["query_id", "doc_id", "score"]
        retrieval_df = retrieval_df.groupby(["query_id"]).agg(lambda x: x.tolist())
        and_results = retrieval_df['doc_id'].tolist()
        for and_res in and_results:
            out_put = list()
            for and_r in and_res:
                out_put.append(and_r.upper().strip())
            self.and_results.append(out_put)
            print("###############")
            print(len(self.and_results))
        self.calucalteANDRecall()

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

    def calucalteANDRecall(self):
        results = list()
        for treclist, and_list in zip(self.trec_retrieval, self.and_results):
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
        print("**************** Combine results ***********************")
        print(results)



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

obj = IR_Recall('/home/junhua/trec/Trec2021/Data/2019_quries/qrels-treceval-trials.csv', '/home/junhua/trec/Trec2021/Output/Final_AND_BoolQuery_scores_2019.csv', '/home/junhua/trec/Trec2021/Output/Final_OR_BoolQuery_scores_2019.csv')
#combined_BoolQuery_scores_2019.csv
#obj = IR_Recall('/home/junhua/trec/Trec2021/Data/2019_quries/qrels-treceval-trials.csv', '/home/junhua/trec/Trec2021/Output/combined_BoolQuery_scores_2019.csv')
