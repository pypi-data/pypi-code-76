import re
# Noise removal using regular expressions
import nltk

nltk.download('stopwords')
nltk.download('words')
# For removing non-english words
from nltk.corpus import stopwords

stop = set(stopwords.words('english'))
# For removing stop words
from emot.emo_unicode import UNICODE_EMO, EMOTICONS


# For converting emojis to words


class textpreprocessor:

    def __init__(self, text):
        self.text = text

    def remove_noise(self, to_lower=True,
                     hash_remove=True,
                     remove_at=True,
                     remove_alphnum=True,
                     remove_URL=True,
                     remove_punct=True,
                     convert_emoji=True,
                     convert_emoticons=True,
                     remove_non_eng=True,
                     remove_stop_words=True
                     ):

        'Function to remove all noise from the text by default.'
        'The default settings can be turned off,by specifying the required parameter as false'

        if to_lower:
            self.lower()

        if hash_remove:
            self.hash_removal()

        if remove_at:
            self.at_removal()

        if remove_URL:
            self.https_removal()

        if remove_alphnum:
            self.remove_alpnum()

        if remove_punct:
            self.punctuation_removal()

        if convert_emoji:
            self.convert_emojis()

        if convert_emoticons:
            self.convert_emoticons()

        if remove_non_eng:
            self.non_eng()

        if remove_stop_words:
            self.stop_word_removal()

        # to remove extra spaces and lines
        self.text = re.sub("[\s]+", ' ', self.text)
        self.text = re.sub("[\n]+", ' ', self.text)
        return self.text

    def lower(self):
        'Function to convert to lower case'
        self.text = self.text.lower()
        return self

    def hash_removal(self):
        'Function to remove # related words'
        self.text = re.sub(r'#[\w]*', ' ', self.text)
        return self

    def at_removal(self):
        'Function to remove @ related words'
        self.text = re.sub(r'@[\w]*', ' ', self.text)
        return self

    def remove_alpnum(self):
        'Function to remove alphanumeric words'
        self.text = re.sub(r'[^\w]', ' ', self.text)
        return self

    def backslash(self):
        'Function to remove \n '
        self.text = self.text.replace("\\n", " ")
        return self

    def https_removal(self):
        'Function to remove https links '
        self.text = re.sub(r"http\S+", "", self.text)
        return self

    def punctuation_removal(self):
        'Function to remove punctuations '
        self.text = re.sub(r"[^a-zA-Z# ]", "", self.text)
        return self

    def convert_emojis(self):
        'Function to convert emojis to text'
        for emot in UNICODE_EMO:
            self.text = self.text.replace(emot, "_".join(UNICODE_EMO[emot].replace(",", "").replace(":", "").split()))
        return self

    def convert_emoticons(self):
        'Function to convert emoticons to text'
        for emot in EMOTICONS:
            self.text = re.sub(u'(' + emot + ')', "_".join(EMOTICONS[emot].replace(",", "").split()), self.text)
        return self

    def non_eng(self):
        'Function to remove non-english words'
        words = set(nltk.corpus.words.words())
        self.text = " ".join(w for w in nltk.wordpunct_tokenize(self.text) if w.lower() in words or not w.isalpha())
        return self

    def stop_word_removal(self):
        'Function to remove stop words'
        words = set(nltk.corpus.words.words())
        self.text = " ".join(word for word in self.text.split()
                             if not word in stop and '#' not in word.lower())
        return self

