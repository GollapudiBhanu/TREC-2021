import pandas as pd

'''
This file is used to caluculate the number of documnets in each query id.

Filepath: inputfilepath, in which documnet we need to calculate the count.
Outpath: where we need to save the count(file name)
'''
class NumberOfDocumnets:

    def __init__(self, file_path, outpath):
        self.filepath = file_path
        self.outpath = outpath
        self.number_documnets()

    def number_documnets(self):
        df = pd.read_csv(self.filepath, sep = '\t', header = None)
        if df.shape[1] == 4:
            df.columns = ['query_id', 'Document_id', 'Score', 'pseudoscore']
        elif df.shape[1] == 3:
            df.columns = ['query_id', 'Document_id', 'Score']
        df['group_id'] = df.groupby(['query_id']).grouper.group_info[0]
        df = df.groupby(["group_id"]).agg(lambda x: x.tolist())
        query_id_list = df['query_id'].tolist()
        document_list = df['Document_id'].tolist()
        doc_len_list = []
        quid = []
        for qid, documnet in zip(query_id_list, document_list):
            doc_len_list.append(len(documnet))
            quid.append(qid[0])

        data = {'query_ID': quid,
                'Documnet_Data': doc_len_list}
        df = pd.DataFrame(data)
        df.to_csv(self.outpath, sep='\t',index=False)


#obj1 = NumberOfDocumnets('/home/junhua/trec/Trec2021/Output/2021Output/Run1/KeywordExtr_Query2021_unigram_12_1.csv',
#                         '/home/junhua/trec/Trec2021/Output/2021Output/Run1/KeywordExtr_Query2021_unigram_12_1_length.csv')
#obj2 = NumberOfDocumnets('/home/junhua/trec/Trec2021/Output/2021Output/Run2/RAW_EXP_RAW_EXP_Test-n-n-2-1.csv',
#                         '/home/junhua/trec/Trec2021/Output/2021Output/Run2/RAW_EXP_RAW_EXP_Test-n-n-2-1_length.csv')
#obj3 = NumberOfDocumnets('/home/junhua/trec/Trec2021/Output/2021Output/Run3/RAW_EXP_RAW_EXP-Final_combined-n-n-2-1.csv',
#                         '/home/junhua/trec/Trec2021/Output/2021Output/Run3/RAW_EXP_RAW_EXP-Final_combined-n-n-2-1_length.csv')

