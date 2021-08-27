from elasticsearch import Elasticsearch

'''
soime code related to Elasticsearch
'''
class Operations:

    def __init__(self, search_index):
        self.search_index = search_index
        self.es = Elasticsearch()

    def getDocumnetwith(self, index):
        doc = self.es.get(index=self.search_index, id=4700719)
        print(doc)

obj = Operations("2016-trec-precision-medicine-final")
obj.getDocumnetwith(4700719)

