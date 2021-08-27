import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import Word
import numpy as np

nltk.download("wordnet")
nltk.download('stopwords')

'''
This file is used to Basic preprocessing, we are not using this, if we want to sepaarte preprocessing we will use this.
'''
class Preprocessing:

    def __init__(self):
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

    def preprocess(self, text_value):
        if text_value == None:
            return ""
        pre_proceed_text_value = self.preProcessingText(text_value)
        tokens_list = self.valueTokenization()
        stem_out_put = self.perform_stemming(tokens_list)
        lem_out_put = self.lemmatization(stem_out_put)
        for output in lem_out_put:
            return ' '.join(map(str, output))


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

    def remove_single_characters(self, text_value):
        new_text = ""
        for w in text_value.split():
            if len(w) > 1:
                new_text = new_text + " " + w
        return new_text


    def valueTokenization(self):
        singleWordList = [
            [word for word in document.split() if word not in self.stopWords_list]
            for document in self.documentData
        ]
        return singleWordList

    def removeStopwords(self, text_value):
        try:
            return " ".join(x for x in text_value.split() if x not in self.stopWords_list)
        except:
            return ""

    def perform_stemming(self, lem_list):
        st = PorterStemmer()
        for words in lem_list:
            for index, word in enumerate(words):
                words[index] = " ".join(
                    [st.stem(word) for word in word.split()])
        return lem_list

    def lemmatization(self, stemList):
        nltk.download("wordnet")
        wordnet_lemmatizer = WordNetLemmatizer()
        for words in stemList:
            for index, word in enumerate(words):
                words[index] = " ".join(
                    [wordnet_lemmatizer.lemmatize(word) for word in word.split()])
        return stemList