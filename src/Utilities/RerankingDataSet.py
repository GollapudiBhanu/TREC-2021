import pandas as pd
from QueryExpansion import QueryExpansion_2016, ExapnsionScore_2016
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import numpy as np
from pandas.core.common import flatten
from Utilities import TextPreprocessing
import json

'''
This file is used to prepare the Reranking Json file.
'''
class Dataset:

    '''
        Input:
            judgement_path: TREC: judgement file path
            query_file_path: Query file path
    '''
    def __init__(self,judgement_path, query_file_path):
        self.judgement_path = judgement_path
        self.query_file_path = query_file_path
        self.query_id_list = []

    '''
        This method is used to read the individual lists from judgement_path
    '''
    def read_file(self):
        #Judgement path
        df = pd.read_csv(self.judgement_path, sep = ',')
        df.coloumns = ['query_id','Document_id','Score','Concat_string']
        df['group_id'] = df.groupby(['query_id']).grouper.group_info[0]
        df = df.groupby(["group_id"]).agg(lambda x: x.tolist())
        df = df.head(1000)
        query_id_list = df['query_id'].tolist()
        document_list = df['Document_id'].tolist()
        revlence_list = df['Score'].tolist()
        document_string_list = df['Concat_string'].tolist()
        return query_id_list, document_list, revlence_list, document_string_list

    '''
        This method is used to read the Query lists from query file path
    '''
    def read_query_file(self):
        df = pd.read_csv('/home/junhua/trec/Trec2021/Output/2016QueryOutput/qrels-treceval-2016.csv')
        df.coloumns = ['QueryID','Main_text','raw_list','Expansion_list']
        df['combined_string'] = df[['raw_list', 'Expansion_list']].agg(','.join, axis=1)

    '''
        it prepared JSON file using judgement file dict and query dict.
    '''
    def prepare2016Data(self):
        document_dict_list = self.preparedocumentdict_list()
        query_dict_list = self.preparequeryDict()
        finaldict = []
        for query_id in self.query_id_list:
            try:
                query = list(filter(lambda c: c['query_id'] == query_id, query_dict_list))[0]
                doc = list(filter(lambda c: c['query_id'] == query_id, document_dict_list))
                query['documents'] = doc[0]['document_Text']
                finaldict.append(query)
            except:
                continue
        dict = {'rankingProblems': finaldict}
        with open('/home/junhua/trec/Trec2021/Output/2016QueryOutput/2016Reranking/Bhanu_ReRanking.json', 'a') as f:
            json.dump(dict, f, indent=4)

    '''
        it prepared JSON file using judgement file dict and query dict(query summary).
    '''
    def prepare2016summaryData(self):
        document_dict_list = self.preparedocumentdict_list()
        query_dict_list = self.prepareSummaryQueryDict()
        finaldict = []

        for querydict, document_dict_list in zip(query_dict_list, document_dict_list):
            qdict = querydict
            qdict['documents'] = document_dict_list
            finaldict.append(qdict)
        dict = {'rankingProblems': finaldict}
        with open('/home/junhua/trec/Trec2021/Output/2021Output/Run2/RUN2_Reranking.json', 'a') as f:
            json.dump(dict, f, indent=4)

    '''
        This method is used to prepare the document data dict list 
    '''
    def preparedocumentdict_list(self):
        result = self.read_file()
        query_id_list = result[0]
        document_list = result[1]
        revelent_score = result[2]
        concat_list = result[3]

        final_document_list = []

        for rev_list, query_list, doc_list, str_list in zip(revelent_score, query_id_list, document_list, concat_list):
            intial_list = []
            for revscore, query_id, id, concat_str, i in zip(rev_list, query_list, doc_list, str_list, range(0,1000)):
                sample_dict = {}
                sample_dict['relevance'] = 1
                sample_dict['docText'] = concat_str
                sample_dict['doc-id'] = id
                #sample_dict['query_id'] = query_id
                intial_list.append(sample_dict)
            docdict = {'query_id': query_list[0],
                       'document_Text': intial_list}
            final_document_list.append(docdict)

        return final_document_list

    '''
        This method is used to prepare the query summary dict.
    '''
    def prepareSummaryQueryDict(self):
        obj = QueryExpansion_2016.ExapandedQuery_2016(self.query_file_path,
                                                      ['QueryID', 'Main_text', 'raw_list', 'Expansion_list'])
        results = obj.getSummaryText()
        current_query_list = results[0]
        query_id_list = results[1]
        final_query_list = []
        for id, query_list in zip(query_id_list, current_query_list):
            process_list = []
            query_dict = {}
            for query in query_list:
                obj = TextPreprocessing.Preprocessing()
                query = obj.preprocess(query)
                process_list.append(query)
            query_dict['queryText'] = " ".join(process_list)
            query_dict['query_id'] = id
            final_query_list.append(query_dict)
        return final_query_list

    '''
        This method is used to prepare the query text dict.
    '''
    def preparequeryDict(self):
        obj = QueryExpansion_2016.ExapandedQuery_2016(self.query_file_path,
                                                      ['Sl.no','QueryID','Main_text','raw_list','Expansion_list'])
        results = obj.getExpansionQuery_2021()
        summary_tuple = results[0]
        current_query_list = summary_tuple[0]
        query_id_list = summary_tuple[1]
        final_query_list = []
        self.query_id_list = query_id_list
        for id, query_list in zip(query_id_list, current_query_list):
            process_list = []
            query_dict = {}
            for query in query_list:
                query = self.process(query)
                process_list.append(query)
            query_dict['queryText'] = " ".join(process_list)
            query_dict['query_id'] = id
            final_query_list.append(query_dict)
        '''
           data = {'QueryId': query_id_list,
                'raw_query':summary_tuple[2],
                'Expansion_Query': current_query_list,
                'Processed_Query': final_query_list}
        
        df = pd.DataFrame(data)
        df.to_csv('/home/junhua/Downloads/preprocessed_raw-exp_manualKW_joined_1-75_B-reformated_Aug12_4.csv')
        '''
        return final_query_list
    '''
        Basic preprocessing
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
            joinedStr = " ".join(output_str)
            return joinedStr
        else:
            return "".join(output_str)


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


#obj = Dataset('/home/junhua/trec/Trec2021/Output/2016QueryOutput/2016Reranking/Bhanu-All_merge_concatstring.csv',
#              '/home/junhua/trec/Trec2021/Data/2016_Quries/Manual_KeywordExtr_Query2016_aug3-2_B-reformated.csv')

#obj.prepare2016summaryData()

#obj.prepare2016Data()







