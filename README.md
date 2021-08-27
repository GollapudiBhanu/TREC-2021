# TREC

**Basic Preprocessing**: 
   
   we are performing the Basic preprocessing steps 
      
      1. Conversion of Lowercase.
      2. Remove Punctuations.
      3. Remove apostrophe.
      4. Remove single_characters.
      5. Remove Stopwords.
      6. Remove Common stopwords.
      7. performs valueTokenization.
      8. Perform stemming
      9. Perform lemmatization
  
  and converting the XML or NXML files to JSON files. 
    
   ```ruby
   
    def perform_TREC_2021(self, input_folder_path, out_folder_path, index_name, query_file_path,
                         raw_out_score_file_path, exp_out_score_file_path, comb_out_score_file_path)
   ```

  input_folder_path: Raw Data folder path(XML files folder path). \
  out_folder_path: Preprocessed folder path (Json files). \
  index_name: Elastic search Index name. \
  query_file_path: Query file path(.csv). \
  raw_out_score_file_path: output of Raw query scores file path(.csv).\
  exp_out_score_file_path: output of Expansion query scores file path(.csv). \
  comb_out_score_file_path: output of combination of both RAW and Expansion query scores(.csv). \
  

 **INDEXING**
    
 We are extacting the required filed and their values from the files and saving them in the elastic search using index and index_name.
    
   
   ```ruby
   
    def indexing_2021(self, input_path, index_name)
   ```
   
 
 **Basic Evaluation**
    
 We are performing Basic Evaluation in 3 steps, for getting the scores.
         
         1. Retrieve RAW query results.
         2. Retrieve Query-Expanison results.
         3. Combine RAW + Query-Expansion results and save it in to single file.
         
    
   
   ```ruby
   
        def saveScores(self, index_name, query_file_path, raw_out_score_file_path, exp_out_score_file_path, comb_out_score_file_path):
            self.getRawQueryscore(query_file_path, raw_out_score_file_path, 'summary', index_name)
            self.getQueryExapansionscore(query_file_path, exp_out_score_file_path, 'summary', index_name)
            self.extractNERBaseLineScoresFromFiles(raw_out_score_file_path, exp_out_score_file_path,
                                               comb_out_score_file_path)
   ```
   
   index_name: Elastic search index name.
   query_file_path: Query file path
   raw_out_score_file_path: RAW query results file path
   exp_out_score_file_path: Exapnsion Query results file path.
   comb_out_score_file_path: Combine RAW + Query Expansion results path
   
   
 **Utilities**:
 
   1. ConvertTSV.py: Convert the given CSV file in to TSV.
   2. Count.py: Caluculate the number of documnets in each query id.used to find the duplicate id's with in queryid's
   3. Evaluation.py: Used to find the duplicate documnet id's with in queryid's.
   4. Evalution_2016.py: Used to find the same document text for the document id's.
   5. ExtractDocument.py: Extract the concat string for the provided documnet id.
   6. Nxml_to_Xml.py: Used to convert NXML file to XML file.
   7. RandomFloat.py: Used to generate list of Random float numbers
   8. Recall.py: Used to find the number of relevant documents form output file, using TREC judgement file
   9. RerankingDataSet.py:  Used for preparing the Reranking Json file.
   10. XML_To_Dict.py: Used to conversion of XML file to JSON dict.
   
**Note**: 

   1. For Query file path, here all the header names should be same \
   2. We are keeping the Raw Query scores top and Expansion Query scores below, and we are grouping the scores based on the QueryID's. 
  







