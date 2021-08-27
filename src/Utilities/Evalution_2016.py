import pandas as pd
import numpy as np

'''
This file is used to find the same document text for the id's.
input: source_file: input file, in which document you need to find the duplicates concatstrings.
'''
class Evaluation_2016:
    def __init__(self, source_file, type=""):
        self.source_file = source_file
        self.findElements(type)

    def findElements(self, type = " "):
        df = pd.read_csv(self.source_file, sep='\t')
        if type == "combined":
            df.columns = ["query_id", "doc_no","score","float-score", "concat_str"]
        else:
            df.columns = ["query_id", "doc_no", "score", "concat_str"]
        df1 = df.groupby(["query_id"]).agg(lambda x: x.tolist())
        doc_list = df1["doc_no"].tolist()
        concat_str = df1["concat_str"].tolist()

        for doc, str in zip(doc_list, concat_str):
            dupes = set([x for x in str if str.count(x) > 1])
            if len(dupes) > 0:
                dupe_value = list(dupes)[0]
                values = np.array(str)
                li = np.where(values == dupe_value)
                print(li)

#obj = Evaluation_2016("/home/junhua/trec/Trec2021/Output/Bhanu_New_Summary_Combined_NER-BERN_Query2016_gene-disease-drug_2016.csv", "combined")
#obj = Evaluation_2016("/home/junhua/trec/Trec2021/Output/Bhanu_New_Summary_OR_NER-BERN_Query2016_gene-disease-drug_2016.csv")


