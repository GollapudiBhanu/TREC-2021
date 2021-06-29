class SaveScore_2016:

    def __init__(self, socre_list, query_id_list, out_file_path):
        self.score_list = socre_list
        self.query_id_list = query_id_list
        self.out_file_path = out_file_path
        self.scores = list()
        self.doc_id_list = list()
        self.extractScores()

    def extractScores(self):
        for result in self.score_list:
            url = list()
            score = list()
            for res in result['hits']['hits']:
                url.append(res['_source']['DOCNO'])
                score.append(res['_score'])
            self.scores.append(score)
            self.doc_id_list.append(url)
        self.savescores()


    def getQueryIdList(self, query_id, count):
        query_id_list = list()
        for _ in range(count):
            query_id_list.append(query_id)
        return query_id_list

    '''
        Prepare scores document
    '''

    def savescores(self):
        for query_id, doc_id_list, score_list in zip(self.query_id_list, self.doc_id_list, self.scores):
            query_id_list = self.getQueryIdList(query_id, len(doc_id_list))
            for query_id, doc_id, score in zip(query_id_list, doc_id_list, score_list):
                if score > 0.0:
                    with open(self.out_file_path, "a") as outFile:
                        outFile.write(str(query_id) + "\t" + doc_id + '\t' + str(score) + "\n")