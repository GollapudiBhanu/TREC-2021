import pandas as pd


class ExtractQueries:
    def __init__(self, query_file_path):
        self.query_file_path = query_file_path

    def getNERQueriesList(self, column_names_list):
        df = pd.read_csv(self.query_file_path)
        column_list = []
        for name in column_names_list:
            column_list.append(name)
        df.columns = column_list
        final_query_list = []
        df = df.dropna()
        print(df.head(100))
        for name in column_list:
            out_list = df[name].tolist()
            final_query_list.append(out_list)
        return tuple(final_query_list)
