from elasticsearch import Elasticsearch
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import numpy as np
import re
import itertools
from itertools import chain
import pandas as pd
from Utilities import RandomFloat
from pandas.core.common import flatten
import os


class GetQueryExapnsionScore_2016:
    '''
        input:
            1.query_list: list of queries
            2.id_list: list of query_id
            3.search_index: Elastic search index
            4. exp_query_list: Query exoanison list
    '''
    def __init__(self, query_list,
                 id_list,
                 search_index,
                 exp_query_list = None):
        self.query_list = query_list
        self.query_id_list = id_list
        self.exp_query_list = exp_query_list
        self.es = Elasticsearch()
        self.search_index = search_index
        self.final_query_expan_list = []
        self.last3_query_list = []
        self.final_documnet_id_list = []
        self.final_score_list = []
        self.expansion_doc_id_list = []
        self.expansion_score_list = []

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
        punc_symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}\~\'\n"
        for symbol in punc_symbols:
            text_value = np.char.replace(text_value, symbol, '')
        return text_value.tolist()

    ''' 
        Input_attributes: inlist: list of strings
        Description: removes the spaces from string.
        Return: inlist: []
    '''
    def trimString(self, inlist):
        for index, sum in enumerate(inlist):
            str = re.sub('[ \t]+', '', sum)
            str = str.replace("'", "")
            inlist[index] = str
        return inlist


    '''
        Input_attributes: query: String
        Description: using WordNetLemmatizer and PorterStemmer, first perform the stemming and after it peforms Lemmatization.
        Return: text_value: String
    '''
    def stemmingwithlemmatization(self, query):
        wordnet_lemmatizer = WordNetLemmatizer()
        st = PorterStemmer()
        combinedString = " "
        split_list = query.split(" ")
        for splitword in split_list:
            stem = st.stem(splitword)
            lem = wordnet_lemmatizer.lemmatize(stem)
            if combinedString is " ":
                combinedString = lem
            else:
                combinedString = combinedString + " " + lem
        return combinedString

    ''' 
        Input_attributes: text_value: String
        Description: Perform Basic preprocessing on Query part.
        Return: list: []
    '''

    def processQuery(self, query):
        expanded_query = query.split(',')
        if len(expanded_query) == 1:
            expanded_query[0] = expanded_query[0].strip()
            output = self.process(expanded_query[0])
            return output
        else:
            output_str_list = list()
            for expquery in expanded_query:
                expquery = expquery.strip()
                output = self.process(expquery)
                output_str_list.append(output)
            return ','.join(output_str_list)

    '''
        1. First it combines Raw query using provided type
        2. It combines Raw query and query expansion with using "OR"
    '''
    def prepareFinalQuery(self, raw_query, expanded_query, type):
        raw_query_str = self.prepareANDRawQuery(raw_query, type)
        if expanded_query is None:
            return raw_query_str
        expanded_query_list = expanded_query.split(',')
        expanded_query_str = " OR ".join(expanded_query_list)
        outputstr = '(' + raw_query_str + ')' + " OR " + '(' + expanded_query_str + ')'
        return outputstr

    '''
        input: 
            expquery: Query term
        Description:
            It performs, basic preprocessing for the query 
    '''
    def process(self, expquery):
        expquery = expquery.split(" ")
        output_str = []
        for exp in expquery:
            exp = exp.strip()
            if exp is "":
                continue
            output = self.lowerCase(exp)
            output = self.removePunctuation(output)
            output = self.stemmingwithlemmatization(output)
            output_str.append(output)
        if len(output_str) > 1:
            #joinedStr = " AND ".join(output_str)
            # return "(" + joinedStr + ")"
            joinedStr = " ".join(output_str)
            return joinedStr
        else:
            return "".join(output_str)

    '''
        Join the query terms using type(AND or OR)
    '''
    def prepareANDRawQuery(self, raw_query, type):
        raw_query_list = raw_query.split(',')
        raw_queryStr = type.join(raw_query_list)
        return raw_queryStr

    '''
        it join the query list using 'AND' operator
    '''
    def joinQuery(self, query_list):
        for index, inputquery in enumerate(query_list):
            pro_query = inputquery.split(' ')
            if len(pro_query) > 1:
                out_query =  " AND " .join(pro_query)
                out_query = '(' + out_query + ')'
                query_list[index] = out_query
        return query_list

    '''
        Input:  
         out_file_path: file path where we need to save the output
         index: query index
         type: which list you need to take in to consideartion 
        
        Description:
            it performs the preprocessing of the query and using Itertools it perform the combination of terms in to the list.
                if type == 'First': we need to take first three terms in to the list.
                if type == 'last': we need to take last terms in to the list
            after that we can process queries and get expanison scores and save the scores in to the out_file_path.
            
                
    '''
    def getQueryExpansionCombination_2021(self, out_file_path, index):
        current_query_list = [self.query_list[index]]
        for query_list in current_query_list:
            finalQuerylist = []
            finallist = []
            process_list = []
            #query_list = query_list.split(',') # if all the queries treated as a single string separted with ,, we need to enable this line.
            for query in query_list:
                query = self.processQuery(query)
                process_list.append(query)
            rangeLength = len(process_list)
            if rangeLength >= 4:
                rangeLength = 4
            for L in range(1, rangeLength + 1):
                outlist = []
                for subset in itertools.combinations(process_list, L):
                    outlist.append(subset)
                finallist.append(outlist)
            for flist in finallist:
                outlist = []
                for fli in flist:
                    sa = list(fli)
                    sa = self.joinQuery(sa)
                    out = " AND ".join(sa)
                    out = '(' + out + ')'
                    outlist.append(out)
                finalQuerylist.append(outlist)
            first_3_queries = []
            last_queres = []
            if len(finalQuerylist) <= 3:
                first_3_queries = finalQuerylist[:1]
                last_queres = finalQuerylist[1:len(finalQuerylist)]
            else:
                first_3_queries = finalQuerylist[:2]
                last_queres = finalQuerylist[2:len(finalQuerylist)]
            out_put_query_list = []
            for s in first_3_queries:
                out = " OR ".join(list(s))
                out_put_query_list.append(out)
            combinedlist = out_put_query_list + last_queres
            #if type == 'last':
            #    self.final_query_expan_list.append(last_queres[::-1])
            #elif type == 'First':
            #    self.final_query_expan_list.append(out_put_query_list[::-1])
            self.final_query_expan_list.append(combinedlist[::-1])
        self.getExpansionScores()
        self.checkDuplicates()
        self.saveScore(out_file_path, index)

    '''
        It will check is there amy duplicates in the list.
    '''
    def checkDuplicates(self):
        for index, query_list in enumerate(self.final_documnet_id_list):
            set_list = list(set(query_list))
            if len(query_list) != len(set_list):
                print(str(index) + "I have duplicates")
    '''
        Input_attributes: search_index: Index to search for query
        Description: 
            1. From query_path using ET, it retrieve element by and element.
            2. Using search_index, from Elastic search it retrieve the results.
        Return: 
            score_list: []
    '''
    def getScores(self, query_type):
        score_list = []
        id_list = []
        for query, queryid in zip(self.query_list, self.query_id_list):
            baseQuery = query.split('#')
            expanded_query = None
            raw_query = self.processQuery(baseQuery[0])
            if len(baseQuery) > 1:
                expanded_query = self.processQuery(baseQuery[1])
            final_query = self.prepareFinalQuery(raw_query, expanded_query, query_type)
            print(final_query)
            query_body = {
                'query': {
                    'query_string': {
                        'default_field': "concat_string",
                        'query': final_query
                    }
                }
            }
            with open("/home/junhua/trec/Trec2021/Data/Metamap_Query.txt", "a") as outfile:
                outfile.write(str(queryid) + "\t" + str(query_body) + "\n")
            query_result = self.es.search(index=self.search_index, body=query_body, size=5000)
            score_list.append(query_result)
            if len(query_result) > 0:
                id_list.append(queryid)
        return score_list, id_list

    '''
        input: 
            query_id: Int 
            count: Int
        Description:
            count times, you need to repeat the same number in the list.
        Output:
            return the list of queryid with provided count length.
    '''
    def getQueryIdList(self, query_id, count):
        query_id_list = list()
        for _ in range(count):
            query_id_list.append(query_id)
        return query_id_list

    '''
        using Combinational query, we search the query in the Elasticsearch.
    '''

    def getExpansionScores(self):
        final_document_id_list = []
        final_score_list = []
        for index, queryexpansion in enumerate(self.final_query_expan_list):
            set_query_id_list = list(set(self.query_id_list))
            query_id = set_query_id_list[index]
            query_id_list = self.getQueryIdList(query_id, len(queryexpansion))
            for queryid, exp_query in zip(query_id_list, queryexpansion):
                if type(exp_query) is list:
                    sub_list = []
                    sub_score = []
                    for expansion in exp_query:
                        #resu = self.retrieveScores_2021(expansion) #if it is 2021 query we need to enable this.
                        resu = self.retrieveScores(expansion) #if it is 2016 or 2019 we need to use this.
                        sub_list.append(resu[0])
                        sub_score.append(resu[1])
                    final_document_id_list.append(sub_list)
                    final_score_list.append(sub_score)
                else:
                    #res = self.retrieveScores_2021(exp_query)
                    res = self.retrieveScores(exp_query)
                    final_document_id_list.append(res[0])
                    final_score_list.append(res[1])
            self.reteriveTop1000(final_document_id_list, final_score_list)

    '''
        Input: 
            document_id_list: list of Id's
            score_list: list of scores
        Description:
            It convert the given list in to Dataframe and retrieves the top2000 items.
    '''
    def reteriveTop1000(self, document_id_list, score_list):
        document_id_list = list(flatten(document_id_list))
        score_list = list(flatten(score_list))
        data = {'Documnet_Id': document_id_list,
                'Score_list': score_list}
        df = pd.DataFrame(data)
        df.sort_values(by=['Score_list'], inplace=True)
        df.drop_duplicates(subset=['Documnet_Id'], keep='first', inplace=True)
        df.duplicated(subset=['Documnet_Id'])
        df = df[:2000]
        documnet_id_1000 = df['Documnet_Id'].values.tolist()
        self.final_documnet_id_list.append(documnet_id_1000)

    '''
        Input: 
            final_query: Query to search in Elastic search.
        Description:
            It search the 'concat_string' term with the provided final_query, in the given search index.
    '''
    def retrieveScores(self, final_query):
        doc_id_list = []
        score_list = []
        query_body = {
            'query': {
                'query_string': {
                    'default_field': "concat_string",
                    'query': final_query
                }
            }
        }
        try:
            query_result = self.es.search(index=self.search_index, body=query_body, size=5000)
            doc_list = []
            score = []
            for res in query_result['hits']['hits']:
                doc_list.append(res['_source']['DOCNO'])
                #doc_list.append(self.__prepareDocId(res['_source']['url'])) # if it is 2019 or 2021.
                score.append(res['_score'])
            doc_id_list.append(doc_list)
            score_list.append(score)
        except:
            pass
        return doc_id_list, score_list

    '''
        It reterieves the docid from the provided URL.
    '''
    def __prepareDocId(self, url):
        head, tail = url.split("httpsclinicaltrialsgovshow")
        return tail

    '''
        Input: 
            out_file_path: outfile path, where we need to save the scores
            index: current index(queryid)
        Description:
            1. using QueryId, documnet_id, scores combine to gether we need to save this in to file.
            2. here we are using random_numbers, we genearte random numbers and save this number as a original score.
    '''
    def saveScore(self, out_file_path, index):
        set_query_id_list = list(set(self.query_id_list))
        currentQuery_id_list = [set_query_id_list[index]]
        ran_obj = RandomFloat.GenerateRandomFloat()
        for query_id, docid_list in zip(currentQuery_id_list, self.final_documnet_id_list):
            random_numbers = ran_obj.genereateFloatNumbers(len(docid_list))
            query_id_list = self.getQueryIdList(query_id, len(docid_list))
            for queryid, doc_id, score in zip(query_id_list, docid_list, random_numbers):
                mode = "a" if os.path.exists(out_file_path) else "w"
                with open(out_file_path, mode) as outfile:
                    outfile.write(str(queryid) + "\t" + doc_id + '\t' + str(score) + "\n")

    '''
        Input: 
            Index: index of current query
            out_file_path: output file path
            type: either 'First' or 'last'
         
    '''
    def getandsavescores(self, index, out_file_path):
        self.getQueryExpansionCombination_2021(out_file_path, index)



