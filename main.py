import BasicPreprocessing
import Indexing2019
import QueryExpansionList
import Corpus
import Bm25_scoring
import Queries
import OkapiBm25
import BoolQuery
import Queryexpansion
import BasicPreprocessing_2016
import Indexing2016


class Main:
    """
        Basic Preprocessing
    """

    def basicpreprocessing(self):
        basic_preprocessing = BasicPreprocessing.Preprocessing('./Data/TREC_2019_input_data', './Data/TREC_2019_Output_data')
        basic_preprocessing.getRootJsonObject()

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
        BaseLineScoring
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
        query = Queries.GetQuery("./Data/2019_quries/topics2019.xml")
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
        corpus = self.preparecorpus()[0]
        document_id_list = self.preparecorpus()[1]

        queries = self.expandedQuery()[0]
        query_id_list = self.expandedQuery()[1]

        bm25 = Bm25_scoring.BM25(corpus, delimiter=' ')
        bm25.getExpandedBM25Score(queries, document_id_list, query_id_list)

    def getOKAPIBm25baselinescoring(self):
        corpus = self.preparecorpus()[0]
        document_id_list = self.preparecorpus()[1]

        queries = self.baselinequery()

        bm25 = OkapiBm25.OKAPIBM25_Scoring(corpus)
        bm25.getBM25Score(queries, document_id_list)

    def getOKAPIBm25QueryExpansionscoring(self):
        corpus = self.preparecorpus()[0]
        document_id_list = self.preparecorpus()[1]

        queries = self.expandedQuery()[0]
        query_id_list = self.expandedQuery()[1]

        bm25 = OkapiBm25.OKAPIBM25_Scoring(corpus)
        bm25.getQueryExapnsionBM25Score(queries, document_id_list, query_id_list)


    def getScoreusingBoolQuery(self):
        bool_query = BoolQuery.GetBoolQuery("./Data/2019_quries/topics2019.xml")

    def queryExpansion(self):
        expanded_query = Queryexpansion.NewExapndedQuery('./Data/Expansiontopics2019.csv')
        expanded_query_list = expanded_query.getGroupedData()
        expanded_query_id_list = expanded_query.removeDuplicates()
        return expanded_query_list, expanded_query_id_list

    def basicpreprocessing2016(self):
        preprocessing_obj = BasicPreprocessing_2016.Preprocessing_2016('./Data/2016_Trec_Basic_Input',
                                               './Data/TREC_2016_OutputData')
        print("Corpus preparation is Done")
        preprocessing_obj.getRootJsonObject()
        print("Basic Preprocessing is done successfully.")

    '''
        Expanded Query List
    '''

    def expandedQuery2019(self):
        expanded_query = QueryExpansionList.ExapndedQuery('./Data/topics2019_expanded.csv')
        expanded_query_list = expanded_query.getGroupedData()
        expanded_query_id_list = expanded_query.removeDuplicates()
        return expanded_query_list, expanded_query_id_list

    def Indexing_2016(self):
        _ = Indexing2016.Indexing_2016('./Data/TREC_2016_OutputData')
        print("Indexing is done")

    """
            Basic Preprocessing
    """

    def basicpreprocessing_2021(self):
        basic_preprocessing = BasicPreprocessing.Preprocessing('./Data/TREC_2021_Basicpreprocessing_Input',
                                                               './Data/TREC_2021_Basicpreprocessing_output')
        basic_preprocessing.getRootJsonObject()






main_obj = Main()
# main_obj.basicpreprocessing()
#main_obj.indexing()
#main_obj.baselinequery()
#main_obj.baseLineScoring()
#main_obj.queryexapnsionscoring()
#main_obj.getOKAPIBm25baselinescoring()
#main_obj.getOKAPIBm25QueryExpansionscoring()
#main_obj.getScoreusingBoolQuery()
#tupe =  main_obj.queryExpansion()
#main_obj.expandedQuery2019()
#main_obj.Indexing_2016()
main_obj.basicpreprocessing_2021()