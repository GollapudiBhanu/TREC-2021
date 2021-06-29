class ListIntialSetUp:

    def __init__(self, and_results_tuple, or_results_tuple, combine_results_tuple=()):
        self.and_results_tuple = and_results_tuple
        self.or_results_tuple = or_results_tuple
        self.combine_results_tuple = combine_results_tuple

    def arrangeQueryExpansionLength(self):
        and_query_id_list = self.and_results_tuple[0]
        and_doc_id_list = self.and_results_tuple[1]
        and_score_list = self.and_results_tuple[2]
        and_len = len(and_query_id_list)

        or_query_id_list = self.or_results_tuple[0]
        or_doc_id_list = self.or_results_tuple[1]
        or_score_list = self.or_results_tuple[2]
        or_len = len(or_query_id_list)

        combine_query_id_list = self.combine_results_tuple[0]
        combine_doc_id_list = self.combine_results_tuple[1]
        combine_score_list = self.combine_results_tuple[2]
        com_len = len(combine_query_id_list)

        if and_len > com_len:
            differlist= self.prepareAndWithCombine(and_query_id_list, combine_query_id_list)
            for i in differlist:
                combine_query_id_list.insert(i - 1, and_query_id_list[i - 1])
                combine_doc_id_list.insert(i - 1, and_doc_id_list[i - 1])
                combine_score_list.insert(i - 1, and_score_list[i - 1])
        if and_len < com_len:
            differlist= self.prepareAndWithCombine(combine_query_id_list,and_query_id_list)
            for i in differlist:
                and_query_id_list.insert(i - 1, combine_query_id_list[i - 1])
                and_doc_id_list.insert(i - 1, combine_doc_id_list[i - 1])
                and_score_list.insert(i - 1, combine_score_list[i - 1])
        if and_len > or_len:
            differlist = self.prepareAndWithCombine(and_query_id_list, or_query_id_list)
            for i in differlist:
                or_query_id_list.insert(i - 1, and_query_id_list[i - 1])
                or_doc_id_list.insert(i - 1, and_doc_id_list[i - 1])
                or_score_list.insert(i - 1, and_score_list[i - 1])
        if and_len < or_len:
            differlist = self.prepareAndWithCombine(or_query_id_list, and_query_id_list)
            for i in differlist:
                and_query_id_list.insert(i - 1, or_query_id_list[i - 1])
                and_doc_id_list.insert(i - 1, or_doc_id_list[i - 1])
                and_score_list.insert(i - 1, or_score_list[i - 1])

        return self.and_results_tuple, self.or_results_tuple, self.combine_results_tuple

    def arrangeBaseLineQueryLength(self):
        and_query_id_list = self.and_results_tuple[0]
        and_doc_id_list = self.and_results_tuple[1]
        and_score_list = self.and_results_tuple[2]
        and_len = len(and_query_id_list)

        or_query_id_list = self.or_results_tuple[0]
        or_doc_id_list = self.or_results_tuple[1]
        or_score_list = self.or_results_tuple[2]
        or_len = len(or_query_id_list)

        if and_len > or_len:
            differlist = self.prepareAndWithCombine(and_query_id_list, or_query_id_list)
            index_list = self.findIndex(differlist, or_query_id_list)
            for index in index_list:
                or_query_id_list.insert(index, and_query_id_list[index])
                or_doc_id_list.insert(index, and_doc_id_list[index])
                or_score_list.insert(index, and_score_list[index])
        if and_len < or_len:
            differlist = self.prepareAndWithCombine(or_query_id_list, and_query_id_list)
            index_list = self.findIndex(differlist, or_query_id_list)
            for index in index_list:
                and_query_id_list.insert(index, or_query_id_list[index])
                and_doc_id_list.insert(index, or_doc_id_list[index])
                and_score_list.insert(index, or_score_list[index])
        return self.and_results_tuple, self.or_results_tuple

    def prepareAndWithCombine(self, max_query_id_list, min_query_id_list):
        max_id_list = []
        min_id_list = []
        for and_query in max_query_id_list:
            max_id_list.append(and_query[0])
        for com_query in min_query_id_list:
            min_id_list.append(com_query[0])

        differ_list = [x for x in max_id_list if x not in min_id_list]
        return differ_list

    def findIndex(self, differList, input_list):
        out_list = []
        for element in differList:
            for index, or_list in enumerate(input_list):
                try:
                    out_index = or_list.index(element)
                    out_list.append(index)
                except:
                    continue
        return out_list
