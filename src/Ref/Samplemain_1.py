from Preprocessing import BasicPreprocessing_2016
from Indexing import Indexing2016
from Queries import BoolQuery, BoolQuery2016,Queries, Query2016
from QueryExpansion import BoolQueryExpansion,CombinedQuery,ExapnsionScore_2016, QueryExpansion_2016,QueryExpansionList
from Retrieval import Savescore2021, SaveScore2016, SaveScore, SaveCombineScore, SaveCombineQueryExapansionScore
from Utilities import ExtractScoresFromFile, IntialSetup

from datetime import datetime
import os


class SampleMain:
    
    def get_dateTime(self):
        now = datetime.today().isoformat()
        return str(now)
    def get_file_name(self, filepath):
        filename = os.path.basename(filepath)
        return filename
        
        
    ############################################ 2016 ###################################################################

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

    def getRawQueries_2016(self):
        # file_path = input("Please enter 2016 query filepath:")
        file_path = '/home/junhua/trec/Trec2021/Data/2016_Quries/topics2016.xml'
        score_obj = BoolQuery2016.GetBoolQuery_2016(file_path)
        score_obj.prepareRawQuery()

    def getMetamapQueries_2016(self, source_file):
        query_obj = Query2016.GetQuery_2016(source_file)
        results = query_obj.getNERQueriesList(["Sl.No",
                                               "queryID",
                                               "note",
                                               "description",
                                               "summary",
                                               "summary_NER",
                                               "note_NER",
                                               "description_NER"])
        return results

    def GetNERMetamapBoolQueryscore_2016(self, source_file, out_and_file, out_or_file ,subtype = ""):
        result = self.getMetamapQueries_2016(source_file)
        query_id_list = []
        query_list = []
        if subtype == "Summary":
            query_id_list = result[1]
            query_list = result[5]
        elif subtype == "Description":
            query_id_list = result[1]
            query_list = result[5]
        elif subtype == "Notes":
            query_id_list = result[1]
            query_list = result[5]
        
        score_obj = BoolQuery2016.GetBoolQuery_2016(query_list, query_id_list)
        results = score_obj.prepareBoolQuery("AND")
        score_res = results[0]
        query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(score_res, query_id, out_and_file)

        results = score_obj.prepareBoolQuery("OR")
        or_score_res = results[0]
        or_query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(or_score_res, or_query_id, out_or_file)

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

    def getSummaryscores(self, query_file_path):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Summary_AND_'+ time + '_'+ filename
        or_file_name = './Output/Summary_OR_'+ time + '_'+ filename
        comb_file_name = './Output/Summary_COMBINED_'+ time + '_'+ filename

        self.GetNERMetamapBoolQueryscore_2016(query_file_path,
                                              and_file_name,
                                              or_file_name,
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
                                              "Sum-Desc-Note")
        self.ExtractNERBaseLineScoresFromFiles_2016(and_file_name,
                                                    or_file_name,
                                                    comb_file_name)

    def getExapnsionQueries_2016(self, source_file):
        obj = QueryExpansion_2016.ExapandedQuery_2016(source_file,
                                                      ['TopicID', 'entities', 'expend_query_entity'])
        results = obj.getGroupedData()
        summary_tuple = results[0]
        description_tuple = results[1]
        note_tuple = results[2]

        return summary_tuple, description_tuple, note_tuple

    def getQueryExapansionscore_2016(self, query_file, and_out_file, or_out_file, type):
        results = self.getExapnsionQueries_2016(query_file)
        query_list = []
        id_list = []
        if type == "Summary":
            tuple = results[0]
            query_list = tuple[0]
            id_list = tuple[1]
        elif type == "Description":
            tuple = results[1]
            query_list = tuple[0]
            id_list = tuple[1]
        elif type == "Notes":
            tuple = results[2]
            query_list = tuple[0]
            id_list = tuple[1]

        score_obj = ExapnsionScore_2016.GetQueryExapnsionScore_2016(query_list, id_list, "2016-trec-precision-medicine-final")

        results = score_obj.getScores("AND")
        score_res = results[0]
        query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(score_res, query_id, and_out_file)

        results = score_obj.getScores("OR")
        or_score_res = results[0]
        or_query_id = results[1]

        _ = SaveScore2016.SaveScore_2016(or_score_res, or_query_id, or_out_file)

    def query_summary_exapansion_scores_2016(self, query_file_path):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Summary_AND_' + time + '_' + filename
        or_file_name = './Output/Summary_OR_' + time + '_' + filename
        comb_file_name = './Output/Summary_COMBINED_' + time + '_' + filename

        self.getQueryExapansionscore_2016(query_file_path,
                                          and_file_name,
                                          or_file_name,
                                          "Summary")
        self.ExtractNERBaseLineScoresFromFiles_2016(and_file_name,
                                                    or_file_name,
                                                    comb_file_name)

    def query_description_exapansion_scores_2016(self, query_file_path):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Summary_AND_' + time + '_' + filename
        or_file_name = './Output/Summary_OR_' + time + '_' + filename
        comb_file_name = './Output/Summary_COMBINED_' + time + '_' + filename

        self.getQueryExapansionscore_2016(query_file_path,
                                          and_file_name,
                                          or_file_name,
                                          "Description")
        self.ExtractNERBaseLineScoresFromFiles_2016(and_file_name,
                                                    or_file_name,
                                                    comb_file_name)

    def query_Notes_exapansion_scores_2016(self, query_file_path):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/Notes_AND_' + time + '_' + filename
        or_file_name = './Output/Notes_OR_' + time + '_' + filename
        comb_file_name = './Output/Notes_COMBINED_' + time + '_' + filename

        self.getQueryExapansionscore_2016(query_file_path,
                                          and_file_name,
                                          or_file_name,
                                          "Notes")
        self.ExtractNERBaseLineScoresFromFiles_2016(and_file_name,
                                                    or_file_name,
                                                    comb_file_name)
        
        
    ###################################### 2019 #################################################################
    
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

    def getScoresUsingBoolQuery_2019(self, query_file_path):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/BoolQuery_'+ time + '_' + filename

        bool_query_results = self.getScoresusingBoolQuery(query_file_path,
                                                          "2019-trec-precision-medicine-final")
        score_list = bool_query_results[0]
        query_id_list = bool_query_results[1]
        _ = SaveScore.Save(and_file_name, query_id_list, score_list)
        print("*...scores saved successfully...*")

    def getScoresUsingBoolQueryExpanison_2019(self, query_file_path):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        and_file_name = './Output/' + 'ExpandedQuery' + time + '_' + filename
        
        expanded_query_results = self.getExpandedQueryresults(query_file_path)
        query_id_list = expanded_query_results[1]
        exp_bool_query_obj = BoolQueryExpansion.GetBoolQueryExpansion(expanded_query_results[0],
                                                                      "2019-trec-precision-medicine-final")
        scores = exp_bool_query_obj.getScores()
        _ = SaveScore.Save(and_file_name, 
                           query_id_list,
                           scores)

        print("*...Exapnded scores saved successfully...*")

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

    