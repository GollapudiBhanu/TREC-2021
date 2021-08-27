import os, glob
import pandas as pd
import os.path
from os import path

'''
This file is used to combine the individual csv files in to single csv file.
'''
class Merged:

    def __init__(self, source_file_path= ""):
        self.source_file_path = source_file_path


    def single(self):
        file = '/home/junhua/trec/Trec2021/Output/2021Output/Rawquery/New/RAWQUERY_N-N-2_1000_1.csv'
        df = pd.read_csv(file, sep= '\t', header=None)
        print(df)

    def merge(self):
        all_filenames = []

        for i in range(0, 76):
            try:
                file = os.path.join(self.source_file_path,
                                    "Final_Expansion_combinational_score_2016_query_exp_" + str(i + 1) + ".csv")
                if path.exists(file):
                    all_filenames.append(file)
            except:
                continue

        combined_csv = pd.concat([pd.read_csv(f, delimiter = '\t', header=None) for f in all_filenames])
        combined_csv.to_csv("/home/junhua/Downloads/merged.csv", index=False, encoding='utf-8-sig')

#obj = Merged('/home/junhua/Downloads/New_strategy')
#obj.merge()