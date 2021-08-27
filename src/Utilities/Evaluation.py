import pandas as pd

'''
This file is used to find the duplicate id's with in queryid's

input: source_file: pass the query file, where we need to find the duplicates of the documnet id's
'''
class GetDuplicates:

    def __init__(self, source_file):
        self.source_file = source_file
        self.findDuplicates()

    ''' 
        Description: Find the duplicates in Doc_id list.
    '''
    def findDuplicates(self):
        df = pd.read_csv(self.source_file, delimiter='\t')
        if df.shape[1] == 5:
            df.columns = ['topicID', 'docID', 'score_drop', 'score', 'doc']
            df = df.drop(columns=['score_drop'])
        else:
            df.columns = ['topicID', 'docID', 'score', 'pse']

        df["group_id"] = df.groupby(["topicID"]).grouper.group_info[0]
        df = df.groupby(["group_id"]).agg(lambda x: x.tolist())
        doc_id_list = df['docID'].tolist()

        for index, doc_list in enumerate(doc_id_list):
            len1 = len(doc_list)
            set_len = len(list(set(doc_list)))

            if len1 == set_len:
                print("NO duplicates")
            else:
                print(index)
                print("dupicates")




#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease-drug_2016.csv')
#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016.csv')
#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/New_Summary_Combined_NER_BoolQuery_scores_2016.csv')


#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_gene-disease_2016.csv')
#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_gene-disease_2016.csv')
#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/New_Summary_Combined_NER-BERN_Query2016_gene-disease_2016.csv')


#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/New_Summary_AND_NER-BERN_Query2016_all.csv')
#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/New_Summary_OR_NER-BERN_Query2016_all.csv')
#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/New_Summary_Combined_New_Summary_OR_NER-BERN_Query2016_all.csv')


#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/Summary_AND_5w-1gram_2016.csv')
#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/Summary_OR_5w-1gram_2016.csv')
#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/Summary_Combined_5w-1gram_2016.csv')

#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/2016QueryOutput/2016Reranking/Bhanu-All_merge.csv')
'''
obj1 = GetDuplicates('/home/junhua/trec/Trec2021/Output/2021Output/Run1/raw_meta_terms_2021_disease-symptom_B-reformated_1-n-2-1.csv')
print("33333333333333333333")
obj2 = GetDuplicates('/home/junhua/trec/Trec2021/Output/2021Output/Run1/Exp_meta_terms_2021_disease-symptom_B-reformated_1-n-n-2.csv')
print("444444444444444444")
obj3 = GetDuplicates('/home/junhua/trec/Trec2021/Output/2021Output/Run1/Exp_meta_terms_2021_disease-symptom_B-reformated_1-n-2-1.csv')
'''


