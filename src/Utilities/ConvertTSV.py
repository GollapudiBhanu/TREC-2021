import csv
import pandas as pd
import os

'''
This is file is used to convert the given file in to Tab seaparted file.

input: input file path(which file you need to convert)
output: output file path(where you need to save the tab separated file)

'''
class TSV:

    def __init__(self, query_file_path, outfilepath):
        self.query_file_path = query_file_path
        self.outfilepath =outfilepath

    def read_file(self):
        df = pd.read_csv(self.query_file_path, sep=',')
        print(len(df.columns))
        return df

    def extract_text(self):
        df = self.read_file()
        df.columns = ['query_id',
                      'summary',
                      'summary_keyword_list',
                      'summary_keyword_expansion_list']
        df['combined'] = df[['summary_keyword_list', 'summary_keyword_expansion_list']].agg(','.join, axis=1)
        combined_data = df['combined'].values.tolist()
        query_id = df["query_id"].tolist()
        return combined_data, query_id

    def convert_to_tsv(self):
        results = self.extract_text()
        text_list = results[0]
        query_id_list = results[1]
        data = {"Query_ID": query_id_list,
                "Query_Text": text_list}
        df = pd.DataFrame(data)
        df.to_csv(self.outfilepath, sep = '\t')

#obj = TSV('/home/junhua/trec/Trec2021/Data/2016_Quries/Manual_KeywordExtr_Query2016_aug3_B-reformated.csv',
#          '/home/junhua/trec/Trec2021/Data/2016_Quries/Manual_KeywordExtr_Query2016_aug3_B-reformated.tsv')
#obj.convert_to_tsv()


