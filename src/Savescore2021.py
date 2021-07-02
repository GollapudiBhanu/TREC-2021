class Savescore_2021:

    def __init__(self, socre_list, query_id_list, out_file_path):
        self.score_list = socre_list
        self.query_id_list = query_id_list
        self.out_file_path = out_file_path
        self.scores = list()
        self.source = list()
        self.doc_id_list = list()
        self.extractScores()

    '''
        Extract the scores and URLs from the provided self.score_list
    '''
    def extractScores(self):
        for result in self.score_list:
            url = list()
            score = list()
            source = list()
            for res in result['hits']['hits']:
                url.append(self.__prepareDocId(res['_source']['url']))
                score.append(res['_score'])
                source.append(res['_source'])
            self.scores.append(score)
            self.doc_id_list.append(url)
            self.source.append(source)
        self.savescores()

    '''
        prepares the Query_id_list with provided id and count.
    '''
    def getQueryIdList(self, query_id, count):
        query_id_list = list()
        for _ in range(count):
            query_id_list.append(query_id)
        return query_id_list

    '''
        It returns the document name from the provided URL.
    '''
    def __prepareDocId(self, url):
        head, tail = url.split("httpsclinicaltrialsgovshow")
        return tail

    '''
        Prepare scores document
    '''

    def savescores(self):
        for query_id, doc_id_list, score_list, source_list in zip(self.query_id_list, self.doc_id_list, self.scores, self.source):
            query_id_list = self.getQueryIdList(query_id, len(doc_id_list))
            for query_id, doc_id, score, source in zip(query_id_list, doc_id_list, score_list, source_list):
                if score > 0.0:
                    with open(self.out_file_path, "a") as outFile:
                        outFile.write(str(query_id) + "\t" + doc_id + '\t' + str(score) + '\t' + str(source) + "\n")