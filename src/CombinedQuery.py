from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import numpy as np


nltk.download("wordnet")

class GetCombinedBoolQuery:
    def __init__(self, query_path):
        self.query_path = query_path
        self.es = Elasticsearch()
        self.and_query_id_list = list()
        self.or_query_id_list = list()
        self.and_score_list = list()
        self.or_score_list = list()

    def lowerCase(self, query):
        return " ".join(x.lower() for x in query.split())

    def stemming(self, query):
        st = PorterStemmer()
        return st.stem(query)

    def removePunctuation(self, text_value):
        punc_symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"
        for symbol in punc_symbols:
            text_value = np.char.replace(text_value, symbol, '')
        return text_value.tolist()


    '''
        Performs lemmatization by using WordNetLemmatizer.
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

    def prepareANDBoolQuery(self, search_index):
        tree = ET.parse(self.query_path)
        root = tree.getroot()
        for element in root:
            disease = element[0].text
            gene = element[1].text
            disease_value = self.lemmatization(disease)
            gene_value = self.lemmatization(gene)
            query_body = {
                'query': {
                    'query_string': {
                        'default_field': "concat_string",
                        'query': (disease_value) + " AND " + (gene_value)
                    }
                }
            }
            query_result = self.es.search(index=search_index, body=query_body, size = 3000)
            self.and_score_list.append(query_result)
            self.and_query_id_list.append(element.attrib["number"])
        return self.and_score_list, self.and_query_id_list

    def prepareORBoolQuery(self, search_index):
        tree = ET.parse(self.query_path)
        root = tree.getroot()
        for element in root:
            disease = element[0].text
            gene = element[1].text
            disease_value = self.lemmatization(disease)
            gene_value = self.lemmatization(gene)
            query_body = {
                'query': {
                    'query_string': {
                        'default_field': "concat_string",
                        'query': (disease_value) + " OR " + (gene_value)
                    }
                }
            }
            query_result = self.es.search(index=search_index, body=query_body, size = 3000)
            self.or_score_list.append(query_result)
            self.or_query_id_list.append(element.attrib["number"])
        return self.or_score_list, self.or_query_id_list

    def prepareBoolQuery(self, search_index):
        and_query_results = self.prepareANDBoolQuery(search_index)
        or_query_results = self.prepareORBoolQuery(search_index)

        return and_query_results, or_query_results

