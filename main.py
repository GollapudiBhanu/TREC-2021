import BasicPreprocessing
import Indexing2019
import QueryExpansionList
import Corpus
import Bm25_scoring
import Queries
import Nxml_to_Xml
import Basicpreprocessing_2016

class Main:
    """
        Basic Preprocessing
    """

    def basicpreprocessing(self):
        basic_preprocessing = BasicPreprocessing.Preprocessing('./Data/TREC_2019_input_data', './Data/TREC_2019_Output_data')
        print("Corpus preparation is Done")
        basic_preprocessing.getRootJsonObject()
        print("Basic Preprocessing is done successfully.")

    '''
        Indexing
    '''

    def indexing(self):
        _ = Indexing2019.Indexing('./Data/TREC_2019_Output_data')
        print("Indexing is Done")

    '''
     Corpus preparation
    '''

    def preparecorpus(self):
        corpus_obj = Corpus.creatCorpus()
        corpus = corpus_obj.prepareCorpus()
        document_id_list = corpus_obj.getdocumentidlist()
        return corpus, document_id_list

    '''
        BaseLineScoring0
    '''

    def baseLineScoring(self):
        corpus = self.preparecorpus()[0]
        document_id_list = self.preparecorpus()[1]

        queries = self.baselinequery()

        bm25 = Bm25_scoring.BM25(corpus, delimiter=' ')
        bm25.getBM25Score(queries, document_id_list)
        # tfidf = bm25.TFIDF()

    '''
        BaseLineQuery
    '''

    def baselinequery(self):
        query = Queries.getQuery()
        queries = query.getQueryList()
        return queries

    '''
        Expanded Query List
    '''

    def expandedQuery(self):
        expanded_query = QueryExpansionList.ExapndedQuery('./Data/Expansiontopics2019.csv')
        expanded_query_list = expanded_query.getGroupedData()
        expanded_query_id_list = expanded_query.removeDuplicates()
        return expanded_query_list, expanded_query_id_list

    '''
        Query Expansion
    '''

    def queryexapnsionscoring(self):
        print("Query expansion")
        corpus = self.preparecorpus()[0]
        document_id_list = self.preparecorpus()[1]

        queries = self.expandedQuery()[0]
        query_id_list = self.expandedQuery()[1]

        bm25 = Bm25_scoring.BM25(corpus, delimiter=' ')
        bm25.getExpandedBM25Score(queries, document_id_list, query_id_list)

    def nxmlConvert(self):
        nxml_obj = Nxml_to_Xml.NxmlConversion("/home/iialab/Bhanu/PythonFiles/Sample_Trec_2016" , "/home/iialab/Bhanu/PythonFiles/sample_Trec_2016_output")
        nxml_obj.convert_nxml_to_xml()
        print("Conversion is Done")

    def basicPreprocessing_2016(self):
        preprocessing_obj = Basicpreprocessing_2016.Preprocessing_2016('/home/iialab/Bhanu/PythonFiles/2016_Trec_Basic_Input', './Data/TREC_2016_OutputData')
        print("Corpus preparation is Done")
        preprocessing_obj.getRootJsonObject()
        print("Basic Preprocessing is done successfully.")




main_obj = Main()
# main_obj.basicpreprocessing()
#main_obj.indexing()
# main_obj.baseLineScoring()
#main_obj.queryexapnsionscoring()
#main_obj.nxmlConvert()
main_obj.basicPreprocessing_2016()
