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
import ExrtractScoresFromFile
import SaveCombineQueryExapansionScore
import BasicPreprocessing_2021
import IntialSetup
import Indexing2021
import Query2016
import BoolQuery2016
import SaveScore2016



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

    def indexing_2016(self):
        _ = Indexing2016.Indexing_2016('./Data/TREC_2016_OutputData')
        print("Indexing is done")

    """
            Basic Preprocessing
    """

    def basicpreprocessing_2021(self):
        basic_preprocessing = BasicPreprocessing_2021.Preprocessing_2021('/home/junhua/trec/Trec2021/Data/TREC_2021_Basicpreprocessing_Input',
                                                 '/home/junhua/trec/Trec2021/Data/TREC_2021_Basicpreprocessing_output')
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
        expanded_query_results = self.getExpandedQueryresults('./Data/2019_quries/topics2019_expandedquery_Metamap.csv')
        query_id_list = expanded_query_results[1]

        exp_bool_query_obj = BoolQueryExpansion.GetBoolQueryExpansion(expanded_query_results[0],
                                                                      "2019-trec-precision-medicine-final")
        scores = exp_bool_query_obj.getScores()
        _ = SaveScore.Save("./Output/New_ExpandedBoolQuery_scores_2019.csv", query_id_list, scores)

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

        _ = SaveScore.Save("./Output/Final_AND_BoolQuery_scores_2019.csv", and_bool_results_id, and_bool_results_score)
        _ = SaveScore.Save("./Output/Final_OR_BoolQuery_scores_2019.csv", or_bool_results_id, or_bool_results_score)


        _ = SaveCombineScore.Savecombine('./Output/combined_BoolQuery_scores_2019.csv',
                                         and_bool_results_score,
                                         or_bool_results_score,
                                         and_bool_results_id,
                                         or_bool_results_id)

        print("*...scores saved successfully...*")

    def ExtarctQueryExpanisonListsfromfile_2019(self):
        obj = ExrtractScoresFromFile.ExtractList(
            '/home/junhua/trec/Trec2021/Output/Final_AND_BoolQuery_scores_2019.csv')
        extract_and_results = obj.extractScore()
        obj1 = ExrtractScoresFromFile.ExtractList(
            '/home/junhua/trec/Trec2021/Output/Final_OR_BoolQuery_scores_2019.csv')
        extract_or_results = obj1.extractScore()
        obj2 = ExrtractScoresFromFile.ExtractList(
            '/home/junhua/trec/Trec2021/Output/New_ExpandedBoolQuery_scores_2019.csv')
        extract_expanded_results = obj2.extractScore()
        obj = IntialSetup.ListIntialSetUp(extract_and_results,extract_or_results,extract_expanded_results)
        results = obj.arrangeQueryExpansionLength()
        return results


    def ExtractScoresFromFiles_2019(self):
        results = self.ExtarctQueryExpanisonListsfromfile_2019()
        extract_and_results = results[0]
        extract_or_results = results[1]
        extract_expanded_results = results[2]

        save_obj = SaveCombineQueryExapansionScore.SaveCombineQueryExapnsion("/home/junhua/trec/Trec2021/Output/Final_Combined_queryexpansion_BoolQuery_scores_2019.csv",
                                                                                  extract_and_results,
                                                                                  extract_or_results,
                                                                                  extract_expanded_results)
        save_obj.extractandSaveQueryExapansionScore()
        print("*...scores saved successfully...*")

    def ExtarctBaseLineQueryListfromfile_2019(self):
        obj = ExrtractScoresFromFile.ExtractList(
            '/home/junhua/trec/Trec2021/Output/Final_AND_BoolQuery_scores_2019.csv')
        extract_and_results = obj.extractScore()
        obj1 = ExrtractScoresFromFile.ExtractList(
            '/home/junhua/trec/Trec2021/Output/Final_OR_BoolQuery_scores_2019.csv')
        extract_or_results = obj1.extractScore()
        obj = IntialSetup.ListIntialSetUp(extract_and_results, extract_or_results)
        results = obj.arrangeBaseLineQueryLength()
        return results

    def ExtractBaseLineScoresFromFiles_2019(self):
        results = self.ExtarctBaseLineQueryListfromfile_2019()
        extract_and_results = results[0]
        extract_or_results = results[1]

        save_obj = SaveCombineQueryExapansionScore.SaveCombineQueryExapnsion("/home/junhua/trec/Trec2021/Output/Final_Combined_BoolQuery_scores_2019.csv",
                                                                                  extract_and_results,
                                                                                  extract_or_results)
        save_obj.extractandSaveBaseLineQueryScore()
        print("*...scores saved successfully...*")

    def indexing_2021(self):
        index_obj = Indexing2021.Indexing_2021('./Data/TREC_2021_Basicpreprocessing_output', "2021-trec-precision-medicine-final")


    def getQueries_2016(self, source_file):
        query_obj = Query2016.GetQuery_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/' + source_file)
        results = query_obj.getQueryListWithId()
        return results

    def GetBoolQueryscore_2016(self):
        #KeywordExtr_Query2016.csv
        #KeywordExtr_Query2016_5w-1gram.csv
        result = self.getQueries_2016('KeywordExtr_Query2016_5w-1gram.csv')
        query_id_list = result[0]
        sum_query_list = result[1]
        score_obj = BoolQuery2016.GetBoolQuery_2016(sum_query_list, query_id_list)
        results = score_obj.prepareBoolQuery()
        score_res = results[0]
        query_id = results[1]
        _ = SaveScore2016.SaveScore_2016(score_res, query_id, "/home/junhua/trec/Trec2021/Output/Summary_AND_BoolQuery_scores_2016.csv")
        #_ = SaveScore2016.SaveScore_2016(score_res, query_id, "/home/junhua/trec/Trec2021/Output/Summary_OR_BoolQuery2016_5w-1gram_scores_2016.csv")
        print("Summary scores saved successfully")
        '''
        result = self.getQueries_2016()
        query_id_list = result[0]
        des_query_list = result[2]
        score_obj = BoolQuery2016.GetBoolQuery_2016(des_query_list, query_id_list)
        results = score_obj.prepareBoolQuery()
        score_res = results[0]
        query_id = results[1]
        _ = SaveScore2016.SaveScore_2016(score_res, query_id, "/home/junhua/trec/Trec2021/Output/Description_AND_BoolQuery_scores_2016.csv")
        print("Description scores saved successfully")

        result = self.getQueries_2016()
        query_id_list = result[0]
        note_query_list = result[3]
        score_obj = BoolQuery2016.GetBoolQuery_2016(note_query_list, query_id_list)
        results = score_obj.prepareBoolQuery()
        score_res = results[0]
        query_id = results[1]
        _ = SaveScore2016.SaveScore_2016(score_res, query_id, "/home/junhua/trec/Trec2021/Output/Notes_AND_BoolQuery_scores_2016.csv")
        print("Notes scores saved successfully")
        '''

    def getMetamapQueries_2016(self, source_file, query_type = " "):
        query_obj = Query2016.GetQuery_2016(source_file)
        if query_type == "NER":
            results = query_obj.getNERQueriesList(["Sl.No", "queryID", "note", "description", "summary", "summary_NER", "note_NER", "description_NER"])
            return results
        elif query_type == "NER-Disease":
            results = query_obj.getNERQueriesList(["Sl.No", "queryID", "summary", "summary_NER3", "description", "description_NER3", "note", "note_NER3"])
            return results
        elif query_type == "NER-Drug":
            results = query_obj.getNERQueriesList(["Sl.No", "queryID", "summary", "summary_NERgdd", "description", "description_NERgdd", "note", "note_NERgdd"])
            return results
        elif query_type == "Weighted":
            results = query_obj.getQueryListWithId()
            return results
        else:
            results = query_obj.getMetamapQueryListWithId()
            return results

    def GetMetamapBoolQueryscore_2016(self, source_file, out_file):
        result = self.getMetamapQueries_2016(source_file)
        query_id_list = result[0]
        sum_query_list = result[1]
        score_obj = BoolQuery2016.GetBoolQuery_2016(sum_query_list, query_id_list)
        results = score_obj.prepareBoolQuery()
        score_res = results[0]
        query_id = results[1]
        _ = SaveScore2016.SaveScore_2016(score_res, query_id, out_file)
        print("Summary scores saved successfully")

    def getFilterMetamapQueries_2016(self):
        query_obj = Query2016.GetQuery_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/Metamap_summary_query_filtered.csv')
        results = query_obj.getFilteredMetamapQueryListWithId()
        return results

    def GetFilterMetamapBoolQueryscore_2016(self):
        result = self.getFilterMetamapQueries_2016()
        query_id_list = result[0]
        filter_query_list = result[1]
        score_obj = BoolQuery2016.GetBoolQuery_2016(filter_query_list, query_id_list)
        results = score_obj.prepareBoolQuery()
        score_res = results[0]
        query_id = results[1]
        _ = SaveScore2016.SaveScore_2016(score_res, query_id,
                                         "/home/junhua/trec/Trec2021/Output/Filter_Summary_AND_Metamap_BoolQuery_scores_2016.csv")
        print("Summary scores saved successfully")

    def ExtarctBaseLineQueryListfromfile_2016(self):
        obj = ExrtractScoresFromFile.ExtractList(
            '/home/junhua/trec/Trec2021/Output/Summary_AND_BoolQuery2016_5w-1gram_scores_2016.csv')
        extract_and_results = obj.extractScore()
        obj1 = ExrtractScoresFromFile.ExtractList(
            '/home/junhua/trec/Trec2021/Output/Summary_OR_BoolQuery2016_5w-1gram_scores_2016.csv')
        extract_or_results = obj1.extractScore()
        obj = IntialSetup.ListIntialSetUp(extract_and_results, extract_or_results)
        results = obj.arrangeBaseLineQueryLength()
        return results

    def ExtractBaseLineScoresFromFiles_2016(self):
        results = self.ExtarctBaseLineQueryListfromfile_2016()
        extract_and_results = results[0]
        extract_or_results = results[1]

        save_obj = SaveCombineQueryExapansionScore.SaveCombineQueryExapnsion("/home/junhua/trec/Trec2021/Output/Summary_ANDWithOR_BoolQuery2016_5w-1gram_scores_2016.csv",
                                                                                  extract_and_results,
                                                                                  extract_or_results)
        save_obj.extractandSaveBaseLineQueryScore()
        print("*...scores saved successfully...*")

    def GetNERMetamapBoolQueryscore_2016(self, source_file, out_and_file, out_or_file ,type):
        result = self.getMetamapQueries_2016(source_file, type)
        query_id_list = list()
        sum_query_list = list()
        if type == "NER":
            query_id_list = result[1]
            sum_query_list = result[5]
        elif type == "NER-Disease":
            query_id_list = result[1]
            sum_query_list = result[3]
        elif type == "NER-Drug":
            query_id_list = result[1]
            sum_query_list = result[3]
        elif type == "Weighted":
            query_id_list = result[0]
            sum_query_list = result[1]

        score_obj = BoolQuery2016.GetBoolQuery_2016(sum_query_list, query_id_list)
        results = score_obj.prepareBoolQuery("AND")
        score_res = results[0]
        query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(score_res, query_id, out_and_file)

        results = score_obj.prepareBoolQuery("OR")
        score_res = results[0]
        query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(score_res, query_id, out_or_file)

        print("Summary scores saved successfully")


    def ExtarctNERBaseLineQueryListfromfile_2016(self, and_file, or_file):
        obj = ExrtractScoresFromFile.ExtractList(and_file)
        extract_and_results = obj.extractScore()
        obj1 = ExrtractScoresFromFile.ExtractList(or_file)
        extract_or_results = obj1.extractScore()
        obj = IntialSetup.ListIntialSetUp(extract_and_results, extract_or_results)
        results = obj.arrangeBaseLineQueryLength()
        return results

    def ExtractNERBaseLineScoresFromFiles_2016(self, and_file, or_file, out_file):
        results = self.ExtarctNERBaseLineQueryListfromfile_2016(and_file, or_file)
        extract_and_results = results[0]
        extract_or_results = results[1]

        save_obj = SaveCombineQueryExapansionScore.SaveCombineQueryExapnsion(out_file, extract_and_results, extract_or_results)
        save_obj.extractandSaveBaseLineQueryScore()
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
#main_obj.getScoresUsingBoolQueryExpanison_2019()
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
#main_obj.getScoreUsingCombinedQuery_2019()
#main_obj.getScoresUsingBoolQueryExpanison_2019()
#main_obj.basicpreprocessing2016()
#main_obj.ExtractScoresFromFiles_2019()
#main_obj.basicpreprocessing_2021()
#main_obj.ExtractBaseLineScoresFromFiles_2019()
#main_obj.ExtractScoresFromFiles_2019()
#main_obj.ExtractBaseLineScoresFromFiles_2019()
#main_obj.indexing_2016()
#main_obj.indexing_2021()
#main_obj.GetBoolQueryscore_2016()
#main_obj.GetMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/Metamap_topic_expansion_2016_summary_sometypes_B-reformated_2.csv', '/home/junhua/trec/Trec2021/Output/Summary_AND_Metamap_BoolQuery_scores_2016.csv')
#main_obj.GetFilterMetamapBoolQueryscore_2016()
#main_obj.GetBoolQueryscore_2016()
#main_obj.ExtarctBaseLineQueryListfromfile_2016()
#main_obj.ExtractBaseLineScoresFromFiles_2016()
#main_obj.ExtractBaseLineScoresFromFiles_2016()
#main_obj.GetMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_all.csv', '/home/junhua/trec/Trec2021/Output/Summary_AND_Metamap_BoolQuery_scores_2016.csv')
main_obj.GetNERMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_all.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER_BoolQuery_scores_2016.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER_BoolQuery_scores_2016.csv',"NER")
main_obj.GetNERMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_gene-disease.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease_2016.csv','/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease_2016.csv' ,"NER-Disease")
main_obj.GetNERMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_gene-disease-drug.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016.csv',"NER-Drug")
main_obj.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER_BoolQuery_scores_2016.csv', '/home/junhua/trec/Trec2021/Output/Summary_OR_NER_BoolQuery_scores_2016.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_Combined_NER_BoolQuery_scores_2016.csv')
main_obj.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease_2016.csv','/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease_2016.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_Combined_NER-BERN_Query2016_gene-disease_2016.csv')
main_obj.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_Combined_NER-BERN_Query2016_gene-disease-drug_2016.csv')
#main_obj.GetNERMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/KeywordExtr_Query2016_5w-1gram.csv', '/home/junhua/trec/Trec2021/Output/Summary_AND_5w-1gram_2016.csv', '/home/junhua/trec/Trec2021/Output/Summary_OR_5w-1gram_2016.csv',"Weighted")
#main_obj.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/Summary_AND_5w-1gram_2016.csv', '/home/junhua/trec/Trec2021/Output/Summary_OR_5w-1gram_2016.csv', '/home/junhua/trec/Trec2021/Output/Summary_Combined_5w-1gram_2016.csv')
