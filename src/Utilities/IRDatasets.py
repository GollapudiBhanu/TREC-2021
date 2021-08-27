import ir_datasets


class DataSet:
    def __init__(self):
        pass

    def reteriveDoc(self):
        dataset = ir_datasets.load('Bhanu/UNT:TREC2016')
        print(dataset)

obj = DataSet()
obj.reteriveDoc()
