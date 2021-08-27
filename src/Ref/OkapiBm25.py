import pandas as pd
from rank_bm25 import BM25Okapi
from elasticsearch import Elasticsearch


class OKAPIBM25_Scoring:

    def __init__(self, corpus_list):
        self.sourceDir = ""
        self.corpus = corpus_list
        self.es = Elasticsearch()

    '''
        Prepares and returns a BM25 object, with tokenized corpus 
    '''

    def prepareBM25(self):
        tokenized_corpus = list()
        for doc in self.corpus:
            if doc is None:
                continue
            tokenized_corpus.append(doc.split(" "))
        bm25 = BM25Okapi(tokenized_corpus)
        return bm25

    '''
        returns a count items in a list, with provided queryId. 
    '''

    def prepareList(self, id, count):
        id_list = list()
        for _ in range(count):
            id_list.append(id)
        return id_list

    '''
        1. Get the BM25 score, with provided query.
        2. match the docId, query_id and scores and writes it in to a output file. 
    '''

    def getBM25Score(self, query_list, doc_id_list):
        for query in query_list:
            tokenized_query = query.split(" ")
            bm25 = self.prepareBM25()
            query_id = self.getqueryId(query)
            doc_scores = bm25.get_scores(tokenized_query)
            query_id_list = self.prepareList(query_id, len(doc_scores))
            for query_id, doc_id, score in zip(query_id_list, doc_id_list, doc_scores):
                if score > 0.0:
                    print("scoring")
                    with open('./Output/Okapi_Final_score.csv', "a") as outFile:
                        outFile.write(str(query_id) + "\t" + doc_id + '\t' + str(score) + "\n")

    '''
            1. Get the BM25 score, with provided query.
            2. match the docId, query_id and scores and writes it in to a output file. 
        '''

    def getQueryExapnsionBM25Score(self, query_list, doc_id_list, query_id_list):
        for query_id, query, doc_id in zip(query_id_list, query_list, doc_id_list):
            tokenized_query = query.split(" ")
            bm25 = self.prepareBM25()
            doc_scores = bm25.get_scores(tokenized_query)
            query_id_list = self.prepareList(query_id, len(doc_scores))
            docs_id = self.prepareList(query_id, len(doc_scores))
            for query_id, doc_id, score in zip(query_id_list, docs_id, doc_scores):
                if score > 0.0:
                    print("scoring")
                    with open('./Output/Okapi_Expanded_Final_score.csv', "a") as outFile:
                        outFile.write(str(query_id) + "\t" + doc_id + '\t' + str(score) + "\n")


    '''
        1. get the Top 'n' scores with the provided query.        
    '''

    def getTopScores(self, query_list, doc_id_list, n):
        data_append = []
        for query in query_list:
            tokenized_query = query.split(" ")
            bm25 = self.prepareBM25()
            query_id = self.getqueryId(query)
            doc_scores = bm25.get_scores(tokenized_query)
            query_id_list = self.getQueryIdList(query_id, 1000)
            zipData = zip(doc_scores, doc_id_list, query_id_list)
            data_Frame = pd.DataFrame(zipData)
            data_Frame.columns = ["score", "fileName", "query_index"]
            data_Frame = data_Frame[data_Frame['score'] >= 0.0]
            # sortedFrame = dataFrame.sort_values(by= 'score', ascending=False , inplace=True)
            data_Frame.sort_values(by='score', ascending=False, inplace=True)
            data_append.append(data_Frame)
            # with open(self.outputFile, "a") as outFile:
            #     sortedFrame.to_string(outFile)
        final = pd.concat(data_append)
        final.to_csv('/home/iialab/Bhanu/PythonFiles/FinalCode/Final_csv1.csv', index=False)

    '''
        it retrieves the queryId from the query string. 
    '''

    def getqueryId(self, query):
        query_id = query.split("\n")
        return query_id[0]