import pandas as pd


class NewExapndedQuery:

    def __init__(self, query_path):
        self.query_path = query_path

    '''
        Reads data from provided query_path using Pandas.
    '''
    def readfile(self):
        expansion_dataframe = pd.read_csv(self.query_path)
        return expansion_dataframe

    '''
        Extract and return the TopicId list from the dataframe.        
    '''
    def getTopicIDList(self):
        expansion_dataframe = self.readfile()
        topic_id_list = expansion_dataframe['TopicID']
        return topic_id_list

    '''
        It separates the "gene" and "disease" values from the QueryId.
    '''
    def groupByTopicId(self):
        topic_id_list = list()
        topic_list = self.getTopicIDList()
        for topic in topic_list:
            if "gene" in topic:
                topic_id = topic.split("gene")
                topic_id_list.append(topic_id[0])
            elif "disease" in topic:
                topic_id = topic.split("disease")
                topic_id_list.append(topic_id[0])
        return topic_id_list

    '''
        It groupes the query's by QueryID and remove the duplicate id's
    '''
    def removeDuplicates(self):
        topicIdList = self.groupByTopicId()
        unique_Id_list = list(set(topicIdList))
        return unique_Id_list

    '''
        Add Extra column to the dataframe.
    '''
    def addColoumnToDataFrame(self):
        expansion_dataFrame = self.readfile()
        topic_id_list = self.groupByTopicId()
        expansion_dataFrame["group_topic_id"] = topic_id_list
        return expansion_dataFrame

    '''
        Get the list of expanded queries with their id.
    '''
    def getGroupedData(self):
        dataFrame = self.addColoumnToDataFrame()
        grouped_list = list()
        df1 = dataFrame.groupby(["group_topic_id"]).agg(lambda x: x.tolist())
        queryConcept = df1["query_concept"].tolist()
        extendedConcept = df1["extended_concept"].tolist()
        query_id_List = self.removeDuplicates()
        for queryId, concept, extended in zip(query_id_List, queryConcept, extendedConcept):
            queryString = ' '.join(map(str, (set(concept + extended))))
            grouped_list.append(queryId + " " + queryString)
        return list(grouped_list)

