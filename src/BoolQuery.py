from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import os
import pandas as pd


class GetBoolQuery:
    def __init__(self, query_path):
        self.query_path = query_path
        self.es = Elasticsearch()
        self.query_id_list = list()
        self.score_list = list()

    def prepareBoolQuery(self, search_index):
        tree = ET.parse(self.query_path)
        root = tree.getroot()
        for element in root:
            value = element[0].text + ',' + element[1].text
            query_body = {
                'query': {
                    'bool': {
                        'should': [
                            {'match': {'brief_title': value}},
                            {'match': {'official_title': value}},
                            {'match': {'brief_summary_text_block': value}},
                            {'match': {'detailed_description_text_block': value}},
                        ],
                        "minimum_should_match": 1
                    }
                }
            }
            query_result = self.es.search(index=search_index, body=query_body, size = 1000)
            self.score_list.append(query_result)
            self.query_id_list.append(element.attrib["number"])
        return self.score_list, self.query_id_list

