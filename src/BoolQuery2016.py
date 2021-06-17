from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import os
import pandas as pd


class GetBoolQuery_2016:
    def __init__(self, query_path):
        self.query_path = query_path
        self.es = Elasticsearch()
        self.scores = list()
        self.urls = list()
        self.query_id = list()
        self.prepareBoolQuery()

    def prepareBoolQuery(self):
        score_list = list()
        tree = ET.parse(self.query_path)
        root = tree.getroot()
        for element in root:
            query_body = {
                'query': {
                    'bool': {
                        'must': [{
                            'bool': {
                                'should': [
                                    {'match': {'journal-title': element[0].text}},
                                    {'match': {'article-type': element[0].text}},
                                    {'match':  {'article-title': element[0].text}},
                                    {'match':  {'abstract': element[0].text}},
                                    {'match': {'keywords': element[0].text}},
                                    {'match': {'subheading': element[0].text}},
                                    {'match': {'introduction': element[0].text}},
                                    {'match': {'conclusion': element[0].text}}
                                ]
                            },
                            'bool': {
                                'should': [
                                    {'match': {'journal': element[1].text}},
                                    {'match': {'article-type': element[1].text}},
                                    {'match': {'article-title': element[1].text}},
                                    {'match': {'abstract': element[1].text}},
                                    {'match': {'keywords': element[1].text}},
                                    {'match': {'subheading': element[1].text}},
                                    {'match': {'introduction': element[1].text}},
                                    {'match': {'conclusion': element[1].text}}
                                ]
                            }
                        }]
                    }
                }
            }
            query_result = self.es.search(index= "2016-trec-precision-medicine", body = query_body, size=1000)
            score_list.append(query_result)
            self.query_id.append(element.attrib["number"])

        #Need to work on this for 2016 data
        for result in score_list:
            url = list()
            score = list()
            for res in result['hits']['hits']:
                url.append(self.__prepareDocId(res['_source']['url']))
                score.append(res['_score'])
            self.scores.append(score)
            self.urls.append(url)
        self.savescores()

    '''
        It returns the document name from the provided URL.
    '''

    def __prepareDocId(self, url):
        head, tail = os.path.split(url)
        return tail

    def getQueryIdList(self, query_id, count):
        query_id_list = list()
        for _ in range(count):
            query_id_list.append(query_id)
        return query_id_list

    '''
        Prepare scores dpcument
    '''
    def savescores(self):
        for query_id, doc_id_list, score_list in zip(self.query_id, self.urls, self.scores):
            query_id_list = self.getQueryIdList(query_id, len(doc_id_list))
            for query_id, doc_id, score in zip(query_id_list, doc_id_list, score_list):
                if score > 0.0:
                    with open("./Output/BoolQuery_scores.csv", "a") as outFile:
                        outFile.write(str(query_id) + "\t" + doc_id + '\t' + str(score) + "\n")