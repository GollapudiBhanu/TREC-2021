from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET


class getQuery:

    def __init__(self):
        self.query_doc = ""

    '''
        From the XML file, it retrieves the query string and prepares a list opf queries.
    '''

    def getQueryList(self):
        query_list = list()
        tree = ET.parse("/home/iialab/Bhanu/PythonFiles/FinalCode/2019_quries/topics2019.xml")
        queryRoot = tree.getroot()
        for query in queryRoot:
            queryString = query.attrib["number"] + "\n"
            for element in query:
                queryString += element.text
                queryString += " "
            query_list.append(queryString)
        return query_list
