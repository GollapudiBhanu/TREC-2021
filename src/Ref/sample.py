def preparecorpus(self, search_index):
    corpus_obj = Corpus.creatCorpus(search_index)
    corpus = corpus_obj.prepareCorpus()
    document_id_list = corpus_obj.getdocumentidlist()
    return corpus, document_id_list


def baselinequery(self, source_file):
    query = Queries.GetQuery(source_file)
    queries = query.getQueryList()
    return queries


def expandedQuery(self, source_file):
    expanded_query = QueryExpansionList.ExapndedQuery(source_file)
    expanded_query_list = expanded_query.getGroupedData()
    expanded_query_id_list = expanded_query.removeDuplicates()
    return expanded_query_list, expanded_query_id_list


def getExpandedQuerylist(self, source_file):
    expanded_query = QueryExpansionList.ExapndedQuery(source_file)
    expanded_query_results = expanded_query.getGroupedData()
    expanded_query_list = expanded_query_results[0]
    expanded_query_id_list = expanded_query_results[1]
    return expanded_query_list, expanded_query_id_list


def basicpreprocessing_2019(self, source_file, dest_file):
    basic_preprocessing = BasicPreprocessing.Preprocessing(source_file, dest_file)
    basic_preprocessing.getRootJsonObject()
    print("Basic preprocessing is Done")


def indexing_2019(self, folder_path, index_name):
    _ = Indexing2019.Indexing(folder_path, index_name)
    print("Indexing if 2019 is Done.")


def baseLineScoring_2019(self):
    basic_result = self.preparecorpus("2019-trec-precision-medicine")
    corpus = basic_result[0]
    document_id_list = basic_result[1]
    queries = self.baselinequery("./Data/2019_quries/topics2019.xml")
    bm25 = Bm25_scoring.BM25(corpus, delimiter=' ')
    bm25.getBM25Score(queries, document_id_list)


def queryexapnsionscoring_2019(self):
    basic_result = self.preparecorpus("2019-trec-precision-medicine")
    corpus = basic_result[0]
    document_id_list = basic_result[1]

    queries = self.expandedQuery('./Data/Expansiontopics2019.csv')[0]
    query_id_list = queries[1]

    bm25 = Bm25_scoring.BM25(corpus, delimiter=' ')
    bm25.getExpandedBM25Score(queries, document_id_list, query_id_list)


def queryExpansion(self):
    expanded_query = Queryexpansion.NewExapndedQuery('./Data/Expansiontopics2019.csv')
    expanded_query_list = expanded_query.getGroupedData()
    expanded_query_id_list = expanded_query.removeDuplicates()
    return expanded_query_list, expanded_query_id_list


def getOKAPIBm25baselinescoring_2019(self):
    basic_result = self.preparecorpus("2019-trec-precision-medicine")
    corpus = basic_result[0]
    document_id_list = basic_result[1]

    queries = self.baselinequery("./Data/2019_quries/topics2019.xml")

    bm25 = OkapiBm25.OKAPIBM25_Scoring(corpus)
    bm25.getBM25Score(queries, document_id_list)


def getOKAPIBm25QueryExpansionscoring_2019(self):
    basic_result = self.preparecorpus("2019-trec-precision-medicine")
    corpus = basic_result[0]
    document_id_list = basic_result[1]

    query_result = self.expandedQuery('./Data/Expansiontopics2019.csv')
    queries = query_result[0]
    query_id_list = query_result[1]

    bm25 = OkapiBm25.OKAPIBM25_Scoring(corpus)
    bm25.getQueryExapnsionBM25Score(queries, document_id_list, query_id_list)
