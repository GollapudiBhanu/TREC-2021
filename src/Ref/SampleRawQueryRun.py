from QueryExpansion import QueryExpansion_2016, ExapnsionScore_2016
from elasticsearch import Elasticsearch
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import numpy as np
import re
import itertools
from itertools import chain
import pandas as pd
from Utilities import RandomFloat
import os
from pandas.core.common import flatten


class sample:


    def __init__(self, source_file):
        self.source_file = source_file
        self.query_list = []
        self.final_query_expan_list = []
        self.query_id_list = []
        self.final_documnet_id_list = []
        self.getscore()
        self.es = Elasticsearch(hosts=["localhost"])
        self.expansion_doc_id_list = []

    def lowerCase(self, query):
        return " ".join(x.lower() for x in query.split())

    def removePunctuation(self, text_value):
        punc_symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}\~\'\n"
        for symbol in punc_symbols:
            text_value = np.char.replace(text_value, symbol, '')
        return text_value.tolist()

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

    def getQueryExpansionCombination(self, out_file_path):
        current_query = [self.query_list[1]]
        for query_list in current_query:
            finalQuerylist = []
            finallist = []
            process_list = []
            for query in query_list:
                query = self.processQuery(query)
                process_list.append(query)
            for L in range(1, len(process_list) + 1):
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
            first_3_queries = finalQuerylist[:3]
            last_queres = finalQuerylist[3:len(finalQuerylist)]
            out_put_query_list = []
            for s in first_3_queries:
                out = " OR ".join(list(s))
                out_put_query_list.append(out)
            combinedlist = out_put_query_list + last_queres
            self.final_query_expan_list.append(combinedlist[::-1])
        self.getExpansionScores()
        self.removeDuplicates(out_file_path)


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


    def joinQuery(self, query_list):
        for index, inputquery in enumerate(query_list):
            pro_query = inputquery.split(' ')
            if len(pro_query) > 1:
                out_query =  " AND " .join(pro_query)
                out_query = '(' + out_query + ')'
                query_list[index] = out_query
        return query_list

    def getExpansionScores(self):
        final_document_id_list = []
        for index, queryexpansion in enumerate(self.final_query_expan_list):
            set_query_id_list = list(set(self.query_id_list))
            query_id = set_query_id_list[index]
            query_id_list = self.getQueryIdList(query_id, len(queryexpansion))
            for queryid, exp_query in zip(query_id_list, queryexpansion):
                if type(exp_query) is list:
                    sub_list = []
                    sub_score = []
                    for expansion in exp_query:
                        resu = self.retrieveScores(expansion)
                        sub_list.append(resu[0])
                        sub_score.append(resu[1])
                    final_document_id_list.append(sub_list)
                else:
                    res = self.retrieveScores(exp_query)
                    final_document_id_list.append(res[0])
            self.final_documnet_id_list.append(final_document_id_list)
            print("#################################################")

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

    def removeDuplicates(self, out_file_path):
        final_list = []
        for combine_doc_list in self.final_documnet_id_list:
            for index, combinational_list in enumerate(combine_doc_list):
                query_doc_list = list(flatten(combinational_list))
                final_list.append(query_doc_list)

            data = {'Doc_id': final_list}
            df = pd.DataFrame(data)
            df.drop_duplicates(keep='first', inplace=True)
            out = df['Doc_id'].values.tolist()
            #out1 = df['score'].values.tolist()
            #self.expansion_score_list.append(out1)
            self.expansion_doc_id_list.append(out)
        self.saveScore(out_file_path)

    def getQueryIdList(self, query_id, count):
        query_id_list = list()
        for _ in range(count):
            query_id_list.append(query_id)
        return query_id_list

    def saveScore(self, out_file_path):
        set_query_id_list = list(set(self.query_id_list))
        ran_obj = RandomFloat.GenerateRandomFloat()
        for query_id, docid_list in zip(set_query_id_list, self.expansion_doc_id_list):
            random_numbers = ran_obj.genereateFloatNumbers(len(docid_list))
            query_id_list = self.getQueryIdList(query_id, len(docid_list))
            for queryid, doc_id, score in zip(query_id_list, docid_list, random_numbers):
                mode = "a" if os.path.exists(out_file_path) else "w"
                with open(out_file_path, mode) as outfile:
                    outfile.write(str(queryid) + "\t" + doc_id + '\t' + str(score) + "\n")

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
            query_result = self.es.search(index='2016-trec-precision-medicine-final', body=query_body, size=1000)
            doc_list = []
            score = []
            for res in query_result['hits']['hits']:
                doc_list.append(res['_source']['DOCNO'])
                score.append(res['_score'])
            doc_id_list.append(doc_list)
            score_list.append(score)
        except:
            pass
        return doc_id_list, score_list

    def getscore(self):
        obj = QueryExpansion_2016.ExapandedQuery_2016(self.source_file,['queryID', 'summary', 'summary_keyword','summary_keyword_expansion'])
        results = obj.getExpansionQuery_2016()
        summary_tuple = results[0]
        self.query_id_list = summary_tuple[1]
        self.query_list = summary_tuple[0]
        self.getQueryExpansionCombination("/Output/Final_Raw_combinational_score_2016_1.csv")

obj = sample('/Data/2016_Quries/Manual_KeywordExtr_Query2016_aug3_B-reformated.csv')
