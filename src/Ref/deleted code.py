'''
        Here I need to prepare the Query in the form of
        a1, a2, a3
        b1, b2, b3
        then the resultant is
        x = (a1 and b1) or (a1 and b2) or (a1 and b3)
        y = (a2 and b1) or (a2 and b2) or (a2 and b3)
        z = (a3 and b1) or (a3 and b2) or (a3 and b3)

        res = x or y or z
    '''
    def prepareExpansionQuery(self, type):
        output_list = []
        for input in self.exp_query_list:
            resu = '#'
            for querystr in input:
                output_str = ""
                for query in querystr.split(','):
                    if query is " ":
                        continue
                    res_query = self.preprocessQuery(query)
                    if output_str == "":
                        output_str = res_query
                    else:
                        output_str = output_str + "," + res_query
                if resu == "#":
                    resu = output_str
                else:
                    resu = resu + "#"+output_str
            output_list.append(resu)
        self.prepareQuery(output_list, type)


'''
       input: 
           expquery: Query term
       Description:
           It performs, basic preprocessing for the query 
   '''


def preprocessQuery(self, query):
    output = query.lstrip()
    output = output.rstrip()
    output = self.lowerCase(output)
    output = self.removePunctuation(output)
    output = self.stemmingwithlemmatization(output)
    return output


def prepareRawQuery(self, type):
    raw_query_list = []
    for sum_query_list in self.query_list:
        sum_query = None
        for query in sum_query_list:
            out = self.preprocessQuery(query)
            out = '(' + out + ')'
            if sum_query is None:
                sum_query = out
            else:
                sum_query = sum_query + type + out
        raw_query_list.append(sum_query)
    return raw_query_list
    def prepareQuery(self, out_list, type):
        for querystring in out_list:
            out_list = []
            query_list = querystring.split('#')
            for query in query_list:
                qu = query.split(',')
                out_list.append(qu)
            self.prepareCombinedQuery(out_list, type)



    def prepareCombinedExpansionQuery(self, query_type):
        self.prepareExpansionQuery(query_type)
        raw_query_list = self.prepareRawQuery(query_type)
        final_query_list = []
        for rawQuery, exp_query in zip(raw_query_list, self.final_query_expan_list):
            final_query = rawQuery + ' OR ' + exp_query
            final_query_list.append(final_query)
        return final_query_list

    def prepareCombinedQuery(self, out_list, type):
        com_query = []
        i = 0
        j = 1
        while(j <= len(out_list) - 1):
            input = out_list[i]
            output = out_list[j]
            i += 1
            j += 1
            for inputword in input:
                for outputword in output:
                    output_query = '(' + '(' + inputword + ')' + type + '('+ outputword + ')' + ')'
                    com_query.append(output_query)
        if len(com_query) == 0:
            com_query = out_list[0]
        res_query = " OR ".join(com_query)
        self.final_query_expan_list.append(res_query)

    def getQueryExpansionCombination(self, out_file_path, index):
        current_query_list = [self.query_list[index]]
        for query_list in current_query_list:
            finalQuerylist = []
            finallist = []
            process_list = []
            for query in query_list:
                query = self.processQuery(query)
                process_list.append(query)
            rangeLength = len(process_list)
            if rangeLength >= 6:
                rangeLength = 6
            for L in range(1, rangeLength + 1):
                outlist = []
                for subset in itertools.combinations(process_list, L):
                    outlist.append(subset)
                finallist.append(outlist)
            for flist in finallist:
                outlist = []
                for fli in flist:
                    sa = list(fli)
                    sa = self.joinQuery(sa)
                    out = " AND ".join(sa)
                    out = '(' + out + ')'
                    outlist.append(out)
                finalQuerylist.append(outlist)
            first_3_queries = []
            last_queres = []
            if len(finalQuerylist) <= 3:
                first_3_queries = finalQuerylist[:1]
                last_queres = finalQuerylist[1:len(finalQuerylist)]
            else:
                first_3_queries = finalQuerylist[:2]
                last_queres = finalQuerylist[2:len(finalQuerylist)]
            out_put_query_list = []
            for s in first_3_queries:
                out = " OR ".join(list(s))
                out_put_query_list.append(out)
            combinedlist = out_put_query_list + last_queres
            self.final_query_expan_list.append(out_put_query_list[::-1])
            print("###############")
            #self.final_query_expan_list.append(out_put_query_list[::-1])
        self.getExpansionScores()
        self.checkDuplicates()
        self.saveScore(out_file_path, index)

    '''
            Input: 
                final_query: Query to search in Elastic search.
            Description:
                It search the 'concat_string' term with the provided final_query, in the given search index.
        '''

    def retrieveScores_2021(self, final_query):
        doc_id_list = []
        score_list = []
        query_body = {
            'query': {
                'query_string': {
                    'default_field': "concat_string",
                    'query': final_query
                }
            }
        }
        try:
            query_result = self.es.search(index=self.search_index, body=query_body, size=2000)
            doc_list = []
            score = []
            for res in query_result['hits']['hits']:
                doc_list.append(self.__prepareDocId(res['_source']['url']))
                score.append(res['_score'])
            doc_id_list.append(doc_list)
            score_list.append(score)
        except:
            pass
        return doc_id_list, score_list

    def removeDuplicates(self, out_file_path, indexnumber):
        final_list = []
        for combine_doc_list in self.final_documnet_id_list:
            for index, combinational_list in enumerate(combine_doc_list):
                query_doc_list = list(flatten(combinational_list))
                final_list.append(query_doc_list)
            final_doc_list = list(flatten(final_list))
            data = {'Doc_id': final_doc_list}
            df = pd.DataFrame(data)
            df.drop_duplicates(keep='first', inplace=True)
            out = df['Doc_id'].values.tolist()
            #out1 = df['score'].values.tolist()
            #self.expansion_score_list.append(out1)
            self.expansion_doc_id_list.append(out)
        self.saveScore(out_file_path, indexnumber)

    '''

    '''

    def flatten(self, list_of_lists):
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return self.flatten(list_of_lists[0]) + self.flatten(list_of_lists[1:])
        return list_of_lists[:1] + self.flatten(list_of_lists[1:])


    def getExpansionScores_2016(self, query_type, out_file_path):
        self.getQueryExpansionCombination(out_file_path, query_type)




