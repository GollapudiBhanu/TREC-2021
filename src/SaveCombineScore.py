class Savecombine:

    def __init__(self, out_file_path, and_score_list, or_score_list, and_id_list, or_id_list):
        self.out_file_path = out_file_path
        self.and_scores = []
        self.and_urls = []
        self.or_scores = []
        self.or_urls = []
        self.and_score_list = and_score_list
        self.and_query_id_list = and_id_list
        self.or_score_list = or_score_list
        self.or_query_id_list = or_id_list

        self.combineScores()

    def extractAndScores(self):
        for result in self.and_score_list:
            url = list()
            score = list()
            for res in result['hits']['hits']:
                url.append(self.__prepareDocId(res['_source']['url']))
                score.append(res['_score'])
            self.and_scores.append(score)
            self.and_urls.append(url)

    def extractORScores(self):
        for result in self.or_score_list:
            url = list()
            score = list()
            for res in result['hits']['hits']:
                url.append(self.__prepareDocId(res['_source']['url']))
                score.append(res['_score'])
            self.or_scores.append(score)
            self.or_urls.append(url)


    def combineScores(self):
        self.extractAndScores()
        self.extractORScores()

        print("*************** Before **********************")
        print(len(self.or_urls))
        print(len(self.or_scores))

        for index, and_url_list, and_score_list, or_url_list, or_score_list in enumerate(zip(self.and_urls, self.and_score_list, self.or_urls, self.or_score_list)):
            for id, and_url, and_score, or_url,or_score in enumerate(zip(and_url_list, and_score_list, or_url_list, or_score_list)):
                for url in and_url:
                    sub_index = or_url.index(url)
                    del or_url[sub_index]
                    del or_score[sub_index]
                or_url_list[id] = or_url
                or_score_list[id] = or_score_list
            self.or_urls[index] = or_url_list
            self.or_scores[index] = or_score_list

        print("*************** After **********************")
        print(len(self.or_urls))
        print(len(self.or_scores))

    def __prepareDocId(self, url):
        head, tail = url.split("httpsclinicaltrialsgovshow")
        return tail

    '''
            Prepare scores document
    '''

    def savescores(self):
        pass

