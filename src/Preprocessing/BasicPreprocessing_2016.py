"""
To Run the Script:
$ python3 [source directory of collection] [destination directory]
     Example:
     $ python3 /home/iialab/Downloads/Preprocessing.py /home/iialab/Downloads/clinical_trials.0 /home/iialab/Downloads/clinical_trials_new
"""

import xml.etree.ElementTree as ET
import json
import os
import sys
from nltk.corpus import stopwords
from textblob import Word
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import numpy as np
import xmltodict

nltk.download("wordnet")
nltk.download('stopwords')


class Preprocessing_2016:
    '''
        Input:
            1.source_dir: Input directory path(ex: Data/TREC_2019_input_data)
            2.dest_dir: Where you want to save the converted files(ex: Data/TREC_2019_Output_data)
    '''
    def __init__(self, source_dir, dest_dir):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.documentData = []
        self.corpus = []
        self.commonWords = []
        self.stopWords_list = ["disease", "diseases", "disorder", "symptom", "symptoms", "drug", "drugs", "problems",
                               "problem", "prob", "probs",
                               "med", "meds", "pill", "pills", "medicine", "medicines", "medication", "medications",
                               "treatment", "treatments", "caps", "capsules",
                               "capsule", "tablet", "tablets", "tabs", "doctor", "dr", "dr.", "doc", "physician",
                               "physicians", "test", "tests", "testing", "specialist",
                               "specialists", "side-effect", "side-effects", "pharmaceutical", "pharmaceuticals",
                               "pharma", "diagnosis", "diagnose", "diagnosed", "exam",
                               "challenge", "device", "condition", "conditions", "suffer", "suffering", "suffered",
                               "feel", "feeling", "prescription", "prescribe",
                               "prescribed", "over-the-counter", "otc", "a", "about", "above", "after", "again",
                               "against", "all", "am", "an", "and", "any", "are",
                               "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between",
                               "both", "but", "by", "can", "can't", "cannot",
                               "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
                               "during", "each", "few", "for", "from",
                               "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd",
                               "he'll", "he's", "her", "here",
                               "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
                               "i'm", "i've", "if", "in", "into",
                               "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't",
                               "my", "myself", "no", "nor", "not", "of",
                               "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out",
                               "over", "own", "same", "shan't", "she", "she'd",
                               "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
                               "the", "their", "theirs", "them", "themselves",
                               "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
                               "this", "those", "through", "to", "too", "under",
                               "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
                               "weren't", "what", "what's", "when", "will," "when's", "where", "where's", "which",
                               "while",
                               "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't",
                               "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",
                               "n't", "'re", "'ve", "'d", "'s", "'ll", "'m", ',', '.', ':', ';', '?', '(', ')', '[',
                               ']', '&',
                               '!', '*', '@', '#', '$', '%']
        all_stopwords = stopwords.words('english')
        self.stopWords_list.append(all_stopwords)
        self.getRootJsonObjectForCorpus()

    '''
          1. It converts provided text to lowercase.
          2. It removes the punctuation.
          3. It removes the stopWords from the text.

     '''

    def preProcessingText(self, text_value):
        if text_value is None:
            return ""
        text_value = self.lowerCase(text_value)
        text_value = self.removePunctuation(text_value)
        text_value = self.remove_apostrophe(text_value)
        text_value = self.remove_single_characters(text_value)
        text_value = self.removeStopwords(text_value)
        return text_value

    def lowerCase(self, text_value):
        try:
            return " ".join(x.lower() for x in text_value.split())
        except:
            return ""
    def removePunctuation(self, text_value):
        punc_symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`'{|}~\n"
        for symbol in punc_symbols:
            text_value = np.char.replace(text_value, symbol, '')
        return text_value.tolist()

    def remove_apostrophe(self, text_value):
        return text_value.replace("'", "")

    '''
        It removes the single character from the text
    '''

    def remove_single_characters(self, text_value):
        new_text = ""
        for w in text_value.split():
            if len(w) > 1:
                new_text = new_text + " " + w
        return new_text

    def removeStopwords(self, text_value):
        try:
            return " ".join(x for x in text_value.split() if x not in self.stopWords_list)
        except:
            return ""

    '''
          It returns list of words from the documentData.
     '''

    def tokenization(self):
        singleWordList = [
            [word for word in document.split() if word not in self.stopWords_list]
            for document in self.corpus
        ]
        return singleWordList

    def valueTokenization(self):
        singleWordList = [
            [word for word in document.split() if word not in self.stopWords_list]
            for document in self.documentData
        ]
        return singleWordList

    '''
          It returns list of list words, whose count of frequency of words is garter than 1.
     '''

    def getCorpusList(self):
        singleWordList = self.tokenization()
        word_count_dict = {}
        for text in singleWordList:
            for token in text:
                word_count = word_count_dict.get(token, 0) + 1
                word_count_dict[token] = word_count
        texts = [[token for token in text if word_count_dict[token] > 1]
                 for text in singleWordList]
        return texts

    '''
          It returns the Most commonly used words from the corpus.
     '''

    def getCommonWords(self):
        frequ = self.getCommonfrequencyWords()
        ret_list = []
        most_list = frequ.most_common(400)
        for value in most_list:
            ret_list.append(value[0])
        return ret_list

    '''
          It returns the Most commonly used words from the corpus, with their frquency.
     '''

    def getCommonfrequencyWords(self):
        commonwordList = self.tokenization()
        joined_list = list()
        for wordsList in commonwordList:
            for words in wordsList:
                joined_list.append(words)
        freq = nltk.FreqDist(joined_list)
        return freq

    '''
          1. Get commonWords from corpus.
          2. Sort the values based on the frequency and return the sorted list.
     '''

    def getTopFrequencyItems(self, number):
        commoList = self.getCommonfrequencyWords()
        sortedItems = sorted(commoList.items(), key=lambda x: x[1], reverse=True)
        ret_list = []
        for value in sortedItems:
            ret_list.append(value[0])
        return ret_list[0:number]

    '''
          Get the commonWords and add them to stop_word list.
     '''

    def addCommonWordsToStopList(self):
        top_freq_list = self.getTopFrequencyItems(1000)
        common_stop_word_list = self.stopWords_list + top_freq_list
        return common_stop_word_list

    '''
          It converts List to string and returns string value

     '''

    def listToString(self, data_list):
        convertList = ''.join(map(str, data_list))
        return convertList

    '''
          Perform Stemming of words.
     '''

    def stemming(self):
        commonList = self.getCorpusList()
        st = PorterStemmer()
        for document in commonList:
            for place, data in enumerate(document):
                document[place] = "".join([st.stem(word) for word in data.split()])
        return commonList

    '''
          Perform Stemming of words.
     '''

    def objectStemming(self):
        commonList = self.tokenization()
        st = PorterStemmer()
        for document in commonList:
            for place, data in enumerate(document):
                document[place] = "".join([st.stem(word) for word in data.split()])
        return commonList

    '''getCommonWords
          Perform lemmatization by using WordNetLemmatizer.
     '''

    def lemmatization(self, stemList):
        nltk.download("wordnet")
        wordnet_lemmatizer = WordNetLemmatizer()
        for words in stemList:
            for index, word in enumerate(words):
                words[index] = " ".join(
                    [wordnet_lemmatizer.lemmatize(word) for word in word.split()])
        return stemList

    '''
          1. getCommonWords
          2. Perform lemmatization by using NLTK Word.
     '''

    def lemmatize(self):
        nltk.download("wordnet")
        lemmatizationList = self.stemming()
        for words in lemmatizationList:
            for index, word in enumerate(words):
                words[index] = " ".join([Word(word).lemmatize() for word in word.split()])
        return lemmatizationList

    '''
        Perform Stemming 
    '''

    def perform_stemming(self, lem_list):
        st = PorterStemmer()
        for words in lem_list:
            for index, word in enumerate(words):
                words[index] = " ".join(
                    [st.stem(word) for word in word.split()])
        return lem_list

    '''
        1. Get commonWords from corpus and add them to stopWordsList.
        2. Preprocess the text_value.
        3. Apply lemmatization for Tokenized words in the List.
    '''

    def valuePreprocessing(self, text_value):
        if text_value == None:
            return ""
        self.documentData.clear()
        pre_proceed_text_value = self.preProcessingText(text_value)
        self.documentData.append(pre_proceed_text_value)
        tokens_list = self.valueTokenization()
        stem_out_put = self.perform_stemming(tokens_list)
        lem_out_put = self.lemmatization(stem_out_put)
        for output in lem_out_put:
            return ' '.join(map(str, output))


    '''
          1. List out all sub-directories
          2. Enumearte all folders and retrieve all xml files.
          3. Using ET, parse the root object from XML file.
     '''

    def getRootJsonObjectForCorpus(self):
        sub_dirs = os.listdir(self.source_dir)
        self.stopWords_list = self.addCommonWordsToStopList()
        for folder in sub_dirs:
            sub_folders = os.listdir(self.source_dir + '/' + folder)
            for sub_folder in sub_folders:
                trec_dir = self.dest_dir + '/' + folder + '/' + sub_folder
                if not os.path.exists(trec_dir):
                    os.makedirs(trec_dir)
                xml_files = os.listdir(self.source_dir + '/' + folder + '/' + sub_folder)
                for file in xml_files:
                    with open(self.source_dir + '/' + folder + '/' + sub_folder + '/' + file, 'r') as file:
                        data_dict = xmltodict.parse(file.read())
                        file.close()
                    self.corpusPrepration(data_dict)

    '''
          1. List out all sub-directories
          2. Enumearte all folders and retrieve all xml files.
          3. Using ET, parse the root object from XML file.
     '''

    def getRootJsonObject(self):
        sub_dirs = os.listdir(self.source_dir)
        self.stopWords_list = self.addCommonWordsToStopList()
        print(self.stopWords_list)
        for folder in sub_dirs:
            sub_folders = os.listdir(self.source_dir + '/' + folder)
            for sub_folder in sub_folders:
                trec_dir = self.dest_dir + '/' + folder + '/' + sub_folder

                if not os.path.exists(trec_dir):
                    os.makedirs(trec_dir)

                xml_files = os.listdir(self.source_dir + '/' + folder + '/' + sub_folder)

                for xml_file in xml_files:
                    with open(self.source_dir + '/' + folder + '/' + sub_folder + '/' + xml_file, 'r') as file:
                        data_dict = xmltodict.parse(file.read())
                        file.close()
                    base = os.path.split(xml_file)
                    fileName = os.path.splitext(base[1])
                    output_file_path = self.dest_dir + '/' + folder + '/' + sub_folder + '/' + fileName[0]
                    self.prepareJsonObject(data_dict, output_file_path)

    '''
          1. It appends the key value pairs in to data dict.
          2. Prepares a JSON_Object
          3. Write the JSON object in to output file.

     '''

    def prepareJsonObject(self, root, output_file_path):
        data = {}
        for key, value in root.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, dict):
                        for childkey, childvalue in subvalue.items():
                            if childkey == "abstract" or "subheading" or "introduction" or "conclusion" or "article-title" or "brief_title" or "article-title" or "abstract" or "introduction" or "conclusion" or "official_title":
                                data[childkey] = self.valuePreprocessing(childvalue)
                            else:
                                data[childkey] = childvalue
                    else:
                        if subkey == "abstract" or "subheading" or "introduction" or "conclusion" or "article-title" or "textblock" or "article-title" or "abstract" or "introduction" or "conclusion" or "brief_title" or "official_title" or "description":
                            data[subkey] = self.valuePreprocessing(subvalue)
                        else:
                            data[subkey] = subvalue
            else:
                if key == "abstract" or "subheading" or "introduction" or "conclusion" or "article-title" or "textblock" or "article-title" or "abstract" or "introduction" or "conclusion" or "brief_title" or "official_title" or "description":
                    data[key] = self.valuePreprocessing(value)
                else:
                    data[key] = value
        json_object = json.dumps(data, indent=1)
        with open(output_file_path + '.json', 'w') as outfile:
            outfile.write(json_object)

    '''
          1. It appends the key value pairs in to data dict.
          2. Prepares a JSON_Object
          3. Prepares corpus(documentData) with all files data.

     '''

    def corpusPrepration(self, root):
        data = {}
        for key, value in root.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, dict):
                        for childkey, childvalue in subvalue.items():
                            data[childkey] = self.preProcessingText(childvalue)
                    else:
                        data[subkey] = self.preProcessingText(subvalue)
            else:
                data[key] = self.preProcessingText(value)
        json_object = json.dumps(data, indent=1)
        json_object = json.loads(json_object)
        fileData = list()
        for _, value in json_object.items():
            fileData.append(str(value))
        self.corpus.append(self.listToString(fileData))
