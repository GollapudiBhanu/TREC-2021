import nltk
from nltk.stem import WordNetLemmatizer
from elasticsearch import Elasticsearch


nltk.download("wordnet")

'''
We didn't use this file, for reference purpose(How to use elastic search query search), I am keeping this.
'''

class BoolQueryScore:

    def __init__(self, query_list, query_id_list, search_index):
        self.query_list = query_list
        self.query_id_list = query_id_list
        self.es = Elasticsearch()
        self.search_index = search_index
        self.score_list = []
        self.id_list = []

    def lowerCase(self, query):
        return " ".join(x.lower() for x in query.split())

    '''
        Performs lemmatization by using WordNetLemmatizer.
    '''

    def lemmatization(self, query):
        lower_query = self.lowerCase(query)
        query_list = [lower_query]
        wordnet_lemmatizer = WordNetLemmatizer()
        splitword = ""
        for index, word in enumerate(query_list):
            for word_ in word.split():
                modified_string = str(word_).strip('()')
                for spli in modified_string.split(','):
                    y = wordnet_lemmatizer.lemmatize(spli)
                    if splitword is "":
                        splitword += y
                    else:
                        splitword = splitword + "," + y
        return splitword

    def constructBoolQuery(self, query):
        lem_query_value = self.lemmatization(query)
        query_body = {
            'query': {
                'bool': {
                    'should': [
                        {'match': {'brief_title': lem_query_value}},
                        {'match': {'official_title': lem_query_value}},
                        {'match': {'brief_summary_text_block': lem_query_value}},
                        {'match': {'detailed_description_text_block': lem_query_value}},
                    ],
                    "minimum_should_match": 1
                }
            }
        }
        return query_body

    def constructBoolMustQuery(self, query):
        lem_query_value = self.lemmatization(query)
        query_body = {
            'query': {
                'bool': {
                    'should': [
                        {'match': {'brief_title': lem_query_value}},
                        {'match': {'official_title': lem_query_value}},
                        {'match': {'brief_summary_text_block': lem_query_value}},
                        {'match': {'detailed_description_text_block': lem_query_value}},
                    ],
                    "minimum_should_match": 1
                }
            }
        }
        return query_body

    def getScore(self):
        for query_id, query in zip(self.query_id_list, self.query_list):
            bool_query = self.constructBoolQuery(query)
            query_result = self.es.search(index=self.search_index, body=bool_query, size=1000)
            self.score_list.append(query_result)
            self.id_list.append(query_id)
        return self.score_list, self.id_list