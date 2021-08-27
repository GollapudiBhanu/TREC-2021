import xml.etree.ElementTree as ET


class GetQuery:
    '''
        Input:
            query_doc: path for query file path.
    '''
    def __init__(self, query_doc):
        self.query_doc = query_doc

    '''
        From the XML file, it retrieves the query string and prepares a list opf queries.
    '''

    def getQueryList(self):
        query_list = list()
        tree = ET.parse(self.query_doc)
        queryRoot = tree.getroot()
        for query in queryRoot:
            queryString = query.attrib["number"] + "\n"
            for element in query:
                queryString += element.text
                queryString += ""
            query_list.append(queryString)
        return query_list
