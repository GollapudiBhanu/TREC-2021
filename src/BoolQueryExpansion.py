from elasticsearch import Elasticsearch

class GetBoolQueryExpansion:
    def __init__(self, combined_query_list, search_index):
        self.combined_query_list = combined_query_list
        self.es = Elasticsearch()
        self.search_index = search_index
        self.score_list = list()

    def getScores(self):
        disease = ""
        gene = ""
        for query in self.combined_query_list:
            if query[0] is not None:
                disease = query[0].split('-')
            if query[1] is not None:
                gene = query[1].split('-')
            diseaseString = ",".join(disease)
            geneString = ",".join(gene)
            combinedString = diseaseString + ',' + geneString
            query_body = {
                'query': {
                    'bool': {
                        'should': [
                            {'match': {'brief_title': combinedString}},
                            {'match': {'official_title': combinedString}},
                            {'match': {'brief_summary_text_block': combinedString}},
                            {'match': {'detailed_description_text_block': combinedString}},
                        ],
                        "minimum_should_match": 1
                    }
                }
            }
            query_result = self.es.search(index=self.search_index, body=query_body, size=1000)
            self.score_list.append(query_result)
        return self.score_list

