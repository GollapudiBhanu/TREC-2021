import xml.etree.ElementTree as ET
import json
import os
from nltk.corpus import stopwords
from textblob import Word
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import numpy as np

nltk.download("wordnet")
nltk.download('stopwords')

class Preprocessing:

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
                               "weren't", "what", "what's", "when", "will","when's", "where", "where's", "which", "while",
                               "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't",
                               "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",
                               "n't", "'re", "'ve", "'d", "'s", "'ll", "'m",
                               ',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
        all_stopwords = stopwords.words('english')
        self.stopWords_list.append(all_stopwords)
        self.getRootJsonObjectForCorpus()

    '''
        Input_attributes: text_value: String
        Description:
            It takes Input as string value and perofrm below 6 operations
                1. It converts provided text to lowercase.
                2. It removes the punctuation.
                3. It removes the stopWords from the text.
                4. It removes apostrophe
                5. It removes single characters
                6. It removes stopwords.
        Return: text_value: String
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

    ''' 
        Input_attributes: text_value: String
        Description: converts string to lowercase.
        Return: text_value: String
    '''

    def lowerCase(self, text_value):
        if text_value is None:
            return ""
        return " ".join(x.lower() for x in text_value.split())

    ''' 
        Input_attributes: text_value: String
        Description: removes the punctuation from string.
        Return: text_value: String
    '''
    def removePunctuation(self, text_value):
        if text_value is None:
            return ""
        punc_symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"
        for symbol in punc_symbols:
            text_value = np.char.replace(text_value, symbol, '')
        return text_value.tolist()

    ''' 
        Input_attributes: text_value: String
        Description: remove apostrophes from string.
        Return: text_value: String
    '''
    def remove_apostrophe(self, text_value):
        if text_value is None:
            return ""
        return text_value.replace("'", "")

    ''' 
        Input_attributes: text_value: String
        Description: remove single characters from string.
        Return: text_value: String
    '''

    def remove_single_characters(self, text_value):
        if text_value is None:
            return ""
        new_text = ""
        for w in text_value.split():
            if len(w) > 1:
                new_text = new_text + " " + w
        return new_text

    ''' 
        Input_attributes: text_value: String
        Description: removes stopwords from string.
        Return: text_value: String
    '''
    def removeStopwords(self, text_value):
        if text_value is None:
            return ""
        return " ".join(x for x in text_value.split() if x not in self.stopWords_list)

    ''' 
        Description: Converts the list of corpus data in to words.
        Return: singleWordList: List
    '''

    def tokenization(self):
        singleWordList = [
            [word for word in document.split() if word not in self.stopWords_list]
            for document in self.corpus
        ]
        return singleWordList

    ''' 
            Description: Converts the list value(json values)data in to words.
            Return: singleWordList: List
    '''
    def valueTokenization(self):
        singleWordList = [
            [word for word in document.split() if word not in self.stopWords_list]
            for document in self.documentData
        ]
        return singleWordList

    '''
        Description: returns list of list words, whose count of frequency of words is grater than 1.
        Return: texts: [[]]
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
        Description: returns the Most commonly used words from the corpus.
        Return: ret_list: [[]]
    '''

    def getCommonWords(self):
        frequ = self.getCommonfrequencyWords()
        ret_list = []
        most_list = frequ.most_common(400)
        for value in most_list:
            ret_list.append(value[0])
        return ret_list

    '''
        Description: using NLTK get the frequency of common words.
        Return: freq: []
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
        Description: 
            1. Get common frquency words from corpus.
            2. Sort the values based on the frequency and return the sorted list.
        Return: ret_list: []
    '''

    def getTopFrequencyItems(self, number):
        commoList = self.getCommonfrequencyWords()
        sortedItems = sorted(commoList.items(), key=lambda x: x[1], reverse=True)
        ret_list = []
        for value in sortedItems:
            ret_list.append(value[0])
        return ret_list[0:number]

    '''
        Description: 
            1. Get common frquency words from corpus.
            2. Add the common frequency words to stopWords_list.
        Return: common_stop_word_list: []
    '''

    def addCommonWordsToStopList(self):
        top_freq_list = self.getTopFrequencyItems(5)
        common_stop_word_list = self.stopWords_list + top_freq_list
        return common_stop_word_list

    '''
        Description: It converts List to string 
        Return: convertList: String
    '''

    def listToString(self, data_list):
        convertList = ''.join(map(str, data_list))
        return convertList

    '''
        Description: Using PorterStemmer, get the corpus values and perform stemming of words.
        Return: commonList: []
    '''

    def stemming(self):
        commonList = self.getCorpusList()
        st = PorterStemmer()
        for document in commonList:
            for place, data in enumerate(document):
                document[place] = "".join([st.stem(word) for word in data.split()])
        return commonList

    '''
        Description: Using PorterStemmer, get the tokenization of words and perform stemming of words.
        Return: commonList: []
    '''

    def objectStemming(self):
        commonList = self.tokenization()
        st = PorterStemmer()
        for document in commonList:
            for place, data in enumerate(document):
                document[place] = "".join([st.stem(word) for word in data.split()])
        return commonList

    '''
        Description: Using WordNetLemmatizer, get the tokenization of words and perform Lemmatization of words.
        Return: stemList: [].
    '''

    def lemmatization(self, stemList):
        wordnet_lemmatizer = WordNetLemmatizer()
        for words in stemList:
            for index, word in enumerate(words):
                words[index] = " ".join(
                    [wordnet_lemmatizer.lemmatize(word) for word in word.split()])
        return stemList

    '''`
        Description: Using WordNetLemmatizer, get the tokenization of words and perform Lemmatization of words.
        Return: lemmatizationList: [].
    '''

    def lemmatize(self):
        lemmatizationList = self.stemming()
        for words in lemmatizationList:
            for index, word in enumerate(words):
                words[index] = " ".join([Word(word).lemmatize() for word in word.split()])
        return lemmatizationList

    '''
        Description: Using PorterStemmer, get the tokenization of words and perform stemming of words.
        Return: commonList: []
    '''

    def perform_stemming(self, lem_list):
        st = PorterStemmer()
        for words in lem_list:
            for index, word in enumerate(words):
                words[index] = " ".join(
                    [st.stem(word) for word in word.split()])
        return lem_list

    '''
        Description:
            1. Get commonWords from corpus and add them to stopWordsList.
            2. Preprocess the text_value.
            3. Apply lemmatization for Tokenized words in the List.

        Return: string
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
        Description:
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
                    tree = ET.parse(self.source_dir + '/' + folder + '/' + sub_folder + '/' + file)
                    root = tree.getroot()
                    self.corpusPrepration(root)

    '''
        Description:
            1. List out all sub-directories
            2. Enumearte all folders and retrieve all xml files.
            3. Using ET, parse the root object from XML file.
    '''

    def getRootJsonObject(self):
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
                    tree = ET.parse(self.source_dir + '/' + folder + '/' + sub_folder + '/' + file)
                    root = tree.getroot()
                    base = os.path.split(file)
                    fileName = os.path.splitext(base[1])
                    output_file_path = self.dest_dir + '/' + folder + '/' + sub_folder + '/' + fileName[0]
                    self.prepareJsonObject(root, output_file_path)

    '''
        Description:
            1. It appends the key value pairs in to data dict.
            2. Prepares a JSON_Object
            3. Write the JSON object in to output file.
    '''

    def prepareJsonObject(self, root, output_file_path):
        data = {}
        for subRootElement in root:
            data[subRootElement.tag] = []
            if len(subRootElement) == 0:
                if subRootElement.tag == "brief_title" or "article-title" or "abstract" or "introduction" or "conclusion" or "official_title":
                    value = self.valuePreprocessing(subRootElement.text)
                    data[subRootElement.tag] = value
                else:
                    data[subRootElement.tag] = subRootElement.text
            for j in subRootElement:
                j_value = j.text
                if j.tag == "textblock" or "article-title" or "abstract" or "introduction" or "conclusion" or "brief_title" or "official_title" or "description":
                    j_value = self.valuePreprocessing(j_value)
                data[subRootElement.tag].append({
                    j.tag: j_value
                })
        json_object = json.dumps(data, indent=1)
        with open(output_file_path + '.json', 'w') as outfile:
            outfile.write(json_object)

    '''
        Description
            1. It appends the key value pairs in to data dict.
            2. Prepares a JSON_Object
            3. Prepares corpus(documentData) with all files data.
    '''

    def corpusPrepration(self, root):
        data = {}
        for index, subRootElement in enumerate(root):
            data[subRootElement.tag] = []
            if len(subRootElement) == 0:
                data[subRootElement.tag] = self.preProcessingText(subRootElement.text)

            for j in subRootElement:
                data[subRootElement.tag].append({
                    j.tag: self.preProcessingText(j.text)
                })
        json_object = json.dumps(data, indent=1)
        json_object = json.loads(json_object)
        fileData = list()
        for key, value in json_object.items():
            if isinstance(value, list):
                for element in value:
                    if isinstance(element, dict):
                        for _, value in element.items():
                            fileData.append(str(value))
                    else:
                        fileData.append(str(value))
        self.corpus.append(self.listToString(fileData))