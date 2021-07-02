from elasticsearch import Elasticsearch
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import numpy as np

class GetBoolQueryExpansion:
    def __init__(self, combined_query_list, search_index):
        self.combined_query_list = combined_query_list
        self.es = Elasticsearch()
        self.search_index = search_index
        self.score_list = list()

    ''' 
        Input_attributes: query: String
        Description: converts string to lowercase.
        Return: String
    '''
    def lowerCase(self, query):
        return " ".join(x.lower() for x in query.split())

    ''' 
        Input_attributes: text_value: String
        Description: removes the punctuation from string.
        Return: list: []
    '''
    def removePunctuation(self, text_value):
        punc_symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
        for symbol in punc_symbols:
            text_value = np.char.replace(text_value, symbol, '')
        return text_value.tolist()


    '''
        Input_attributes: query: String
        Description: using WordNetLemmatizer and PorterStemmer, first perform the stemming and after it peforms Lemmatization.
        Return: text_value: String
    '''
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

    ''' 
        Input_attributes: text_value: String
        Description: Perform Basic preprocessing on Query part.
        Return: list: []
    '''

    def processQuery(self, query_list):
        output_str_list = list()
        for index, query in enumerate(query_list):
            expanded_query = query.split(',')
            for expquery in expanded_query:
                output = self.lowerCase(expquery)
                output = self.removePunctuation(output)
                output = self.stemmingwithlemmatization(output)
                output_str_list.append(output)
        return ','.join(output_str_list)

    '''
        Input_attributes: search_index: Index to search for query
        Description: 
            1. From query_path using ET, it retrieve element by and element.
            2. Using search_index, from Elastic search it retrieve the results.
        Return: 
            score_list: []
    '''
    def getScores(self, query_type = " AND "):
        disease = ""
        gene = ""
        score_list = []
        for query in self.combined_query_list:
            if query[0] is not None:
                disease = query[0].split('#')
            if query[1] is not None:
                gene = query[1].split('#')
            disease = self.processQuery(disease)
            gene = self.processQuery(gene)
            query_body = {
                'query': {
                    'query_string': {
                        'default_field': "concat_string",
                        'query': "(" + disease + ")" + query_type + "(" + gene + ")"
                    }
                }
            }
            query_result = self.es.search(index=self.search_index, body=query_body, size=1000)
            score_list.append(query_result)
        return score_list

