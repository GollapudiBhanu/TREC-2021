from gensim import corpora
import math
import pandas as pd

'''
We didn't use this file, for reference purpose i...,e how to calculate BM25 score I am keeping this.
'''

class BM25:
    def __init__(self, corpus_list, delimiter='|'):
        self.dictionary = corpora.Dictionary()
        self.DF = {}
        self.delimiter = delimiter
        self.DocTF = []
        self.queryId = []
        self.DocIDF = {}
        self.N = 0
        self.DocAvgLen = 0
        self.corpus = corpus_list
        self.DocLen = []
        self.buildDictionary()
        self.TFIDF_Generator()

    def buildDictionary(self):
        raw_data = []
        for line in self.corpus:
            raw_data.append(line.strip().split(self.delimiter))
        self.dictionary.add_documents(raw_data)

    def TFIDF_Generator(self, base=math.e):
        docTotalLen = 0
        for line in self.corpus:
            doc = line.strip().split(self.delimiter)
            docTotalLen += len(doc)
            self.DocLen.append(len(doc))
            bow = dict([(term, freq * 1.0 / len(doc)) for term, freq in self.dictionary.doc2bow(doc)])
            for term, tf in bow.items():
                if term not in self.DF:
                    self.DF[term] = 0
                self.DF[term] += 1
            self.DocTF.append(bow)
            self.N = self.N + 1
        for term in self.DF:
            self.DocIDF[term] = math.log((self.N - self.DF[term] + 0.5) / (self.DF[term] + 0.5), base)
        self.DocAvgLen = docTotalLen / self.N

    def BM25Score(self, query_name, k1=1.5, b=0.75):
        query_bow = self.dictionary.doc2bow(query_name)
        scores = []
        for idx, doc in enumerate(self.DocTF):
            commonTerms = set(dict(query_bow).keys()) & set(doc.keys())
            tmp_score = []
            doc_terms_len = self.DocLen[idx]
            for term in commonTerms:
                upper = (doc[term] * (k1 + 1))
                below = ((doc[term]) + k1 * (1 - b + b * doc_terms_len / self.DocAvgLen))
                tmp_score.append(self.DocIDF[term] * upper / below)
            scores.append(sum(tmp_score))
        return scores

    def TFIDF(self):
        tfidf_list = []
        for doc in self.DocTF:
            doc_tfidf = [(term, tf * self.DocIDF[term]) for term, tf in doc.items()]
            doc_tfidf.sort()
            tfidf_list.append(doc_tfidf)
        return tfidf_list

    def Items(self):
        items = self.dictionary.items()
        return items

    def getBM25Score(self, query_list, document_id_list):
        data_frame_collection = list()
        for single_query in query_list:
            query_id = self.getqueryId(single_query)
            scores = self.BM25Score(single_query.split())
            query_id_list = self.getQueryIdList(query_id, len(scores))
            zipData = zip(query_id_list, document_id_list, scores)
            data_frame = pd.DataFrame(zipData)
            data_frame.columns = ["query_id", "doc_id", "score"]
            data_frame['score'] = data_frame['score'].astype(float)
            data_frame = data_frame[data_frame['score'] > 0.0]
            data_frame_collection.append(data_frame)
        final = pd.concat(data_frame_collection)
        final.to_csv('./Output/Final_score.csv', index=False)

    def getExpandedBM25Score(self, query_list, document_id_list, expanded_query_id_list=[]):
        data_frame_collection = list()
        for single_query, query_id in zip(query_list, expanded_query_id_list):
            scores = self.BM25Score(single_query.split())
            query_id_list = self.getQueryIdList(query_id, len(scores))
            zipData = zip(query_id_list, document_id_list, scores)
            data_frame = pd.DataFrame(zipData)
            data_frame.columns = ["query_id", "doc_id", "score"]
            data_frame['score'] = data_frame['score'].astype(float)
            data_frame = data_frame[data_frame['score'] > 0.0]
            data_frame_collection.append(data_frame)
        final = pd.concat(data_frame_collection)
        final.to_csv('./Output/Expanded_Final_score.csv', index=False)

    '''
        Returns a count items in a list, with provided queryId. 
    '''

    def getQueryIdList(self, query_id, count):
        query_id_list = list()
        for _ in range(count):
            query_id_list.append(query_id)
        return query_id_list

    '''
        it retrieves the queryId from the query string. 
    '''

    def getqueryId(self, query):
        query_id = query.split("\n")
        return query_id[0]

    def getQueryExpandID(self, query_list):
        topic_id_list = query_list['TopicID']
        self.query_expand_id = topic_id_list
