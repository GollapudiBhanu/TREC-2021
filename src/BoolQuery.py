from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET


class GetBoolQuery:
    def __init__(self, query_path):
        self.query_path = query_path
        self.es = Elasticsearch()

    def prepareBoolQuery(self):
        tree = ET.parse(self.query_path)
        root = tree.getroot()

        for element in root:
            query_body = {
                'query': {
                    'bool': {
                        'must': [{
                            'bool': {
                                'should': [
                                    {'match': {'brief_title': element[0].text}},
                                    {'match': {'official_title': element[0].text}},
                                    {'match':  {'brief_summary_text_block': element[0].text}},
                                    {'match':  {'detailed_description_text_block': element[0].text}},
                                ]
                            },
                            'bool': {
                                'should': [
                                    {'match': {'brief_title': element[1].text}},
                                    {'match': {'official_title': element[1].text}},
                                    {'match': {'brief_summary_text_block': element[1].text}},
                                    {'match': {'detailed_description_text_block': element[1].text}},
                                ]
                            }
                        }]
                    }
                }
            }
