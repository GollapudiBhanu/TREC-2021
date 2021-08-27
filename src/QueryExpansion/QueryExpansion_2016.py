import pandas as pd
import re
import os
import numpy as np

class ExapandedQuery_2016:

    def __init__(self, query_file_path, coloumn_list):
        self.query_file_path = query_file_path
        self.coloumn_list = coloumn_list
        self.exp_query_list = []

    '''
        Reads data from provided query_path using Pandas.
    '''

    def readfile(self):
        expansion_dataframe = pd.read_csv(self.query_file_path)
        return expansion_dataframe

    '''
        Extract and return the TopicId list from using 'TopicID' the dataframe.        
    '''

    def getTopicIDList(self):
        expansion_dataframe = self.readfile()
        topic_id_list = expansion_dataframe[self.coloumn_list[0]]
        return topic_id_list

    '''
        It separates the "gene" and "disease" values from the QueryId.
    '''

    def groupByTopicId(self):
        topic_id_list = list()
        topic_name_list = list()
        topic_list = self.getTopicIDList()
        for topic in topic_list:
            if "summary" in topic:
                topic_id = topic.split("summary")
                topic_name_list.append("summary")
                topic_id = str(topic_id[0]).split('T')
                topic_id_list.append(int(topic_id[1]) + 1)
            elif "description" in topic:
                topic_id = topic.split("description")
                topic_name_list.append("description")
                topic_id = str(topic_id[0]).split('T')
                topic_id_list.append(int(topic_id[1]) + 1)
            elif "note" in topic:
                topic_id = topic.split("note")
                topic_name_list.append("note")
                topic_id = str(topic_id[0]).split('T')
                topic_id_list.append(int(topic_id[1]) + 1)
        return topic_id_list, topic_name_list

    '''
        Add Extra column to the dataframe.
    '''

    def addColoumnToDataFrame(self):
        expansion_dataFrame = self.readfile()
        topics = self.groupByTopicId()
        topic_id_list = topics[0]
        topic_name_list = topics[1]
        expansion_dataFrame["group_topic_id"] = topic_id_list
        expansion_dataFrame["TopicName"] = topic_name_list
        return expansion_dataFrame

    '''
        Prepares the TopicId list with list of list topic id's
    '''

    def getTopicIdList(self, topic_id_lsit):
        topics = list()
        for topic_list in topic_id_lsit:
            topics.append(str(topic_list[0]))
        return topics

    def getGroupedData(self):
        df = self.addColoumnToDataFrame()
        df['entities'] = df[self.coloumn_list[1]].astype(str)
        df['expend_query_entity'] = df[self.coloumn_list[2]].astype(str)
        trimlist = df['expend_query_entity'].tolist()
        #trimlist = self.trimString(trimlist)
        df['expend_query_entity'] = trimlist
        df['combined'] = df[['entities', 'expend_query_entity']].agg('#'.join, axis=1)
        df['Topics'] = df['TopicName']
        summary = df.groupby(['TopicName']).get_group("summary")
        description = df.groupby(['TopicName']).get_group("description")
        notes = df.groupby(['TopicName']).get_group("note")

        summary_query_expansion = summary['combined'].tolist()
        summary_topic_id_list = summary['group_topic_id'].tolist()
        summary_basic_query = summary['entities'].tolist()
        summary_tuple = (summary_query_expansion, summary_topic_id_list, summary_basic_query)

        description_query_expansion = description['combined'].tolist()
        description_topic_id_list = description['group_topic_id'].tolist()
        description_basic_query = description['entities'].tolist()
        description_tuple = (description_query_expansion, description_topic_id_list, description_basic_query)

        notes_query_expansion = notes['combined'].tolist()
        notes_topic_id_list = notes['group_topic_id'].tolist()
        notes_basic_query = notes['entities'].tolist()
        note_tuple = (notes_query_expansion, notes_topic_id_list, notes_basic_query)

        return (summary_tuple, description_tuple, note_tuple, notes_basic_query)

    def getCombinedGroupeddata(self):
        df = pd.read_csv(self.query_file_path)
        column_list = []
        for name in self.coloumn_list:
            column_list.append(name)
        df.columns = column_list
        df = df.dropna()
        df['queryID'] = pd.to_numeric(df['queryID'])
        df.sort_values(by=['queryID'], ascending=True, inplace=True)
        df['summary_combined'] = df[['summary_keyword', 'summary_keyword_expansion']].agg('#'.join, axis=1)
        summary_query_expansion =  df['summary_combined'].tolist()
        summary_topic_id_list = df['queryID'].tolist()
        summary_basic_query = df['summary_keyword'].tolist()
        summary_tuple = (summary_query_expansion, summary_topic_id_list, summary_basic_query)
        return (summary_tuple, None, None)

    def getExpansionQuery_2016(self):
        df = pd.read_csv(self.query_file_path)
        column_list = []
        for name in self.coloumn_list:
            column_list.append(name)
        df.columns = column_list
        df['queryID'] = pd.to_numeric(df['queryID'])
        query_id_list = df['queryID'].tolist()
        df.sort_values(by=['queryID'], ascending=True, inplace=True)
        summary_expansion = df['summary_keyword_expansion'].tolist()
        summary_expansion = self.removeNone(summary_expansion)
        df['final_summary_keyword_expansion'] = summary_expansion
        df['summary_combined'] = df[['summary_keyword', 'final_summary_keyword_expansion']].agg(','.join, axis=1)
        df["group_id"] = df.groupby(["queryID"]).grouper.group_info[0]
        df = df.groupby(['group_id']).agg(lambda x: x.tolist())
        summary_query_list = df['summary_keyword'].tolist()
        summary_query_list = self.joinlist(summary_query_list)
        summary_combined = df['summary_combined'].tolist()
        summary_combined = self.joinlist(summary_combined)
        summary_tuple = (summary_combined, query_id_list, summary_query_list)
        return (summary_tuple, None, None)

    def getExpansionQuery_2021(self):
        df = pd.read_csv(self.query_file_path, sep=',')
        column_list = []
        for name in self.coloumn_list:
            column_list.append(name)
        df.columns = column_list
        df['QueryID'] = pd.to_numeric(df['QueryID'])
        query_id_list = df['QueryID'].tolist()
        df.sort_values(by=['QueryID'], ascending=True, inplace=True)
        summary_expansion = df['Expansion_list'].tolist()
        summary_expansion = self.removeNone(summary_expansion)
        df['final_Expansion_list'] = summary_expansion
        df['summary_combined'] = df[['raw_list', 'final_Expansion_list']].agg(','.join, axis=1)
        df["group_id"] = df.groupby(["QueryID"]).grouper.group_info[0]
        df = df.groupby(['group_id']).agg(lambda x: x.tolist())
        print(df.head(10))
        summary_query_list = df['raw_list'].tolist()
        summary_query_list = self.joinlist(summary_query_list)
        summary_combined = df['summary_combined'].tolist()
        summary_combined = self.joinlist(summary_combined)
        summary_tuple = (summary_combined, query_id_list, summary_query_list)
        return (summary_tuple, None, None)


    def getSummaryText(self):
        df = pd.read_csv(self.query_file_path, sep=',')
        column_list = []
        for name in self.coloumn_list:
            column_list.append(name)
        df.columns = column_list
        df['QueryID'] = pd.to_numeric(df['QueryID'])
        query_id_list = df['QueryID'].tolist()
        df.sort_values(by=['QueryID'], ascending=True, inplace=True)
        maintext = df['Main_text'].tolist()
        return (maintext, query_id_list)


    def getRawQuery(self):
        df = pd.read_csv(self.query_file_path, sep=',')
        column_list = []
        for name in self.coloumn_list:
            column_list.append(name)
        df.columns = column_list
        df['QueryID'] = pd.to_numeric(df['QueryID'])
        query_id_list = df['QueryID'].tolist()
        df.sort_values(by=['QueryID'], ascending=True, inplace=True)
        rawQuery = df['raw_list'].tolist()
        summarytuple = (None, query_id_list, rawQuery)
        return (summarytuple, None, None)


    def getExpansionQuery(self):
        df = pd.read_csv(self.query_file_path)
        column_list = []
        for name in self.coloumn_list:
            column_list.append(name)
        df.columns = column_list
        df.drop(labels=['description','description_keyword','note','note_keyword'], axis=1, inplace=True)
        df.dropna(inplace=True)
        df = df.mask(df.eq('None')).dropna()
        df['queryID'] = pd.to_numeric(df['queryID'])
        query_id_list = df['queryID'].tolist()
        df.sort_values(by=['queryID'], ascending=True, inplace=True)
        df["group_id"] = df.groupby(["queryID"]).grouper.group_info[0]
        df = df.groupby(['group_id']).agg(lambda x: x.tolist())
        summary_expansion_list = df['summary_keyword_expansion'].tolist()
        summary_query_list = df['summary_keyword'].tolist()
        summary_tuple = (summary_expansion_list, query_id_list, summary_query_list)
        return (summary_tuple, None, None)

    def joinlist(self, input):
        final_query_exp_list = []
        x = list(filter(None, input))
        for summary_query_list in input:
            out = []
            for query in summary_query_list:
                input = query.split(",")
                for query in input:
                    query = query.strip()
                    if query == "":
                        continue
                    elif query == 'None':
                        continue
                    out.append(query)
            final_query_exp_list.append(out)
        return final_query_exp_list

    def removeNone(self, exp_list):
        for index, query in enumerate(exp_list):
            try:
                query_list = query.split(',')
                res = [x for x in query_list if x != 'nan']
                res = ','.join(res)
                exp_list[index] = res
            except:
                exp_list[index] = str(query)
        return exp_list
