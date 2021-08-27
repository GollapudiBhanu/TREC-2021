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
import Savescore2021
from pathlib import Path

class Main:

    ############################# 2019 #######################################

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

    def getScoresusingBoolQuery(self, source_file, search_index):
        bool_query = BoolQuery.GetBoolQuery(source_file)
        results_list = bool_query.prepareBoolQuery(search_index)
        return results_list

    def getExpandedQuerylist(self, source_file):
        expanded_query = QueryExpansionList.ExapndedQuery(source_file)
        expanded_query_results = expanded_query.getGroupedData()
        expanded_query_list = expanded_query_results[0]
        expanded_query_id_list = expanded_query_results[1]
        return expanded_query_list, expanded_query_id_list

    def getExpandedQueryresults(self, source_path):
        expanded_query_results = self.getExpandedQuerylist(source_path)
        expanded_query_list = expanded_query_results[0]
        expanded_query_id_list = expanded_query_results[1]
        return expanded_query_list, expanded_query_id_list

    def getScoresusingCombinedBoolQuery(self, source_file, search_index):
        bool_query = CombinedQuery.GetCombinedBoolQuery(source_file)
        results_list = bool_query.prepareBoolQuery(search_index)
        return results_list

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

    ########### 2019 - Bool Queries #######################3

    def getScoresUsingBoolQuery_2019(self):
        bool_query_results = self.getScoresusingBoolQuery("./Data/2019_quries/topics2019.xml",
                                                          "2019-trec-precision-medicine-final")
        score_list = bool_query_results[0]
        query_id_list = bool_query_results[1]
        _ = SaveScore.Save("./Output/AND_BoolQuery_scores_2019-final.csv", query_id_list, score_list)
        print("*...scores saved successfully...*")


    def getScoresUsingBoolQueryExpanison_2019(self):
        expanded_query_results = self.getExpandedQueryresults('./Data/2019_quries/topics2019_expandedquery_Metamap.csv')
        query_id_list = expanded_query_results[1]

        exp_bool_query_obj = BoolQueryExpansion.GetBoolQueryExpansion(expanded_query_results[0],
                                                                      "2019-trec-precision-medicine-final")
        scores = exp_bool_query_obj.getScores()
        _ = SaveScore.Save("./Output/New_ExpandedBoolQuery_scores_2019.csv",
                           query_id_list, scores)

        print("*...Exapnded scores saved successfully...*")


    def getScoresUsingClinicalBertBoolQueryExpanison_2019(self):
        expanded_query_results = self.getExpandedQueryresults('./Data/2019_quries/bool_final_query.csv')
        query_id_list = expanded_query_results[1]

        exp_bool_query_obj = BoolQueryExpansion.GetBoolQueryExpansion(expanded_query_results[0],
                                                                      "2019-trec-precision-medicine-final")
        scores = exp_bool_query_obj.getScores()
        _ = SaveScore.Save("./Output/ClinicalBert_ExpandedBoolQuery_scores_2019.csv",
                           query_id_list, scores)

        print("*...ClinicalBERT scores saved successfully...*")

    def ExtarctBaseLineQueryListfromfile_2019(self, and_file, or_file):
        obj = ExrtractScoresFromFile.ExtractList(and_file)
        extract_and_results = obj.extractScore()
        obj1 = ExrtractScoresFromFile.ExtractList(or_file)
        extract_or_results = obj1.extractScore()
        obj = IntialSetup.ListIntialSetUp(extract_and_results, extract_or_results)
        results = obj.arrangeBaseLineQueryLength()
        return results

    def ExtractBaseLineScoresFromFiles_2019(self, and_file, or_file, out_file):
        results = self.ExtarctBaseLineQueryListfromfile_2019(and_file, or_file)
        extract_and_results = results[0]
        extract_or_results = results[1]

        save_obj = SaveCombineQueryExapansionScore.SaveCombineQueryExapnsion(out_file, extract_and_results, extract_or_results)
        save_obj.extractandSaveBaseLineQueryScore()
        print("*...scores saved successfully...*")


    def extarctQueryExpanisonListsfromfile_2019(self, and_file, or_file, combine_file):
        obj = ExrtractScoresFromFile.ExtractList(and_file)
        extract_and_results = obj.extractScore()

        obj1 = ExrtractScoresFromFile.ExtractList(or_file)
        extract_or_results = obj1.extractScore()

        obj2 = ExrtractScoresFromFile.ExtractList(combine_file)
        extract_expanded_results = obj2.extractScore()

        obj = IntialSetup.ListIntialSetUp(extract_and_results,extract_or_results,extract_expanded_results)
        results = obj.arrangeQueryExpansionLength()

        return results

    def extractScoresFromFiles_2019(self, and_file, or_file, combine_file, out_file):
        results = self.extarctQueryExpanisonListsfromfile_2019(and_file, or_file, combine_file)
        extract_and_results = results[0]
        extract_or_results = results[1]
        extract_expanded_results = results[2]

        save_obj = SaveCombineQueryExapansionScore.SaveCombineQueryExapnsion(out_file,
                                                                                  extract_and_results,
                                                                                  extract_or_results,
                                                                                  extract_expanded_results)
        save_obj.extractandSaveQueryExapansionScore()
        print("*...scores saved successfully...*")

    def getScoreUsingCombinedQuery_2019(self, query_file_path, search_index, and_file, or_file, combine_file):
        combine_query_results = self.getScoresusingCombinedBoolQuery(query_file_path, search_index)

        and_bool_results = combine_query_results[0]
        or_bool_results = combine_query_results[1]

        and_bool_results_score = and_bool_results[0]
        and_bool_results_id = and_bool_results[1]

        or_bool_results_score = or_bool_results[0]
        or_bool_results_id = or_bool_results[1]

        _ = SaveScore.Save(and_file, and_bool_results_id, and_bool_results_score)
        _ = SaveScore.Save(or_file, or_bool_results_id, or_bool_results_score)
        _ = SaveCombineScore.Savecombine(combine_file,
                                         and_bool_results_score,
                                         or_bool_results_score,
                                         and_bool_results_id,
                                         or_bool_results_id)

        print("*...scores saved successfully...*")


    def perform_TREC_2019(self):
        self.basicpreprocessing_2019('./Data/TREC_2019_input_data',
                                     './Data/TREC_2019_Output_data')
        self.indexing_2019('./Data/TREC_2019_Output_data',
                           "2019-trec-precision-medicine-final")

        file = Path('/home/junhua/trec/Trec2021/Output/Final_AND_BoolQuery_scores_2019.csv')
        if file.is_file():
            self.ExtractBaseLineScoresFromFiles_2019('./Output/Final_AND_BoolQuery_scores_2019.csv',
                                                     './Output/Final_OR_BoolQuery_scores_2019.csv',
                                                     './Output/Final_Combined_BoolQuery_scores_2019.csv')
            self.extractScoresFromFiles_2019('./Output/Final_AND_BoolQuery_scores_2019.csv',
                                             './Output/Final_OR_BoolQuery_scores_2019.csv',
                                             './Output/New_ExpandedBoolQuery_scores_2019.csv')
        else:
            self.getScoreUsingCombinedQuery_2019("./Data/2019_quries/topics2019.xml",
                                                 "2019-trec-precision-medicine-final",
                                                 "./Output/Final_AND_BoolQuery_scores_2019.csv",
                                                 "./Output/Final_OR_BoolQuery_scores_2019.csv")





    ################################# 2016 ##############################

    def basicpreprocessing2016(self, source_file, dest_file):
        preprocessing_obj = BasicPreprocessing_2016.Preprocessing_2016(source_file, dest_file)
        print("Corpus preparation is Done")
        preprocessing_obj.getRootJsonObject()
        print("Basic Preprocessing is done successfully.")

    def indexing_2016(self, out_put_path, search_index):#'./Data/TREC_2016_OutputData'
        _ = Indexing2016.Indexing_2016(out_put_path, search_index)
        print("Indexing is done")


    def getMetamapQueries_2016(self, source_file, query_type = " "):
        query_obj = Query2016.GetQuery_2016(source_file)
        if query_type == "NER":
            results = query_obj.getNERQueriesList(["Sl.No",
                                                   "queryID",
                                                   "note",
                                                   "description",
                                                   "summary",
                                                   "summary_NER",
                                                   "note_NER",
                                                   "description_NER"])
            return results
        elif query_type == "NER-Disease":
            results = query_obj.getNERQueriesList(["Sl.No",
                                                   "queryID",
                                                   "summary",
                                                   "summary_NER3",
                                                   "description",
                                                   "description_NER3",
                                                   "note",
                                                   "note_NER3"])
            return results
        elif query_type == "NER-Drug":
            results = query_obj.getNERQueriesList(["Sl.No",
                                                   "queryID",
                                                   "summary",
                                                   "summary_NERgdd",
                                                   "description",
                                                   "description_NERgdd",
                                                   "note",
                                                   "note_NERgdd"])
            return results
        elif query_type == "Weighted":
            results = query_obj.getQueryListWithId()
            return results
        elif query_type == "NER-All":
            results = query_obj.getNERQueriesList(["Sl.No",
                                                   "queryID",
                                                   "summary",
                                                   "summary_NER_all",
                                                   "description",
                                                   "description_NER_all",
                                                   "note","note_NER_all"])
            return results
        else:
            results = query_obj.getMetamapQueryListWithId()
            return results

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
        elif type == "NER-All":
            query_id_list = result[1]
            sum_query_list = result[3]

        score_obj = BoolQuery2016.GetBoolQuery_2016(sum_query_list, query_id_list)
        results = score_obj.prepareBoolQuery("AND")
        score_res = results[0]
        query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(score_res, query_id, out_and_file)

        results = score_obj.prepareBoolQuery("OR")
        or_score_res = results[0]
        or_query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(or_score_res, or_query_id, out_or_file)

        print("Summary scores saved successfully")

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

    def getFilterMetamapQueries_2016(self, source_file):
        query_obj = Query2016.GetQuery_2016(source_file)
        results = query_obj.getFilteredMetamapQueryListWithId()
        return results

    def getFilterMetamapBoolQueryscore_2016(self, out_file):
        result = self.getFilterMetamapQueries_2016()
        query_id_list = result[0]
        filter_query_list = result[1]
        score_obj = BoolQuery2016.GetBoolQuery_2016(filter_query_list, query_id_list)
        results = score_obj.prepareBoolQuery()
        score_res = results[0]
        query_id = results[1]
        _ = SaveScore2016.SaveScore_2016(score_res, query_id,out_file)#"/home/junhua/trec/Trec2021/Output/Filter_Summary_AND_Metamap_BoolQuery_scores_2016.csv"
        print("Summary scores saved successfully")

    def ExtarctNERBaseLineQueryListfromfile_2016(self, and_file, or_file, combined_files = False):
        obj = ExrtractScoresFromFile.ExtractList(and_file)
        obj1 = ExrtractScoresFromFile.ExtractList(or_file)
        extract_and_results = tuple()
        extract_or_results = tuple()
        if combined_files == True:
            extract_and_results = obj.extractCombinedDocScores()
            extract_or_results = obj1.extractCombinedDocScores()
        else:
            extract_and_results = obj.extractScore()
            extract_or_results = obj1.extractScore()
        obj = IntialSetup.ListIntialSetUp(extract_and_results,
                                          extract_or_results)
        results = obj.arrangeBaseLineQueryLength()
        return results

    def ExtractNERBaseLineScoresFromFiles_2016(self,
                                               and_file,
                                               or_file,
                                               out_file,
                                               combined_files=False):
        results = self.ExtarctNERBaseLineQueryListfromfile_2016(and_file,
                                                                or_file,
                                                                combined_files)
        extract_and_results = results[0]
        extract_or_results = results[1]

        save_obj = SaveCombineQueryExapansionScore.SaveCombineQueryExapnsion(out_file,
                                                                             extract_and_results,
                                                                             extract_or_results)
        save_obj.extractandSaveBaseLineQueryScore()

        print("*... 2016 scores saved successfully...*")

    def combineBothCombineFiles_2016(self):
        self.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/New_Summary_Combined_NER_BoolQuery_scores_2016.csv',
                                                    '/home/junhua/trec/Trec2021/Output/Summary_Combined_5w-1gram_2016.csv',
                                                    '/home/junhua/trec/Trec2021/Output/Combined_drug_with5w-1g_2016.csv',
                                                    True)


    def perform_TREC_2016(self):
        self.basicpreprocessing2016('./Data/2016_Trec_Basic_Input','./Data/TREC_2016_OutputData')
        self.indexing_2016('./Data/TREC_2016_OutputData', "2016-trec-precision-medicine-final")

        self.GetNERMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_gene-disease-drug.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016.csv',"NER-Drug")
        self.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_Combined_NER_BoolQuery_scores_2016.csv')

        self.GetNERMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_gene-disease.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease_2016.csv','/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease_2016.csv' ,"NER-Disease")
        self.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease_2016.csv','/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease_2016.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_Combined_NER-BERN_Query2016_gene-disease_2016.csv')

        self.GetNERMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_all.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_all.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_all.csv',"NER-All")
        self.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_all.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_all.csv', '/home/junhua/trec/Trec2021/Output/New_Summary_Combined_New_Summary_OR_NER-BERN_Query2016_all.csv')

        self.GetNERMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/KeywordExtr_Query2016_5w-1gram.csv', '/home/junhua/trec/Trec2021/Output/Summary_AND_5w-1gram_2016.csv', '/home/junhua/trec/Trec2021/Output/Summary_OR_5w-1gram_2016.csv',"Weighted")
        self.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/Summary_AND_5w-1gram_2016.csv', '/home/junhua/trec/Trec2021/Output/Summary_OR_5w-1gram_2016.csv', '/home/junhua/trec/Trec2021/Output/Summary_Combined_5w-1gram_2016.csv')

        self.combineBothCombineFiles_2016()

        self.GetMetamapBoolQueryscore_2016('./Data/2016_Quries/NER-BERN_Query2016_all.csv',
                                           './Output/Summary_AND_Metamap_BoolQuery_scores_2016.csv')

        self.getFilterMetamapBoolQueryscore_2016('./Data/2016_Quries/Metamap_summary_query_filtered.csv')


    ##################################### 2021 #################################################

    def basicpreprocessing_2021(self, source_file, dest_file):
        basic_preprocessing = BasicPreprocessing_2021.Preprocessing_2021(source_file, dest_file)
        basic_preprocessing.getRootJsonObject()
        print("************** Preprocessing of 2021 done successfully *******************")

    def indexing_2021(self, out_file, index_name):
        _ = Indexing2021.Indexing_2021(out_file,index_name)
        print("************** Indexing 2021 done successfully *******************")

    def getQueryList_2021(self, source_file, query_type=" "):
        query_obj = Query2016.GetQuery_2016(source_file)
        if query_type == "NER-BERN":
            results = query_obj.getNERQueriesList(["Sl.No",
                                                   "QueryID",
                                                   "Age",
                                                   "Gender",
                                                   "Main_text",
                                                   "Main_text_NER",
                                                   "NERgdd"])
            return results

    def getQueryscore_2021(self, source_file, out_and_file, out_or_file, type, query_type, search_index):
        result = self.getQueryList_2021(source_file, type)
        query_id_list = list()
        sum_query_list = list()
        if type == "NER-BERN":
            query_id_list = result[1]
            sum_query_list = result[6]

        score_obj = BoolQuery2016.GetBoolQuery_2016(sum_query_list, query_id_list, search_index)
        results = score_obj.prepareBoolQuery(query_type)
        score_res = results[0]
        query_id = results[1]

        _ = Savescore2021.Savescore_2021(score_res, query_id, out_and_file)

        print(" ***************** Summary scores of 2021 saved successfully ************ ")


    def perform_TREC_2021(self):
        self.basicpreprocessing_2021('./Data/TREC_2021_Basicpreprocessing_Input',
                                     './Data/TREC_2021_Basicpreprocessing_output')
        self.indexing_2021('./Data/TREC_2021_Basicpreprocessing_output',
                           "2021-trec-precision-medicine-final")
        self.getQueryscore_2021('./Data/2021Quries/NER-BERN_Query2021_gene-disease-drug.csv',
                                '/home/junhua/trec/Trec2021/Output/Source_NER-BERN_Query_gene-disease-drug_2021.csv',
                                ' ',
                                "NER-BERN",
                                "AND",
                                "2021-trec-precision-medicine-final")

    def perform_TREC(self, year):
        if year == "2016":
            self.perform_TREC_2016()
        elif year == "2019":
            self.perform_TREC_2019()
        elif year == "2021":
            self.perform_TREC_2021()

if __name__ == '__main__':
    main_obj = Main()
    main_obj.perform_TREC("2019")

        




