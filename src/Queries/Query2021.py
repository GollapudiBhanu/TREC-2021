import pandas as pd


class ExtractQueries:
    '''
        input:
            query_file_path: input query file path
    '''
    def __init__(self, query_file_path):
        self.query_file_path = query_file_path

    '''
        input: 
            column_names_list: column names
        Description:
            It prepares the list of queires,based on the column names
        output: 
            it returns the tuple, with a list of all queries.  
    '''
    def getNERQueriesList(self, column_names_list):
        df = pd.read_csv(self.query_file_path)
        column_list = []
        for name in column_names_list:
            column_list.append(name)
        df.columns = column_list
        final_query_list = []
        df = df.dropna()
        for name in column_list:
            out_list = df[name].tolist()
            final_query_list.append(out_list)
        return tuple(final_query_list)
