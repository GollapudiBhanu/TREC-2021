from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import numpy as np

nltk.download("wordnet")

class GetBoolQuery:
    def __init__(self, query_path):
        self.query_path = query_path
        self.es = Elasticsearch()

    ''' 
        Input_attributes: query: String
        Description: converts string to lowercase.
        Return: String
    '''
    def lowerCase(self, query):
        return " ".join(x.lower() for x in query.split())

    ''' 
        Input_attributes: query: String
        Description: Using Portstemmer, performs stemming.
        Return: String
    '''
    def stemming(self, query):
        st = PorterStemmer()
        return st.stem(query)

    ''' 
        Input_attributes: text_value: String
        Description: removes the punctuation from string.
        Return: list: []
    '''
    def removePunctuation(self, text_value):
        punc_symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"
        for symbol in punc_symbols:
            text_value = np.char.replace(text_value, symbol, '')
        return text_value.tolist()

    '''
        Input_attributes: query: String
        Description: using WordNetLemmatizer 
        Return: text_value: String
    '''
    def lemmatization(self, query):
        lower_query = self.lowerCase(query)
        lower_query = self.removePunctuation(lower_query)
        query_list = [lower_query]
        wordnet_lemmatizer = WordNetLemmatizer()
        splitword = ""
        for index, word in enumerate(query_list):
            for word_ in word.split():
                modified_string = str(word_).strip('()')
                for split_word in modified_string.split(','):
                    stem_word = self.stemming(split_word)
                    lem_word = wordnet_lemmatizer.lemmatize(stem_word)
                    if splitword is "":
                        splitword += lem_word
                    else:
                        splitword =  splitword + "," + lem_word
        return splitword

    '''
        Input_attributes: search_index: Index to search for query
        Description: 
            1. From query_path using ET, it retrieve element by and element.
            2. Using search_index, from Elastic search it retrieve the results.
        Return: 
            1.self.score_list: []
            2.self.query_id_list: []
    '''
    def prepareBoolQuery(self, search_index, query_type = " AND "):
        tree = ET.parse(self.query_path)
        root = tree.getroot()
        query_id_list = list()
        score_list = list()
        for element in root:
            disease = element[0].text
            gene = element[1].text
            disease_value = self.lemmatization(disease)
            gene_value = self.lemmatization(gene)
            query_body = {
                'query': {
                    'query_string': {
                        'default_field': "concat_string",
                        'query': (disease_value) + query_type + (gene_value)
                    }
                }
            }
            query_result = self.es.search(index=search_index, body=query_body, size = 3000)
            score_list.append(query_result)
            query_id_list.append(element.attrib["number"])
        return score_list, query_id_list