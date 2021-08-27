from Preprocessing import BasicPreprocessing_2021, BasicPreprocessing, BasicPreprocessing_2016
from Indexing import Indexing2016, Indexing2019, Indexing2021
from Queries import BoolQuery, BoolQuery2016,Queries, Query2016
from QueryExpansion import BoolQueryExpansion,CombinedQuery,ExapnsionScore_2016,Queryexpansion,QueryExpansion_2016,QueryExpansionList
from Ref import Corpus, OkapiBm25
from Ref import Bm25_scoring
from Retrieval import Savescore2021, SaveScore2016, SaveScore, SaveCombineScore, SaveCombineQueryExapansionScore
from Utilities import ExtractScoresFromFile, IntialSetup, Evaluation

from pathlib import Path
from datetime import datetime
import os

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
        obj = ExtractScoresFromFile.ExtractList(and_file)
        extract_and_results = obj.extractScore()
        obj1 = ExtractScoresFromFile.ExtractList(or_file)
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
        obj = ExtractScoresFromFile.ExtractList(and_file)
        extract_and_results = obj.extractScore()

        obj1 = ExtractScoresFromFile.ExtractList(or_file)
        extract_or_results = obj1.extractScore()

        obj2 = ExtractScoresFromFile.ExtractList(combine_file)
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

    def getrawqueries_2016(self, query_file_path):
        obj = Queries.GetQuery(query_file_path)
        query_list = obj.getQueryList()
        return query_list

    def getMetamapQueries_2016(self, source_file, query_type = " "):
        query_obj = Query2016.GetQuery_2016(source_file)
        results = ()
        
        if query_type == "NER":
            results = query_obj.getNERQueriesList(["Sl.No",
                                                   "queryID",
                                                   "note",
                                                   "description",
                                                   "summary",
                                                   "summary_NER",
                                                   "note_NER",
                                                   "description_NER"])
        elif query_type == "NER-Disease":
            results = query_obj.getNERQueriesList(["Sl.No",
                                                   "queryID",
                                                   "summary",
                                                   "summary_NER3",
                                                   "description",
                                                   "description_NER3",
                                                   "note",
                                                   "note_NER3"])
        
        elif query_type == "NER-Drug" or query_type == "NER-Drug-Sum_Desc_Note":
            column_list = ["Sl.No","queryID","summary",
                          "summary_NERgdd","description",
                          "description_NERgdd","note",
                          "note_NERgdd"]
        
            if query_type == "NER-Drug":
                results = query_obj.getNERQueriesList(column_list)
            elif query_type == "NER-Drug-Sum_Desc_Note":
                results = query_obj.getNERCombinedQueriesList(column_list)

        elif query_type == "Weighted":
            results = query_obj.getQueryListWithId()
        
        elif query_type == "NER-All":
            results = query_obj.getNERQueriesList(["Sl.No",
                                                   "queryID",
                                                   "summary",
                                                   "summary_NER_all",
                                                   "description",
                                                   "description_NER_all",
                                                   "note","note_NER_all"])
        elif query_type == "Reformated":
            results = query_obj.getNERQueriesList(["Sl.No",
                                                   "queryID",
                                                   "query_concept",
                                                   "extended_concept"])
        else:
            results = query_obj.getMetamapQueryListWithId()
        
        return results

    def GetNERMetamapBoolQueryscore_2016(self, source_file, out_and_file, out_or_file ,type, subtype = ""):
        result = self.getMetamapQueries_2016(source_file, type)
        query_id_list = list()
        sum_query_list = list()
        query_id_list = result[1]
        if type == "NER":
            sum_query_list = result[5]
        elif type == "NER-Disease":
            sum_query_list = result[3]
        elif type == "NER-Drug":
            if subtype == "summary":
                sum_query_list = result[3]
            elif subtype == "Description":
                sum_query_list = result[5]
            elif subtype == "Note":
                sum_query_list = result[7]
        elif type == 'NER-Drug-Sum_Desc_Note':
            sum_query_list = result[7]
        elif type == "Weighted":
            sum_query_list = result[1]
        elif type == "NER-All":
            sum_query_list = result[3]
        elif type == "Reformated":
            sum_query_list = result[2]

        score_obj = BoolQuery2016.GetBoolQuery_2016("", sum_query_list, query_id_list)
        results = score_obj.prepareBoolQuery("AND")
        score_res = results[0]
        query_id = results[1]
        query_string = []#results[2]

        _ = SaveScore2016.SaveScore_2016(score_res, query_id, out_and_file, query_string)

        results = score_obj.prepareBoolQuery("OR")
        or_score_res = results[0]
        or_query_id = results[1]
        query_string = []#results[2]

        _ = SaveScore2016.SaveScore_2016(or_score_res, or_query_id, out_or_file,query_string)

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
        obj = ExtractScoresFromFile.ExtractList(and_file)
        obj1 = ExtractScoresFromFile.ExtractList(or_file)
        if combined_files == True:
            extract_and_results = obj.extractCombinedDocScores()
            extract_or_results = obj1.extractCombinedDocScores()
        else:
            extract_and_results = obj.extractScore()
            extract_or_results = obj1.extractScore()
        obj = IntialSetup.ListIntialSetUp(extract_and_results,
                                          extract_or_results)
        results = obj.arrangeBaseLineQueryLength_combinational()
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
        save_obj.extractandSaveBaseLineQueryScoreWithoutDocument()
        #save_obj.extractandSaveBaseLineQueryScore()
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

        self.GetNERMetamapBoolQueryscore_2016(
            '/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_gene-disease-drug.csv',
            '/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016_1.csv',
            '/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016_1.csv',
            "NER-Drug")

        self.ExtractNERBaseLineScoresFromFiles_2016(
            '/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016_1.csv',
            '/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016_1.csv',
            '/home/junhua/trec/Trec2021/Output/NNew_Summary_Combined_NER-BERN_Query2016_gene-disease-drug_2016_1.csv')
    
    def get_dateTime(self):
        now = datetime.today().isoformat()
        return str(now)
    def get_file_name(self, filepath):
        filename = os.path.basename(filepath)
        return filename
    
    def getSummaryscores(self, query_file_path):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)        
        and_file_name = './Output/Summary_AND_'+ time + '_'+ filename
        or_file_name = './Output/Summary_OR_'+ time + '_'+ filename
        comb_file_name = './Output/Summary_COMBINED_'+ time + '_'+ filename
        
        self.GetNERMetamapBoolQueryscore_2016(query_file_path,
                                              and_file_name,
                                              or_file_name,
                                              "NER-Drug",
                                              "summary")
        self.ExtractNERBaseLineScoresFromFiles_2016(and_file_name,
                                                    or_file_name,
                                                    comb_file_name)

    def getDescriptionScores(self, query_file_path):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Description_AND_' + time + '_' + filename
        or_file_name = './Output/Description_OR_' + time + '_' + filename
        comb_file_name = './Output/Description_COMBINED_' + time + '_' + filename
        
        self.GetNERMetamapBoolQueryscore_2016(query_file_path,
                                              and_file_name,
                                              or_file_name,
                                              "NER-Drug",
                                              "Description")
        self.ExtractNERBaseLineScoresFromFiles_2016(and_file_name,
                                                    or_file_name,
                                                    comb_file_name)

    def getNoteScores(self, query_file_path):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Notes_AND_' + time + '_' + filename
        or_file_name = './Output/Notes_OR_' + time + '_' + filename
        comb_file_name = './Output/Notes_COMBINED_' + time + '_' + filename

        self.GetNERMetamapBoolQueryscore_2016(query_file_path,
                                              and_file_name,
                                              or_file_name,
                                              "NER-Drug",
                                              "Note")
        self.ExtractNERBaseLineScoresFromFiles_2016(and_file_name,
                                                    or_file_name,
                                                    comb_file_name)

    def getCombined_Sum_Desc_Note_scores_2016(self, query_file_path):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Sum_Descrition_Notes_AND_' + time + '_' + filename
        or_file_name = './Output/Sum_Descrition_Notes_OR_' + time + '_' + filename
        comb_file_name = './Output/Sum_Descrition_Notes_COMBINED_' + time + '_' + filename

        self.GetNERMetamapBoolQueryscore_2016(query_file_path,
                                              and_file_name,
                                              or_file_name,
                                              "NER-Drug-Sum_Desc_Note",
                                              "Sum-Desc-Note")
        self.ExtractNERBaseLineScoresFromFiles_2016(and_file_name,
                                                    or_file_name,
                                                   comb_file_name)

    def getRawQueries_2016(self):
        #file_path = input("Please enter 2016 query filepath:")
        file_path = '/home/junhua/trec/Trec2021/Data/2016_Quries/topics2016.xml'
        score_obj = BoolQuery2016.GetBoolQuery_2016(file_path)
        score_obj.prepareRawQuery()

    def getExapnsionQueries_2016(self, source_file, type):
        obj = None
        results = None
        # ['sl.no', 'queryID','summary','summary_keyword','summary_keyword_expansion','description','description_keyword','note','note_keyword'])
        if type == "Manual":
            obj = QueryExpansion_2016.ExapandedQuery_2016(source_file,
                                                          ['sl.no', 'queryID', 'Main_text', 'summary_keyword',
                                                           'summary_keyword_expansion'])
            #results = obj.getCombinedGroupeddata()
            results = obj.getExpansionQuery_2016()
        else:
            obj = QueryExpansion_2016.ExapandedQuery_2016(source_file,
                                  ['TopicID', 'entities', 'expend_query'])
            results = obj.getGroupedData()

        '''
        if type == "PRF":
            obj = QueryExpansion_2016.ExapandedQuery_2016(source_file,
                                  ['TopicID', 'entities', 'expend_query'])
        elif type == "KW":
            obj = QueryExpansion_2016.ExapandedQuery_2016(source_file,
                                                          ['TopicID', 'entities', 'expend_query'])
        elif type == "Metamap":
            obj = QueryExpansion_2016.ExapandedQuery_2016(source_file,
                                                          ['TopicID', 'entities', 'expend_query_metamap'])
        '''
        summary_tuple = results[0]
        description_tuple = results[1]
        note_tuple = results[2]

        return summary_tuple, description_tuple, note_tuple

    def getQueryExapansionscore_2016(self, query_file, and_out_file, or_out_file, query_type, type, out_file="", index = 0):
        results = self.getExapnsionQueries_2016(query_file, query_type)
        query_expansion_list = []
        query_list = []
        id_list = []
        if type == "summary":
            tuple = results[0]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]
        elif type == "description":
            tuple = results[1]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]
        elif type == "Note":
            tuple = results[2]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]

        '''
        score_obj = ExapnsionScore_2016.GetQueryExapnsionScore_2016(query_expansion_list, id_list, "2016-trec-precision-medicine-final")

        results = score_obj.getScores(" AND ")
        score_res = results[0]
        query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(score_res, query_id, and_out_file)

        results = score_obj.getScores(" OR ")
        or_score_res = results[0]
        or_query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(or_score_res, or_query_id, or_out_file)
        
        '''
        ids = [26, 29]
        for i in ids:
            index = id_list.index(i)
            score_obj = ExapnsionScore_2016.GetQueryExapnsionScore_2016(query_expansion_list, id_list,
                                                                    "2016-trec-precision-medicine-final")
            results = score_obj.getExpansionScores_2021(index, out_file, 'First')

        #score_obj = ExapnsionScore_2016.GetQueryExapnsionScore_2016(query_expansion_list, id_list,
        #                                                            "2016-trec-precision-medicine-final")

        #results = score_obj.getScores(" AND ")
        results = score_obj.getExpansionScores_2016(index, out_file)
        '''
        score_res = results[0]
        query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(score_res, query_id, and_out_file)

        results = score_obj.getScores(" OR ")
        or_score_res = results[0]
        or_query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(or_score_res, or_query_id, or_out_file)
        '''

    def query_exapansion_scores_2016(self, query_file_path, type, outfile, index=0):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Summary_AND_Raw' + time + '_' + filename
        or_file_name = './Output/Summary_OR__Raw' + time + '_' + filename
        comb_file_name = './Output/Summary_COMBINED__Raw' + time + '_' + filename
        
        self.getQueryExapansionscore_2016(query_file_path,
                                          and_file_name,
                                          or_file_name,
                                          type,
                                          "summary",
                                          outfile,
                                          index)
        '''
        self.ExtractNERBaseLineScoresFromFiles_2016(and_file_name,
                                                    or_file_name,
                                                    comb_file_name)
        '''
    def prf_queryExapansion_2016(self):
        self.getQueryExapansionscore_2016("/home/junhua/trec/Trec2021/Data/2016_Quries/PRF_entity_Bert_2016.csv",
                                             '/home/junhua/trec/Trec2021/Output/PRF_summary_queryexpansion_AND_2016-1.csv',
                                             '/home/junhua/trec/Trec2021/Output/PRF_summary_queryexpansion_OR_2016-1.csv',
                                             "PRF",
                                             "summary")
        self.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/PRF_summary_queryexpansion_AND_2016-1.csv',
                                                    '/home/junhua/trec/Trec2021/Output/PRF_summary_queryexpansion_OR_2016-1.csv',
                                                    '/home/junhua/trec/Trec2021/Output/PRF_summary_queryexpansion_Combined_2016-1.csv')

    def kw_queryExapansion_2016(self):
        self.getQueryExapansionscore_2016("/home/junhua/trec/Trec2021/Data/2016_Quries/PRF_KW_Bert_2016.csv",
                                             '/home/junhua/trec/Trec2021/Output/KW_summary_queryexpansion_AND_2016-1.csv',
                                             '/home/junhua/trec/Trec2021/Output/KW_summary_queryexpansion_OR_2016-1.csv',
                                             "KW",
                                             "summary")
        self.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/KW_summary_queryexpansion_AND_2016-1.csv',
                                                    '/home/junhua/trec/Trec2021/Output/KW_summary_queryexpansion_OR_2016-1.csv',
                                                    '/home/junhua/trec/Trec2021/Output/KW_summary_queryexpansion_Combined_2016-1.csv')

    def metamap_queryExapansion_2016(self):
        self.getQueryExapansionscore_2016("/home/junhua/trec/Trec2021/Data/2016_Quries/PRF_metamap_Bert_2016.csv",
                                             '/home/junhua/trec/Trec2021/Output/Metamap_summary_queryexpansion_AND_2016-1.csv',
                                             '/home/junhua/trec/Trec2021/Output/Metamap_summary_queryexpansion_OR_2016-1.csv',
                                             "Metamap",
                                             "summary")
        self.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/Metamap_summary_queryexpansion_AND_2016-1.csv',
                                                    '/home/junhua/trec/Trec2021/Output/Metamap_summary_queryexpansion_OR_2016-1.csv',
                                                    '/home/junhua/trec/Trec2021/Output/Metamap_summary_queryexpansion_Combined_2016-1.csv')

    def queryExpansion_2016(self):
        self.prf_queryExapansion_2016()
        self.kw_queryExapansion_2016()
        self.metamap_queryExapansion_2016()

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

    def bool_query_scores_2021(self):
        self.getQueryscore_2021('./Data/2021Quries/NER-BERN_Query2021_gene-disease-drug.csv',
                                '/home/junhua/trec/Trec2021/Output/Source_NER-BERN_Query_gene-disease-drug_2021.csv',
                                ' ',
                                "NER-BERN",
                                "AND",
                                "2021-trec-precision-medicine-final")

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
        
        
    #################################### 2016 ######################################################
        
    def get_bool_query_scores_2016(self, query_file_path):
        self.getSummaryscores(query_file_path)
        #self.getDescriptionScores(query_file_path)
        #self.getNoteScores(query_file_path)
        #self.getCombined_Sum_Desc_Note_scores_2016(query_file_path)
        
    def get_quey_expansion_scores_2016(self, query_file_path):
        self.query_exapansion_scores_2016(query_file_path)
        
    ################################## 2019 ##########################################################
    
    def get_bool_query_scores_2019(self, query_file_path):
        self.getSummaryscores(query_file_path)
        self.getDescriptionScores(query_file_path)
        self.getNoteScores(query_file_path)
        self.getCombined_Sum_Desc_Note_scores_2016(query_file_path)

    def get_quey_expansion_scores_2019(self, query_file_path):
        self.query_exapansion_scores_2016(query_file_path)
        
        
    ################################### 2021 #########################################

    def get_bool_query_scores_2021(self, query_file_path): 
        pass

    def query_exapansion_scores_2021(self, query_file_path, type, outfile, index=0):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Summary_AND_Raw' + time + '_' + filename
        or_file_name = './Output/Summary_OR__Raw' + time + '_' + filename
        comb_file_name = './Output/Summary_COMBINED__Raw' + time + '_' + filename

        self.getQueryExapansionscore_2021(query_file_path,
                                          and_file_name,
                                          or_file_name,
                                          type,
                                          "summary",
                                          outfile,
                                          index)

    def query_exapansion_scores_2021_2(self, query_file_path, type, outfile, index=0):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Summary_AND_Raw' + time + '_' + filename
        or_file_name = './Output/Summary_OR__Raw' + time + '_' + filename
        comb_file_name = './Output/Summary_COMBINED__Raw' + time + '_' + filename

        self.getQueryExapansionscore_2021_2(query_file_path,
                                          and_file_name,
                                          or_file_name,
                                          type,
                                          "summary",
                                          outfile,
                                          index)

    def query_exapansion_scores_2021_3(self, query_file_path, type, outfile, index=0):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Summary_AND_Raw' + time + '_' + filename
        or_file_name = './Output/Summary_OR__Raw' + time + '_' + filename
        comb_file_name = './Output/Summary_COMBINED__Raw' + time + '_' + filename

        self.getQueryExapansionscore_2021_3(query_file_path,
                                          and_file_name,
                                          or_file_name,
                                          type,
                                          "summary",
                                          outfile,
                                          index)


    def getExapnsionQueries_2021(self, source_file, type):
        obj = QueryExpansion_2016.ExapandedQuery_2016(source_file,
                                                      ['QueryID','Main_text','raw_list','Expansion_list'])
                                  #['sl.no','QueryID','raw_list','Expansion_list'])
        results = obj.getExpansionQuery_2021()
        #results = obj.getRawQuery()
        summary_tuple = results[0]
        description_tuple = results[1]
        note_tuple = results[2]
        return summary_tuple, description_tuple, note_tuple

    def getExapnsionQueries_2021_3(self, source_file, type):
        obj = QueryExpansion_2016.ExapandedQuery_2016(source_file,
                                                      ['sl.no','QueryID','raw_list', 'Expansion_list'])
                                  #['sl.no','QueryID','raw_list','Expansion_list'])
        results = obj.getExpansionQuery_2021()
        summary_tuple = results[0]
        description_tuple = results[1]
        note_tuple = results[2]
        return summary_tuple, description_tuple, note_tuple

    def getQueryExapansionscore_2021(self, query_file, and_out_file, or_out_file, query_type, type, out_file="", index = 0):
        results = self.getExapnsionQueries_2021(query_file, query_type)
        query_expansion_list = []
        query_list = []
        id_list = []
        if type == "summary":
            tuple = results[0]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]
        elif type == "description":
            tuple = results[1]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]
        elif type == "Note":
            tuple = results[2]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]

        for i in range(0, 10):
            #index = id_list.index(i)
            score_obj = ExapnsionScore_2016.GetQueryExapnsionScore_2016(query_list, id_list,
                                                                        "2021-trec-precision-medicine-final")
            results = score_obj.getExpansionScores_2021(i,
                                                        '/home/junhua/trec/Trec2021/Output/2021Output/Run1/KeywordExtr_Query2021_unigram_12_1.csv',
                                                        'First')

    def getQueryExapansionscore_2021_2(self, query_file, and_out_file, or_out_file, query_type, type, out_file="",
                                     index=0):
        results = self.getExapnsionQueries_2021(query_file, query_type)
        query_expansion_list = []
        query_list = []
        id_list = []
        if type == "summary":
            tuple = results[0]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]
        elif type == "description":
            tuple = results[1]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]
        elif type == "Note":
            tuple = results[2]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]

        ids = [24,48,50]
        for i in ids:
            index = id_list.index(i)
            score_obj = ExapnsionScore_2016.GetQueryExapnsionScore_2016(query_list, id_list,
                                                                        "2021-trec-precision-medicine-final")
            results = score_obj.getExpansionScores_2021(index,
                                                        '/home/junhua/trec/Trec2021/Output/2021Output/Run2/RUN2_RAW_manualKW_joined_1-75_B-reformated_Aug12_5_n-n-2.csv',
                                                        'last')

    def getQueryExapansionscore_2021_3(self, query_file, and_out_file, or_out_file, query_type, type, out_file="",
                                     index=0):
        results = self.getExapnsionQueries_2021_3(query_file, query_type)
        query_expansion_list = []
        query_list = []
        id_list = []
        if type == "summary":
            tuple = results[0]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]
        elif type == "description":
            tuple = results[1]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]
        elif type == "Note":
            tuple = results[2]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
            query_list = tuple[2]

        ids = [50, 56, 72]
        for i in ids:
            index = id_list.index(i)
            score_obj = ExapnsionScore_2016.GetQueryExapnsionScore_2016(query_expansion_list, id_list,
                                                                        "2021-trec-precision-medicine-final")
            results = score_obj.getExpansionScores_2021(index,
                                                        '/home/junhua/trec/Trec2021/Output/2021Output/Run3/EXP_Final_combined-n-2-1.csv',
                                                        'First')

    def get_quey_expansion_scores_2021(self, query_file_path):
        self.query_exapansion_scores_2016(query_file_path)

    ###########################################################################################################

    def perform_TREC(self, year):
        if year == 1:
            self.perform_TREC_2016()
        elif year == 2:
            self.perform_TREC_2019()
        elif year == 3:
            self.perform_TREC_2021()
            
    def getQueryresults(self, year, query_file_path):
        if year == 1:
           self.get_bool_query_scores_2016(query_file_path)
        elif year == 2:
            self.get_bool_query_scores_2019(query_file_path)
        elif year == 3:
            self.get_bool_query_scores_2021(query_file_path)
            
    def getQueryExapnsionResults(self, year, query_file_path):
        if year == 1:
            self.get_quey_expansion_scores_2016(query_file_path)
        elif year == 2:
            self.get_quey_expansion_scores_2019(query_file_path)
        elif year == 3:
            self.get_quey_expansion_scores_2021(query_file_path)

    def main(self):
        year_input = input("Which year you want to process queries \n 1.2016 2. 2019 3. 2021")
        query_type = input("Enter your Query type 1.Basic Query 2.Expanded QUery")
        query_file_path = input("Enter query_file_path")
        if query_type == 1:
            self.getQueryresults(year_input, query_file_path)
        elif query_type == 2:
            self.getQueryExapansionscore_2016(year_input, query_file_path)


    def evaluation(self):
        obj = Evaluation.GetDuplicates('/home/junhua/trec/Trec2021/Output/combined_rerank_cross_output_f5k_OR_rawq_2k-1.csv')


