from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import numpy as np
import SaveScore


nltk.download("wordnet")

class GetCombinedBoolQuery:
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
        Description: Using PorterStemmer, performs stemming operation on Query string.
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
        Description: Using WordNetLemmatizer, Performs lemmatization by using WordNetLemmatizer.
        Return: String
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
        Input_attributes: 
            1.search_index: Index to search for query
            2.type: type of operation while combing Queries.
        Description: 
            1. From query_path using ET, it retrieve element by and element.
            2. Using search_index, from Elastic search it retrieve the results.
        Return: 
            1.score_list: []
            2.id_list: []
    '''
    def prepareQuery(self, search_index, type):
        tree = ET.parse(self.query_path)
        root = tree.getroot()
        score_list = []
        id_list = []
        for element in root:
            disease = element[0].text
            gene = element[1].text
            disease_value = self.lemmatization(disease)
            gene_value = self.lemmatization(gene)
            query_body = {
                'query': {
                    'query_string': {
                        'default_field': "concat_string",
                        'query': (disease_value) + type + (gene_value)
                    }
                }
            }
            query_result = self.es.search(index=search_index, body=query_body, size = 3000)
            score_list.append(query_result)
            id_list.append(element.attrib["number"])
        return score_list, id_list

    def prepareBoolQuery(self, search_index):
        and_query_results = self.prepareQuery(search_index, " AND ")
        or_query_results = self.prepareQuery(search_index, " OR ")

        return and_query_results, or_query_results