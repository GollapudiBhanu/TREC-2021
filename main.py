import BasicPreprocessing
import Indexing2019
import QueryExpansionList
import Corpus
import Bm25_scoring
import Queries
import OkapiBm25
import BoolQuery
import Queryexpansion
import BasicPreprocessing_2016
import Indexing2016
import SaveScore
import BoolQueryExpansion
import Query2021
import BoolQuery_score
import CombinedQuery
import SaveCombineScore


class Main:
    """
        Basic Preprocessing
    """

    def basicpreprocessing(self):
        basic_preprocessing = BasicPreprocessing.Preprocessing('./Data/TREC_2019_input_data', './Data/TREC_2019_Output_data')
        basic_preprocessing.getRootJsonObject()

    '''
        Indexing
    '''

    def indexing(self, folder_path,index_name):
        _ = Indexing2019.Indexing(folder_path,index_name)
        print("Indexing is Done")

    '''
     Corpus preparation
    '''

    def preparecorpus(self):
        corpus_obj = Corpus.creatCorpus()
        corpus = corpus_obj.prepareCorpus()
        document_id_list = corpus_obj.getdocumentidlist()
        return corpus, document_id_list

    '''
        BaseLineScoring
    '''

    def baseLineScoring(self):
        corpus = self.preparecorpus()[0]
        document_id_list = self.preparecorpus()[1]

        queries = self.baselinequery()

        bm25 = Bm25_scoring.BM25(corpus, delimiter=' ')
        bm25.getBM25Score(queries, document_id_list)
        # tfidf = bm25.TFIDF()

    '''
        BaseLineQuery
    '''

    def baselinequery(self):
        query = Queries.GetQuery("./Data/2019_quries/topics2019.xml")
        queries = query.getQueryList()
        return queries

    '''
        Expanded Query List
    '''

    def expandedQuery(self):
        expanded_query = QueryExpansionList.ExapndedQuery('./Data/Expansiontopics2019.csv')
        expanded_query_list = expanded_query.getGroupedData()
        expanded_query_id_list = expanded_query.removeDuplicates()
        return expanded_query_list, expanded_query_id_list

    '''
        Query Expansion
    '''

    def queryexapnsionscoring(self):
        corpus = self.preparecorpus()[0]
        document_id_list = self.preparecorpus()[1]

        queries = self.expandedQuery()[0]
        query_id_list = self.expandedQuery()[1]

        bm25 = Bm25_scoring.BM25(corpus, delimiter=' ')
        bm25.getExpandedBM25Score(queries, document_id_list, query_id_list)

    def getOKAPIBm25baselinescoring(self):
        corpus = self.preparecorpus()[0]
        document_id_list = self.preparecorpus()[1]

        queries = self.baselinequery()

        bm25 = OkapiBm25.OKAPIBM25_Scoring(corpus)
        bm25.getBM25Score(queries, document_id_list)

    def getOKAPIBm25QueryExpansionscoring(self):
        corpus = self.preparecorpus()[0]
        document_id_list = self.preparecorpus()[1]

        queries = self.expandedQuery()[0]
        query_id_list = self.expandedQuery()[1]

        bm25 = OkapiBm25.OKAPIBM25_Scoring(corpus)
        bm25.getQueryExapnsionBM25Score(queries, document_id_list, query_id_list)


    def getScoresusingBoolQuery(self, source_file, search_index):
        bool_query = BoolQuery.GetBoolQuery(source_file)
        results_list = bool_query.prepareBoolQuery(search_index)
        return results_list

    '''
        Expanded Query List
    '''

    def getExpandedQueryresults(self, source_path):
        expanded_query_results = self.getExpandedQuerylist(source_path)
        expanded_query_list = expanded_query_results[0]
        expanded_query_id_list = expanded_query_results[1]
        return expanded_query_list, expanded_query_id_list

    def queryExpansion(self):
        expanded_query = Queryexpansion.NewExapndedQuery('./Data/Expansiontopics2019.csv')
        expanded_query_list = expanded_query.getGroupedData()
        expanded_query_id_list = expanded_query.removeDuplicates()
        return expanded_query_list, expanded_query_id_list

    def basicpreprocessing2016(self):
        preprocessing_obj = BasicPreprocessing_2016.Preprocessing_2016('./Data/2016_Trec_Basic_Input',
                                               './Data/TREC_2016_OutputData')
        print("Corpus preparation is Done")
        preprocessing_obj.getRootJsonObject()
        print("Basic Preprocessing is done successfully.")

    '''
        Get expanded query results based on the file path
    '''
    def getExpandedQuerylist(self, source_file):
        expanded_query = QueryExpansionList.ExapndedQuery(source_file)
        expanded_query_results = expanded_query.getGroupedData()
        expanded_query_list = expanded_query_results[0]
        expanded_query_id_list = expanded_query_results[1]
        return expanded_query_list, expanded_query_id_list

    def Indexing_2016(self):
        _ = Indexing2016.Indexing_2016('./Data/TREC_2016_OutputData')
        print("Indexing is done")

    """
            Basic Preprocessing
    """

    def basicpreprocessing_2021(self):
        basic_preprocessing = BasicPreprocessing.Preprocessing('./Data/TREC_2021_Basicpreprocessing_Input',
                                                               './Data/TREC_2021_Basicpreprocessing_output')
        basic_preprocessing.getRootJsonObject()


    '''
        Save Elasticsearch scores in file
    '''
    def getScoresUsingBoolQuery_2019(self):
        bool_query_results = self.getScoresusingBoolQuery("./Data/2019_quries/topics2019.xml", "2019-trec-precision-medicine-final")
        score_list = bool_query_results[0]
        query_id_list = bool_query_results[1]
        _ = SaveScore.Save("./Output/AND_BoolQuery_scores_2019-final.csv", query_id_list, score_list)
        print("*...scores saved successfully...*")

    '''
           Save Elasticsearch scores in file
    '''

    def getScoresUsingBoolQueryExpanison_2019(self):
        expanded_query_results = self.getExpandedQueryresults('./Data/topics2019_expandedquery_Metamap.csv')
        query_id_list = expanded_query_results[1]

        exp_bool_query_obj = BoolQueryExpansion.GetBoolQueryExpansion(expanded_query_results[0],
                                                                      "2019-trec-precision-medicine")
        scores = exp_bool_query_obj.getScores()
        _ = SaveScore.Save("./Output/ExpandedBoolQuery_scores_2019.csv", query_id_list, scores)

        print("*...Exapnded scores saved successfully...*")

    def getScoresUsingClinicalBertBoolQueryExpanison_2019(self):
        expanded_query_results = self.getExpandedQueryresults('./Data/2019_quries/bool_final_query.csv')
        query_id_list = expanded_query_results[1]

        exp_bool_query_obj = BoolQueryExpansion.GetBoolQueryExpansion(expanded_query_results[0],
                                                                      "2019-trec-precision-medicine-final")
        scores = exp_bool_query_obj.getScores()
        _ = SaveScore.Save("./Output/ClinicalBert_ExpandedBoolQuery_scores_2019.csv", query_id_list, scores)

        print("*...Exapnded scores saved successfully...*")


    '''
        which returns tuple for Queries and QueryIdList
    '''
    def getQueries(self, query_file_path):
        extract_query = Query2021.ExtractQueries(query_file_path)
        return extract_query.getQueries()

    def getScoresusingBoolQuery_2021(self, query_file_path, search_index):
        query_res = self.getQueries(query_file_path)
        query_list = query_res[1]
        query_id_list = query_res[0]
        bool_score = BoolQuery_score.BoolQueryScore(query_list, query_id_list, search_index)
        bool_results = bool_score.getScore()
        query_id_list = bool_results[1]
        score_list = bool_results[0]
        _ = SaveScore.Save("./Output/BoolQuery_scores_2021.csv", query_id_list, score_list)
        print("*...scores saved successfully...*")

    '''./Data/2021Quries/Query_keywords_2021.csv'
            Save Elasticsearch scores in file
    '''

    def getScoresUsingBoolQuery_20211(self):
        bool_query_results = self.getScoresusingBoolQuery("./Data/2021Quries/Query_keywords_2021.csv",
                                                          "2020-trec-precision-medicine")
        score_list = bool_query_results[0]
        query_id_list = bool_query_results[1]
        _ = SaveScore.Save("./Output/BoolQuery_scores_2019.csv", query_id_list, score_list)
        print("*...scores saved successfully...*")

    def getScoresusingCombinedBoolQuery(self, source_file, search_index):
        bool_query = CombinedQuery.GetCombinedBoolQuery(source_file)
        results_list = bool_query.prepareBoolQuery(search_index)
        return results_list

    def getScoreUsingCombinedQuery_2019(self):
        combine_query_results = self.getScoresusingCombinedBoolQuery("./Data/2019_quries/topics2019.xml",
                                                          "2019-trec-precision-medicine-final")

        and_bool_results = combine_query_results[0]
        or_bool_results = combine_query_results[1]

        and_bool_results_score = and_bool_results[0]
        and_bool_results_id = and_bool_results[1]

        or_bool_results_score = or_bool_results[0]
        or_bool_results_id = or_bool_results[1]
        _ = SaveCombineScore.Savecombine('./Output/combined_BoolQuery_scores_2019.csv',
                                         and_bool_results_score,
                                         or_bool_results_score,
                                         and_bool_results_id,
                                         or_bool_results_id)

        print("*...scores saved successfully...*")




