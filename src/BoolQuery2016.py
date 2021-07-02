from elasticsearch import Elasticsearch
import os
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import numpy as np

nltk.download("wordnet")
nltk.download('stopwords')

class GetBoolQuery_2016:
    def __init__(self, query_list, query_id_list, search_index = "2016-trec-precision-medicine-final"):
        self.query_list = query_list
        self.query_id_list = query_id_list
        self.es = Elasticsearch()
        self.search_index = search_index
        self.stopword_list = stopwords.words('english')

    ''' 
        Input_attributes: query: String
        Description: converts string to lowercase.
        Return: String
    '''
    def lowerCase(self, query):
        if str(query) is None:
            return ""
        return " ".join(x.lower() for x in str(query).split())

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
        punc_symbols = "!\"#$%&()*+-,./:;<=>?@[\]^_`{|}~\n"
        for symbol in punc_symbols:
            text_value = np.char.replace(text_value, symbol, ' ')
        return text_value.tolist()

    ''' 
        Input_attributes: text_value: String
        Description: removes stopwords from string.
        Return: text_value: String
    '''
    def removeStopwords(self, text_value):
        result = []
        for text in text_value.split(" "):
            if text not in self.stopword_list:
                result.append(text)
        if len(result) == 0:
            return None
        return " ".join(set(result))

    '''
        Input_attributes: query: String
        Description: using WordNetLemmatizer 
        Return: text_value: String
    '''
    def lemmatization(self, query, type = "AND"):
        lower_query = self.lowerCase(query)
        lower_query = self.removePunctuation(lower_query)
        lower_query = self.removeStopwords(lower_query)
        if lower_query is None:
            return None
        query_list = [lower_query]
        wordnet_lemmatizer = WordNetLemmatizer()
        splitword = ""
        for index, word in enumerate(query_list):
            for word_ in word.split():
                stem_word = self.stemming(word_)
                lem_word = wordnet_lemmatizer.lemmatize(stem_word)
                if splitword is "":
                    splitword += lem_word
                else:
                    splitword = splitword + "," + lem_word
        if type == "AND":
            return self.prepareAndQuery(splitword)
        if type == "OR":
            return self.prepareORQuery(splitword)

    '''
        Input_attributes: query: String
        Description: Combine all strings using "AND" operator 
        Return: out_query_string: String
    '''
    def prepareAndQuery(self, splitword):
        out_query_string = ""
        for split in splitword.split(","):
            query_string = "(" + split + ")"
            if out_query_string is "":
                out_query_string = query_string
            else:
                out_query_string = out_query_string + "AND" + query_string
        return out_query_string

    '''
        Input_attributes: query: String
        Description: Combine all strings using "OR" operator 
        Return: out_query_string: String
    '''

    def prepareORQuery(self, splitword):
        out_query_string = ""
        for split in splitword.split(","):
            query_string = "(" + split + ")"
            if out_query_string is "":
                out_query_string = query_string
            else:
                out_query_string = out_query_string + "OR" + query_string
        return out_query_string

    '''
        Input_attributes: search_index: Index to search for query
        Description: 
            1. From query_path using ET, it retrieve element by and element.
            2. Using search_index, from Elastic search it retrieve the results.
        Return: 
            1.scores: []
            2.id_list: []
    '''
    def prepareBoolQuery(self, type):
        scores = list()
        id_list = list()
        for number, query in zip(self.query_id_list, self.query_list):
            query = self.lemmatization(query, type)
            if query == None:
                continue
            query_body = {
                'query': {
                    'query_string': {
                        'default_field': "concat_string",
                        'query': query
                    }
                }
            }
            query_result = self.es.search(index=self.search_index, body=query_body, size=3000)
            scores.append(query_result)
            id_list.append(number)
        return scores, id_list