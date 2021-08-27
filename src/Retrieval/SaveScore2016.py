import os

class SaveScore_2016:
    '''
        Input:
            out_file_path: output file path
            query_id_list: query_id_list
            score_list: score list
            query_string: list of query strings

    '''
    def __init__(self, score_list, query_id_list, out_file_path,query_string = []):
        self.score_list = score_list
        self.query_id_list = query_id_list
        self.out_file_path = out_file_path
        self.query_string = query_string
        self.scores = list()
        self.doc_id_list = list()
        self.documnets = []
        self.extractScores()

    '''
        Extract the scores and URLs from the provided self.score_list
    '''
    def extractScores(self):
        for result in self.score_list:
            url = list()
            documents = []
            score = list()
            for res in result['hits']['hits']:
                url.append(res['_source']['DOCNO'])
                score.append(res['_score'])
                documents.append(res['_source']['concat_string'])
            self.scores.append(score)
            self.doc_id_list.append(url)
            self.documnets.append(documents)
        if len(self.query_string) == 0:
            self.savescores()
        else:
            self.savescores_tsv()


    '''
        prepares the Query_id_list with provided id and count.
    '''
    def getQueryIdList(self, query_id, count):
        query_id_list = list()
        for _ in range(count):
            query_id_list.append(query_id)
        return query_id_list

    '''
        Prepare scores document
    '''

    def savescores(self):
        for query_id, doc_id_list, score_list, documnets in zip(self.query_id_list, self.doc_id_list, self.scores, self.documnets):
            query_id_list = self.getQueryIdList(query_id, len(doc_id_list))
            for query_id, doc_id, score, document in zip(query_id_list, doc_id_list, score_list, documnets):
                if score > 0.0:
                    mode = "a" if os.path.exists(self.out_file_path) else "w"
                    with open(self.out_file_path, mode) as outFile:
                        outFile.write(str(query_id) + "\t" + doc_id + '\t' + str(score) + '\t' + str(document) +"\n")

    def savescores_tsv(self):
        for query_id, doc_id_list, score_list, documnets, query_string in zip(self.query_id_list, self.doc_id_list, self.scores, self.documnets, self.query_string):
            query_id_list = self.getQueryIdList(query_id, len(doc_id_list))
            query_string_list = self.getQueryIdList(query_string, len(doc_id_list))
            for query_id, doc_id, score, document, querystring in zip(query_id_list, doc_id_list, score_list, documnets, query_string_list):
                if score > 0.0:
                    mode = "a" if os.path.exists(self.out_file_path) else "w"
                    with open(self.out_file_path, mode) as outFile:
                        outFile.write(str(query_id) + "\t" + querystring +'\t'+ doc_id + '\t' +  str(document) + '\t' + str(score) +"\n")