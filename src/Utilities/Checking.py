import pandas as pd

'''
This file is used to find the compare two lists i.e in the combinational list, the upper part must be AND results need to present.
'''

class Check:
    '''
       Input:
        input_file: Inputfile(combinational file)
        out_put_file: Output file (AND result file)
    '''
    def __init__(self, input_file, out_put_file):
        self.input_file = input_file
        self.out_put_file = out_put_file

    '''
        input:
            input it takes the file path as a input
        Description:
            from the file, it retrievs the list of Document_id's.
        Output:
            It returns the list of Documnet_id's
    '''
    def input(self, input):
        df = pd.read_csv(input, delimiter='\t', header=None)
        if df.shape[1] == 5:
            df.columns = ["query_id", "doc_id", "BM25score","score", "Text"]
        elif df.shape[1] == 4:
            df.columns = ["query_id", "doc_id", "BM25score", "Text"]
        df = df.dropna()
        df = df.drop_duplicates()
        df["group_id"] = df.groupby(["query_id"]).grouper.group_info[0]
        df = df.groupby(["group_id"]).agg(lambda x: x.tolist())
        doc_id_list = df['doc_id'].tolist()
        return doc_id_list

    '''
        it compares the inputlist(combiantional results) with outputlist(and results)
    '''
    def extract_out(self):
        andres = self.input(self.out_put_file)
        comres = self.input(self.input_file)

        for inputlist, outputlist in zip(andres, comres):
            out = outputlist[0: len(inputlist)]
            if inputlist == out:
                print("I am equal")
            else:
                print("################################")
                print("I am not equal")

