import RandomFloat
import math



class SaveCombineQueryExapnsion:

    def __init__(self, out_file_path, and_results_tuple, or_results_tuple, combine_results_tuple=()):
        self.and_results_tuple = and_results_tuple
        self.or_results_tuple = or_results_tuple
        self.combine_results_tuple = combine_results_tuple
        self.score_res = list()
        self.doc_res = list()
        self.out_file_path = out_file_path
        self.query_id_res = list()

    def extractandSaveQueryExapansionScore(self):
        and_query_id_results = self.and_results_tuple[0]
        and_doc_id_results = self.and_results_tuple[1]
        and_score_results = self.and_results_tuple[2]

        or_query_id_results = self.or_results_tuple[0]
        or_doc_id_results = self.or_results_tuple[1]
        or_score_results = self.or_results_tuple[2]

        combine_query_id_results = self.combine_results_tuple[0]
        combine_doc_id_results = self.combine_results_tuple[1]
        combine_score_results = self.combine_results_tuple[2]

        id_res = []
        score_res = []
        doc_res = []

        for and_query_id_list, and_doc_id_list, and_score_list, com_query_id_list, com_doc_id_list, com_score_list in zip(and_query_id_results, and_doc_id_results, and_score_results,
                                                                                                                          combine_query_id_results, combine_doc_id_results, combine_score_results):
            print(and_query_id_list[0])
            query_id_results = and_query_id_list
            doc_id_results = and_doc_id_list
            score_results = and_score_list

            copy_com_id = com_query_id_list.copy()
            copy_doc_id = com_doc_id_list.copy()
            copy_score_list = com_score_list.copy()

            for and_doc_id in and_doc_id_list:
                print(and_doc_id)
                try:
                    index = copy_doc_id.index(and_doc_id)
                    del copy_doc_id[index]
                    del copy_score_list[index]
                    del copy_com_id[index]
                except ValueError as ve:
                    print(ve)
            query_id_results.extend(copy_com_id)
            doc_id_results.extend(copy_doc_id)
            score_results.extend(copy_score_list)
            id_res.append(query_id_results)
            score_res.append(score_results)
            doc_res.append(doc_id_results)

        for and_query_id_list, and_doc_id_list, and_score_list, or_query_id_list, or_doc_id_list, or_score_list in zip(id_res, doc_res, score_res,
                                                                                                                       or_query_id_results, or_doc_id_results, or_score_results):
            query_id_results = and_query_id_list
            doc_id_results = and_doc_id_list
            score_results = and_score_list

            copy_or_id = or_query_id_list.copy()
            copy_doc_id = or_doc_id_list.copy()
            copy_or_score_list = or_score_list.copy()

            for and_doc_id in and_doc_id_list:
                try:
                    index = copy_doc_id.index(and_doc_id)
                    del copy_doc_id[index]
                    del copy_or_score_list[index]
                    del copy_or_id[index]
                except:
                    pass
            query_id_results.extend(copy_or_id)
            doc_id_results.extend(copy_doc_id)
            score_results.extend(copy_or_score_list)
            self.query_id_res.append(query_id_results)
            self.score_res.append(score_results)
            self.doc_res.append(doc_id_results)
        self.savescores()

    def extractandSaveBaseLineQueryScore(self):
        and_query_id_results = self.and_results_tuple[0]
        and_doc_id_results = self.and_results_tuple[1]
        and_score_results = self.and_results_tuple[2]

        or_query_id_results = self.or_results_tuple[0]
        or_doc_id_results = self.or_results_tuple[1]
        or_score_results = self.or_results_tuple[2]

        for and_query_id_list, and_doc_id_list, and_score_list, or_query_id_list, or_doc_id_list, or_score_list in zip(and_query_id_results, and_doc_id_results, and_score_results,
                                                                                                                          or_query_id_results, or_doc_id_results, or_score_results):
            query_id_results = and_query_id_list
            doc_id_results = and_doc_id_list
            score_results = and_score_list

            copy_or_id = or_query_id_list.copy()
            copy_doc_id = or_doc_id_list.copy()
            copy_or_score_list = or_score_list.copy()

            for and_doc_id in and_doc_id_list:
                try:
                    index = copy_doc_id.index(and_doc_id)
                    del copy_doc_id[index]
                    del copy_or_score_list[index]
                    del copy_or_id[index]
                except:
                    pass
            query_id_results.extend(copy_or_id)
            doc_id_results.extend(copy_doc_id)
            score_results.extend(copy_or_score_list)
            self.query_id_res.append(query_id_results)
            self.score_res.append(score_results)
            self.doc_res.append(doc_id_results)
        self.savescores()

    '''
        Prepare scores document
    '''

    def savescores(self):
        ran_obj = RandomFloat.GenerateRandomFloat()
        random_numbers = ran_obj.genereate1000FloatNumbers()
        for query_id_list, doc_id_list, score_list in zip(self.query_id_res, self.doc_res, self.score_res):
            for query_id, doc_id, score, random_number in zip(query_id_list, doc_id_list, score_list, random_numbers):
                if score > 0.0:
                    with open(self.out_file_path, "a") as outFile:
                        outFile.write(str(query_id) + "\t" + str(doc_id).upper() + '\t' + str(score) + '\t' + str(
                            random_number) + "\n")
