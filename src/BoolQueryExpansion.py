from elasticsearch import Elasticsearch
import QueryExpansionList


class GetBoolQuery_2016:
    def __init__(self, querys):
        self.query_list = querys
        self.es = Elasticsearch()
        self.query()

    def query(self):
        disease = ""
        gene = ""
        score_list = []
        for query in self.query_list:
            if query[0] is not None:
                disease = query[0].split('-')
            if query[1] is not None:
                gene = query[1].split('-')
            query_body = {
                'query': {
                    'bool': {
                        'filter': {
                            'bool': {
                                'must': [{
                                    'bool': {
                                        'should': [{
                                            'terms': {
                                                'journal-title': disease
                                            },
                                            'terms': {
                                                'article-type': disease
                                            },
                                            'terms': {
                                                'article-title': disease
                                            },
                                            'terms': {
                                                'abstract': disease
                                            },
                                            'terms': {
                                                'keywords': disease
                                            },
                                            'terms': {
                                                'subheading': disease
                                            },
                                            'terms': {
                                                'introduction': disease
                                            },
                                            'terms': {
                                                'conclusion': disease
                                            }
                                        }]
                                    },
                                    'bool': {
                                        'should': [{
                                            'terms': {
                                                'journal-title': gene
                                            },
                                            'terms': {
                                                'article-type': gene
                                            },
                                            'terms': {
                                                'article-title': gene
                                            },
                                            'terms': {
                                                'abstract': gene
                                            },
                                            'terms': {
                                                'keywords': gene
                                            },
                                            'terms': {
                                                'subheading': gene
                                            },
                                            'terms': {
                                                'introduction': gene
                                            },
                                            'terms': {
                                                'conclusion': gene
                                            }
                                        }]
                                    },

                                }]
                            }
                        }
                    }
                }
            }
            query_result = self.es.search(index="2016-trec-precision-medicine", body=query_body, size=1000)
            score_list.append(query_result)
        for result in score_list:
            url = list()
            score = list()
            for res in result['hits']['hits']:
                print(res['_source']['url'])
                print(res['_score'])

expanded_query = QueryExpansionList.ExapndedQuery('./Data/topics2019_expanded.csv')
query_list = expanded_query.getGroupedData()
query_obj = GetBoolQuery_2016(query_list)
