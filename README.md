# TREC-2021 @UNT

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
   
   
  
 **Note**:  
 1. For Query file path, here all the header names should be same \
 2.We are keeping the Raw Query scores top and Expansion Query scores below, and we are grouping the scores based on the QueryID's. 
  
  def indexing_2021(self, input_path, index_name):







