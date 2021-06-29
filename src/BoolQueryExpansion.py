from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import numpy as np

class GetBoolQueryExpansion:
    def __init__(self, combined_query_list, search_index):
        self.combined_query_list = combined_query_list
        self.es = Elasticsearch()
        self.search_index = search_index
        self.score_list = list()

    def lowerCase(self, query):
        return " ".join(x.lower() for x in query.split())

    def stemmingwithlemmatization(self, query):
        wordnet_lemmatizer = WordNetLemmatizer()
        st = PorterStemmer()
        combinedString = ""
        split_list = query.split(" ")
        for splitword in split_list:
            stem = st.stem(splitword)
            lem = wordnet_lemmatizer.lemmatize(stem)
            if combinedString is "":
                combinedString = lem
            else:
                combinedString = combinedString + " " + lem
        return combinedString


    def removePunctuation(self, text_value):
        punc_symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
        for symbol in punc_symbols:
            text_value = np.char.replace(text_value, symbol, '')
        return text_value.tolist()

    '''
        Performs lemmatization by using WordNetLemmatizer.
    '''

    def lemmatization(self, query_list):
        output_str_list = list()
        for index, query in enumerate(query_list):
            expanded_query = query.split(',')
            for expquery in expanded_query:
                output = self.lowerCase(expquery)
                output = self.removePunctuation(output)
                output = self.stemmingwithlemmatization(output)
                output_str_list.append(output)
        return ','.join(output_str_list)


    def getScores(self):
        disease = ""
        gene = ""
        for query in self.combined_query_list:
            if query[0] is not None:
                disease = query[0].split('#')
            if query[1] is not None:
                gene = query[1].split('#')
            disease = self.lemmatization(disease)
            gene = self.lemmatization(gene)
            query_body = {
                'query': {
                    'query_string': {
                        'default_field': "concat_string",
                        'query': "(" + disease + ")" + " AND " + "(" + gene + ")"
                    }
                }
            }
            query_result = self.es.search(index=self.search_index, body=query_body, size=1000)
            self.score_list.append(query_result)
        return self.score_list

