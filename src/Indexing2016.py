'''
2019-trec-precision-medicine"

To run the script
           $python3 [filename] [source data collection folder path]

for example:
         $python3 /home/iialab/Bhanu/Indexing2019.py /home/iialab/Bhanu/2019_clinical_trials_new.0
'''

import json
from elasticsearch import Elasticsearch
import os


class Indexing_2016:

    def __init__(self, source_dir, search_index):
        self.es = Elasticsearch()
        self.search_index = search_index
        self.source_dir = source_dir#'/home/junhua/trec/FinalCode/TREC_2019_Basic_preprocessing'
        self.loadJsonDict()

    '''
    Set the default values for keys in the dict
    '''

    def setDefaultValuesForDict(self, data):
        data.setdefault("DOCNO", None)
        data.setdefault("journal-title", None)
        data.setdefault("article-type", None)
        data.setdefault("article-title", None)
        data.setdefault("abstract", None)
        data.setdefault("keywords", None)
        data.setdefault("subheading", None)
        data.setdefault("introduction", None)
        data.setdefault("conclusion", None)

    '''
        Prepares a dictionary with the vakues fromthe file
    '''

    def prepareDict(self, data):
        doc = {
            'DOCNO': data['DOCNO'],
            'journal-title': data['journal-title'],
            'article-type': data['article-type'],
            'article-title': data['article-title'],
            'abstract': data['abstract'],
            'keywords': data['keywords'],
            'subheading': data['subheading'],
            'introduction': data['introduction'],
            'conclusion': data['conclusion']
        }
        doc['concat_string'] = self.prepareConcatString(doc)
        return doc

    def prepareConcatString(self, doc):
        aTitle = doc['article-title']
        abstract = doc['abstract']
        keyword = doc['keywords']
        subheading = doc['subheading']
        introduction = doc['introduction']
        conclusion = doc['conclusion']

        if aTitle is None:
            aTitle = ""
        if abstract is None:
            abstract = ""
        if keyword is None:
            keyword = ""
        if subheading is None:
            subheading = ""
        if introduction is None:
            introduction = ""
        if conclusion is None:
            conclusion = ""

        return aTitle + " " + abstract + " " + keyword + " " + subheading+ " " + introduction + " " + conclusion

    '''
        1. list out all sub-directories and get folder by folder and get all xml files.
        2. Using elastic search indexing method it provides the index for the file with name '2019-trec-precision-medicine'
    '''

    def loadJsonDict(self):
        sub_dirs = os.listdir(self.source_dir)
        index_value = 0
        for folder in sub_dirs:
            sub_dirs = os.listdir(self.source_dir + '/' + folder + '/')
            for childDir in sub_dirs:
                jsonFiles = os.listdir(self.source_dir + '/' + folder + '/' + childDir)
                for fileIndex, file in enumerate(jsonFiles):
                    index_value += 1
                    dict = self.loadJson(self.source_dir + '/' + folder + '/' + childDir + '/' + file)
                    self.indexing(dict, index_value)

    def loadJson(self, sourceFile):
        jsonFile = open(sourceFile)
        data = json.load(jsonFile)
        self.setDefaultValuesForDict(data)
        return data

    def indexing(self, data, index_value):
        doc = self.prepareDict(data)
        res = Elasticsearch().index(index=self.search_index, id=int(index_value), body=doc)
        print(index_value)
        print(res['result'])
        print("####################################")