main_obj = Main()
# main_obj.basicpreprocessing()
#main_obj.indexing('./Data/TREC_2019_Output_data',"2019-trec-precision-medicine")
#main_obj.baselinequery()
#main_obj.baseLineScoring()
#main_obj.queryexapnsionscoring()
#main_obj.getOKAPIBm25baselinescoring()
#main_obj.getOKAPIBm25QueryExpansionscoring()
#main_obj.getScoreusingBoolQuery()
#tupe =  main_obj.queryExpansion()
#main_obj.expandedQuery2019()
#main_obj.Indexing_2016()
#main_obj.basicpreprocessing_2021()
#main_obj.indexing('./Data/TREC_2021_Basicpreprocessing_output', "2021-trec-precision-medicine_final")
#main_obj.getScoresUsingQueryExpanison_2019()
#bool_query_results = main_obj.getScoresusingBoolQuery("./Data/2019_quries/topics2019.xml", "2019-trec-precision-medicine")#main_obj.getScoresWithElasticSearchUsingBoolQuery_2019()
#main_obj.getScoresUsingBoolQuery_2019()
#main_obj.getScoresUsingBoolQueryExpanison_2019()
#main_obj.getScoresUsingClinicalBertBoolQueryExpanison_2019()
#main_obj.getScoresusingBoolQuery_2021('./Data/2021Quries/Query_keywords_2021.csv',
                                      #'2021-trec-precision-medicine')
#basic_preprocessing = Preprocessing('/home/junhua/trec/Trec2021/Data/TREC_2019_input_data', '/home/junhua/trec/Trec2021/Data/TREC_2019_Output_data')
#basic_preprocessing.getRootJsonObject()
#main_obj.indexing('./Data/TREC_2019_Output_data',"2019-trec-precision-medicine-final")
#main_obj.getScoresUsingBoolQuery_2019()
main_obj.getScoreUsingCombinedQuery_2019()
