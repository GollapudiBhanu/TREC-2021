import sys
import os
from typing import List, Any

from elasticsearch import Elasticsearch


class creatCorpus:

    def __init__(self):
        self.sourceDir = ""
        self.query_doc = ""
        self.es = Elasticsearch()
        self.doc_id = list()
        self.query_id = list()
        self.outputFile = '/home/iialab/Bhanu/PythonFiles/FinalCode/2019_Bm25_Top1000.txt'

    '''
        Returns the total number of files
    '''

    def __getTotalNumberOfFiles(self, n):
        #if len(sys.argv) < 2:
        #    print('[ERROR] Incomplete number of arguments')
        #elif len(sys.argv) >= 3:
         #   self.sourceDir = sys.argv[1]
        #self.sourceDir = "home/iialab/Bhanu/PythonFiles/FinalCode/TREC_2019_Basic_preprocessing"
        #root_folder = os.listdir(self.sourceDir)
        #total_count = len(root_folder)
        return 306238

    '''
        It returns the document name from the provided URL.
    '''

    def __prepareDocId(self, url):
        head, tail = os.path.split(url)
        self.doc_id.append(tail)

    '''
        1. From Elasticsearch it retrieves the document, with provided index.
        2. From Dict, with values, it forms and returns string.
    '''

    def __getdocumnetby(self, index):
        resultantString = ""
        try:
            res = self.es.get(index="2019-trec-precision-medicine", id=index)
            for key, value in res['_source'].items():
                if key == "url":
                    self.__prepareDocId(value)
                if value is None:
                    continue
                resultantString += value
            return resultantString
        except:
            print(str(index) + "error")

    '''
        It prepares a list (i...e corpus) with all the documents data.
    '''

    def prepareCorpus(self):
        number_of_documents = self.__getTotalNumberOfFiles(2)
        corpus = list()
        for index in range(number_of_documents):
            document = self.__getdocumnetby(index + 1)
            corpus.append(document)
        return corpus

    def getdocumentidlist(self):
        return self.doc_id