if __name__ == '__main__':
    main_obj = Main()
    #main_obj.perform_TREC("2019")
    # main_obj.GetNERMetamapBoolQueryscore_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_gene-disease-drug.csv', '/home/junhua/trec/Trec2021/Output/Text_New_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016.csv', '/home/junhua/trec/Trec2021/Output/Text_New_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016.csv',"NER-Drug")
    # main_obj.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/Text_New_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016.csv', '/home/junhua/trec/Trec2021/Output/Text_New_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016.csv', '/home/junhua/trec/Trec2021/Output/Text_New_Summary_Combined_NER_BoolQuery_scores_2016.csv')
    #results = main_obj.getMetamapQueries_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_gene-disease-drug.csv',query_type = "NER-Drug")
    #main_obj.GetNERMetamapBoolQueryscore_2016('./Data/2016_Quries/Meta_query2016_summary_3types_B-reformated.csv','./Output/New_Summary_AND_Reformated_Query2016.csv','./Output/Text_New_Summary_OR_Reformated_Query2016.csv',"Reformated")
    #main_obj.GetNERMetamapBoolQueryscore_2016('./Data/2016_Quries/summary_sometypes_Reformated_2016.csv',
     #                                         './Output/SomeTypes_Summary_AND_Reformated_Query2016.csv',
     #                                         './Output/SomeTypes_New_Summary_OR_Reformated_Query2016.csv',"Reformated")

    #main_obj.getNER_GeneDiseaseDrug_2016()
    #main_obj.getRawQueries_2016()
    #main_obj.prf_queryExapansion_2016()
    #main_obj.kw_queryExapansion_2016()
    #main_obj.metamap_queryExapansion_2016()

    #main_obj.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/Bhanu_New_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016-1_5000.csv',
    #                                                '/home/junhua/trec/Trec2021/Output/semantic_output_f5k_OR_rawq.csv',
    #                                                '/home/junhua/trec/Trec2021/Output/combined_semantic_cross_output_f5k_OR_rawq_2k-1.csv')

    #main_obj.queryExpansion_2016()
    #main_obj.evaluation()

    #main_obj.GetNERMetamapBoolQueryscore_2016(
    #        '/home/junhua/trec/Trec2021/Data/2016_Quries/NER-BERN_Query2016_gene-disease-drug.csv',
    #        '/home/junhua/trec/Trec2021/Output/Reranking_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016_1.tsv',
    #        '/home/junhua/trec/Trec2021/Output/Reranking_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016_1.tsv',
    #        "NER-Drug", "summary")


    #main_obj.query_exapansion_scores_2016('./Data/2016_Quries/Manual_KeywordExtr_Query2016_.csv', "Manual")
    #main_obj.query_exapansion_scores_2016('./Data/2016_Quries/New_PRF_entity_Bert_2016.csv', "PRF")
    #main_obj.query_exapansion_scores_2016('./Data/2016_Quries/New_PRF_KW_Bert_2016.csv', "KW")
    #main_obj.query_exapansion_scores_2016('./Data/2016_Quries/New_PRF_metamap_Bert_2016.csv', "Metamap")
    #main_obj.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/Summary_AND_2021-07-20T14:03:05.844488_Manual_KeywordExtr_Query2016_.csv',
    #                                     '/home/junhua/trec/Trec2021/Output/Summary_OR_2021-07-20T14:03:05.844488_Manual_KeywordExtr_Query2016_.csv',
    #                                     '/home/junhua/trec/Trec2021/Output/Bhanu.combined.csv')

    #main_obj.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/Summary_AND_Raw2021-07-21T11_07_02.983398_Manual_KeywordExtr_Query2016_.csv',
    #                                                '/home/junhua/trec/Trec2021/Data/2016_Quries/rerank_cross_output_Sum_OR_QExp_Manual_KwExtr_Q2016_f2k_2k_J27.csv',
    #                                               '/home/junhua/trec/Trec2021/Output/Combined_Summary_ANDrerank_cross_2016.csv')



    #main_obj.query_exapansion_scores_2021('/home/junhua/trec/Trec2021/Data/2021Quries/KeywordExtr_Query2021_unigram_12w.csv',
    #                                      "",
    #                                      '')

    #main_obj.query_exapansion_scores_2021_2('/home/junhua/trec/Trec2021/Data/2021Quries/raw-exp_manualKW_joined_1-75_B-reformated_Aug12_5.csv',
    #                                      "",
    #                                      '')
    '''
    main_obj.query_exapansion_scores_2016('/home/junhua/trec/Trec2021/Data/2016_Quries/Manual_KeywordExtr_Query2016_aug3-2_B-reformated.csv',
                                          "Manual",
                                          '/home/junhua/trec/Trec2021/Output/Bhanu-EXP-Manual_KeywordExtr_Query2016_aug3-2_B-reformated-n-2-1.csv',
                                          25)
    '''

    '''
    main_obj.query_exapansion_scores_2021('/home/junhua/trec/Trec2021/Data/2016_Quries/raw-exp_manualKW_joined_1-75_B-reformated_Aug12.csv',
                                           "Manual",
                                          '/home/junhua/trec/Trec2021/Output/2021Output/2021_new_query_expansion/raw-exp_manualKW_joined_1-75_B-reformated_Aug12.cs')

    for i in range(0,76):
        main_obj.query_exapansion_scores_2021('./Data/2021Quries/raw-exp_manualKW_joined_1-75_B-reformated.csv',
                                          "Manual",
                                          '/home/junhua/trec/Trec2021/Output/2021Output/2021_query_expansion_5000/Query_expansion_Combinational_n-n-2-5000_score_2021.csv',

    main_obj.query_exapansion_scores_2016('./Data/2016_Quries/Manual_KeywordExtr_Query2016_aug3_B-reformated.csv',
                                          "Manual",
                                          '/home/junhua/trec/Trec2021/Output/Final_Raw_combinational_score_2021_query.csv',
                                          25)

    main_obj.query_exapansion_scores_2016('./Data/2016_Quries/Manual_KeywordExtr_Query2016_aug3_B-reformated.csv',
                                          "Manual",
                                          '/home/junhua/trec/Trec2021/Output/Final_RAW_EXP_combinational_score_2016_query_exp_n-2-1.csv',
                                          25)
    main_obj.query_exapansion_scores_2016('./Data/2016_Quries/Manual_KeywordExtr_Query2016_aug3_B-reformated.csv',
                                          "Manual",
                                          '/home/junhua/trec/Trec2021/Output/Final_Expansion_combinational_score_2016_query_exp_29.csv',
                                          28)
    print("29")

    main_obj.query_exapansion_scores_2016('./Data/2016_Quries/Manual_KeywordExtr_Query2016_aug3_B-reformated.csv',
                                          "Manual",
                                          '/home/junhua/trec/Trec2021/Output/Final_Expansion_combinational_score_2016_query_exp_20.csv',
                                          19)
    print("25")
    '''

    main_obj.ExtractNERBaseLineScoresFromFiles_2016('/home/junhua/trec/Trec2021/Output/2016QueryOutput/2016Reranking/All_merge.csv',
                                                    '/home/junhua/trec/Trec2021/Output/Bhanu-RAW-EXP-RAW-EXP-Manual_KeywordExtr_Query2016_aug3-2_B-reformated-n-n-2.csv',
                                                    '/home/junhua/trec/Trec2021/Output/2016QueryOutput/2016Reranking/Bhanu-All_merge.csv')

