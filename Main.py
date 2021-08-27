from Preprocessing import BasicPreprocessing_2021, BasicPreprocessing, BasicPreprocessing_2016
from Indexing import Indexing2016, Indexing2019, Indexing2021
from QueryExpansion import ExapnsionScore_2016, QueryExpansion_2016
from Retrieval import SaveCombineQueryExapansionScore
from Utilities import ExtractScoresFromFile, IntialSetup, ExtractDocument

from datetime import datetime
import os


class Main:

    def get_dateTime(self):
        now = datetime.today().isoformat()
        return str(now)

    def get_file_name(self, filepath):
        filename = os.path.basename(filepath)
        return filename

    ######################### 2016 ####################################

    '''
        Input: 
            input_folder_path: input folder path
            dest_folder_path: output folder path, where you want to save the output files.
        Description:
            It performs the Basic preprocessing operation for the provided input folder and save the preprocessed files in the destination path.
    '''
    def basicpreprocessing2016(self, input_folder_path, dest_folder_path):
        preprocessing_obj = BasicPreprocessing_2016.Preprocessing_2016(input_folder_path, dest_folder_path)
        preprocessing_obj.getRootJsonObject()
        print("Basic Preprocessing is done successfully.")

    '''
        Input: 
            input_path: preproceed files path.
            search_index: Elastic search index,
    '''
    def indexing_2016(self, input_path, search_index):#'./Data/TREC_2016_OutputData'
        _ = Indexing2016.Indexing_2016(input_path, search_index)
        print("Indexing is done")



    ################################ 2019 ####################################

    '''
        Input: 
            input_folder_path: input folder path
            dest_folder_path: output folder path, where you want to save the output files.
        Description:
            It performs the Basic preprocessing operation for the provided input folder and save the preprocessed files in the destination path.
    '''
    def basicpreprocessing_2019(self, input_folder_path, dest_folder_path):
        basic_preprocessing = BasicPreprocessing.Preprocessing(input_folder_path, dest_folder_path)
        basic_preprocessing.getRootJsonObject()
        print("Basic preprocessing is Done")

    '''
        Input: 
            input_path: preproceed files path.
            search_index: Elastic search index,
    '''
    def indexing_2019(self, input_path, index_name):
        _ = Indexing2019.Indexing(input_path, index_name)
        print("Indexing if 2019 is Done.")


    ################################ 2021 ##########################################

    '''
        Input: 
            input_folder_path: input folder path
            dest_folder_path: output folder path, where you want to save the output files.
        Description:
            It performs the Basic preprocessing operation for the provided input folder and save the preprocessed files in the destination path.
    '''
    def basicpreprocessing_2021(self, source_file, dest_file):
        basic_preprocessing = BasicPreprocessing_2021.Preprocessing_2021(source_file, dest_file)
        basic_preprocessing.getRootJsonObject()
        print("************** Preprocessing of 2021 done successfully *******************")

    '''
        Input: 
            input_path: preproceed files path.
            search_index: Elastic search index,
    '''
    def indexing_2021(self, input_path, index_name):
        _ = Indexing2021.Indexing_2021(input_path, index_name)
        print("************** Indexing 2021 done successfully *******************")


    #####################################################################################################

    '''
        Input: 
            query_file_path: Query file path.
        Description:
            From the give file path, it retrievs the summary_tuple, description_tuple and note_tuple.
    '''
    def getExapnsionQueries(self, query_file_path):
        obj = QueryExpansion_2016.ExapandedQuery_2016(query_file_path,
                                                      ['queryID', 'Main_text', 'raw_list', 'Expansion_list'])
        results = obj.getExpansionQuery_2021()
        summary_tuple = results[0]
        description_tuple = results[1]
        note_tuple = results[2]
        return summary_tuple, description_tuple, note_tuple

    '''
        Input: 
            query_file: Query file path.
            out_file: output file path
            type: which type your retrieving
            search_index: Elastic search index

        Description:
            From the give query_file path, it retrievs the summary_tuple, description_tuple and note_tuple and get the exapnsion scores and save that scores in to the out_file.
    '''
    def getQueryExapansionscore(self, query_file, out_file, type, search_index):
        results = self.getExapnsionQueries(query_file)
        query_expansion_list = []
        id_list = []
        if type == "summary":
            tuple = results[0]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
        elif type == "description":
            tuple = results[1]
            query_expansion_list = tuple[0]
            id_list = tuple[1]
        elif type == "Note":
            tuple = results[2]
            query_expansion_list = tuple[0]
            id_list = tuple[1]

        score_obj = ExapnsionScore_2016.GetQueryExapnsionScore_2016(query_expansion_list,
                                                                    id_list,
                                                                    search_index)

        for index in range(0, len(id_list)):
            score_obj.getandsavescores(index, out_file)

    '''
        input: 
            query_file_path: Input query file path
            search_index: Elastic search index
            type: type of query(ex: summary, description, Note) 
    '''
    def query_exapansion_scores(self, query_file_path, search_index, type = "summary"):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        out_file_name = './Output/Summary_Expansion' + time + '_' + filename

        self.getQueryExapansionscore(query_file_path,out_file_name, type, search_index)

    '''
        Input: 
            query_file: Query file path.
            out_file: output file path
            type: which type your retrieving
             search_index: Elastic search index

        Description:
            From the give query_file path, it retrievs the summary_tuple, description_tuple and note_tuple and get the exapnsion scores and save that scores in to the out_file.
    '''
    def getRawQueryscore(self, query_file, out_file, type, search_index):
        results = self.getExapnsionQueries(query_file)
        query_list = []
        id_list = []
        if type == "summary":
            tuple = results[0]
            id_list = tuple[1]
            query_list = tuple[2]
        elif type == "description":
            tuple = results[1]
            id_list = tuple[1]
            query_list = tuple[2]
        elif type == "Note":
            tuple = results[2]
            id_list = tuple[1]
            query_list = tuple[2]

        score_obj = ExapnsionScore_2016.GetQueryExapnsionScore_2016(query_list, id_list,
                                                                    search_index)

        for index in range(0, len(id_list)):
            score_obj.getandsavescores(index, out_file)

    '''
        input: 
            query_file_path: Input query file path
            search_index: Elastic search index
            type: type of query(ex: summary, description, Note) 
    '''
    def raw_query_scores(self, query_file_path, search_index, type = "summary"):
        time = self.get_dateTime()
        filename = self.get_file_name(query_file_path)
        out_file_name = './Output/Summary_Raw' + time + '_' + filename

        self.getQueryExapansionscore(query_file_path,
                                     out_file_name,
                                     type, search_index)

    ########################################################################################################

    '''
        Input: 
            first_file: The file where we need to store the scores on first position
            second_file:The file where we need to store the scores on second position
        Description:
            From the individual files, it extract the scores, remove duplicates. 
        
        Output:
            results: tuple(contaimns and results and or results)
    '''
    def extarctNERBaseLineQueryListfromfile(self, first_file, second_file):
        obj = ExtractScoresFromFile.ExtractList(first_file)
        obj1 = ExtractScoresFromFile.ExtractList(second_file)

        extract_and_results = obj.extractScore()
        extract_or_results = obj1.extractScore()

        obj = IntialSetup.ListIntialSetUp(extract_and_results,
                                          extract_or_results)
        results = obj.arrangeBaseLineQueryLength_combinational()

        return results

    '''
        Input: 
            first_file: The file where we need to extract the scores and save it on first position.
            second_file:The file where we need to extract the scores and save it on second position.
            result_file: The file where we need to 
        
        Description:
            After intail setup, we need to save the results in to outfile.
    '''
    def extractNERBaseLineScoresFromFiles(self, first_file, second_file, result_file):
        results = self.extarctNERBaseLineQueryListfromfile(first_file, second_file)
        extract_and_results = results[0]
        extract_or_results = results[1]

        save_obj = SaveCombineQueryExapansionScore.SaveCombineQueryExapnsion(result_file,
                                                                             extract_and_results,
                                                                             extract_or_results)
        save_obj.extractandSaveBaseLineQueryScoreWithoutDocument()
        #save_obj.extractandSaveBaseLineQueryScore()


    '''
        input:
            index_name: Elastic search index name
            query_file_path: query file name
            raw_out_score_file_path:Raw query results save file path.
            exp_out_score_file_path:Exp Query results save file path.
            comb_out_score_file_path: Combine results save file path. 
    '''

    def saveScores(self, index_name, query_file_path, raw_out_score_file_path, exp_out_score_file_path, comb_out_score_file_path):
        self.getRawQueryscore(query_file_path, raw_out_score_file_path, 'summary', index_name)
        self.getQueryExapansionscore(query_file_path, exp_out_score_file_path, 'summary', index_name)
        self.extractNERBaseLineScoresFromFiles(raw_out_score_file_path, exp_out_score_file_path,
                                               comb_out_score_file_path)

    '''
        input:
            input_folder_path: Input folder path
            out_folder_path: pre-processed output folder path.
            index_name: Elastic search index name
            query_file_path: query file name(.csv file)
            raw_out_score_file_path:Raw query results save file path(.csv file)
            exp_out_score_file_path:Exp Query results save file path(.csv file)
            comb_out_score_file_path: Combine results save file path(.csv file)
    '''
    def perform_TREC_2016(self, input_folder_path, out_folder_path, index_name, query_file_path, raw_out_score_file_path, exp_out_score_file_path, comb_out_score_file_path):
        self.basicpreprocessing2016(input_folder_path, out_folder_path)
        self.indexing_2016(out_folder_path, index_name)
        self.saveScores(index_name, query_file_path, raw_out_score_file_path, exp_out_score_file_path, comb_out_score_file_path)

    '''
        input:
            input_folder_path: Input folder path
            out_folder_path: pre-processed output folder path.
            index_name: Elastic search index name
            query_file_path: query file name(.csv file)
            raw_out_score_file_path:Raw query results save file path(.csv file)
            exp_out_score_file_path:Exp Query results save file path(.csv file)
            comb_out_score_file_path: Combine results save file path(.csv file)
    '''
    def perform_TREC_2019(self, input_folder_path, out_folder_path, index_name, query_file_path,
                          raw_out_score_file_path, exp_out_score_file_path, comb_out_score_file_path):
        self.basicpreprocessing_2019(input_folder_path, out_folder_path)
        self.indexing_2019(out_folder_path, index_name)
        self.saveScores(index_name, query_file_path, raw_out_score_file_path, exp_out_score_file_path,
                        comb_out_score_file_path)

    '''
        input:
            input_folder_path: Input folder path
            out_folder_path: pre-processed output folder path.
            index_name: Elastic search index name
            query_file_path: query file name(.csv file)
            raw_out_score_file_path:Raw query results save file path(.csv file)
            exp_out_score_file_path:Exp Query results save file path(.csv file)
            comb_out_score_file_path: Combine results save file path(.csv file)
    '''

    def perform_TREC_2021(self, input_folder_path, out_folder_path, index_name, query_file_path,
                          raw_out_score_file_path, exp_out_score_file_path, comb_out_score_file_path):
        self.basicpreprocessing_2021(input_folder_path, out_folder_path)
        self.indexing_2021(out_folder_path, index_name)
        self.saveScores(index_name, query_file_path, raw_out_score_file_path, exp_out_score_file_path,
                        comb_out_score_file_path)

    '''
        Input:
            input_file_path: input file path(.csv)
            out_file_path: output file path(.csv)
            search_index: Elastic search index.
    '''
    def extractDocument(self, input_file_path, out_file_path, search_index):
        obj = ExtractDocument.ExrtractText(input_file_path,out_file_path)
        obj.getQueryExpansionText_1(search_index)

    def TREC(self):
        year_input = int(input("Which year you want to process queries \n 1.2016 2. 2019 3. 2021 \n"))
        input_folder_path = input("Enter Raw input data folder path:\n")
        out_folder_path = input("Enter where you want to save the pre-processed folder path:\n")
        index_name = input("Enter Elastic search index name:\n")
        query_file_path = input("Enter Query file path:\n")
        raw_out_score_file_path = input("Enter the path for Where you want to save the RAW query results:\n")
        exp_out_score_file_path = input("Enter the path for Where you want to save the Exapnded query results:\n")
        comb_out_score_file_path = input("Enter the path where you want to save the Combined results(RAW+EXP):\n")

        if year_input == 1:
            self.perform_TREC_2016(input_folder_path, out_folder_path, index_name, query_file_path, raw_out_score_file_path, exp_out_score_file_path, comb_out_score_file_path)
        elif year_input == 2:
            self.perform_TREC_2019(input_folder_path, out_folder_path, index_name, query_file_path, raw_out_score_file_path, exp_out_score_file_path, comb_out_score_file_path)
        elif year_input == 3:
            self.perform_TREC_2021(input_folder_path, out_folder_path, index_name, query_file_path, raw_out_score_file_path, exp_out_score_file_path, comb_out_score_file_path)

if __name__ == '__main__':
    main_obj = Main()
    main_obj.TREC()

























