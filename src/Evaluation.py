import pandas as pd

class GetDuplicates:

    def __init__(self, source_file):
        self.source_file = source_file
        self.findDuplicates()

    ''' 
        Description: Find the duplicates in Doc_id list.
    '''
    def findDuplicates(self):
        df = pd.read_csv(self.source_file, delimiter='\t')
        if df.shape[1] == 4:
            df.columns = ['topicID', 'docID', 'score_drop', 'score']
            df = df.drop(columns=['score_drop'])
        else:
            df.columns = ['topicID', 'docID', 'score']
        if df[df.duplicated()].shape[0] == 1:
            print('error', df[df.duplicated()].shape)
        else:
            print("No duplicates")


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

#obj = GetDuplicates('/home/junhua/trec/Trec2021/Output/Combined_drug_with5w-1g_2016.csv')


