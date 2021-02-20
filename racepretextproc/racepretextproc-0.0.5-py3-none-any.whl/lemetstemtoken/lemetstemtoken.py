
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from textblob import Word

class lemetization_stemming_tokenization:


    def __init__(self, text):
        self.text = text

   #function for Stemming, Lemmetization, tokenisation
    def lemet_stem_token(self,
                         do_stem=False,
                         do_lemet=True):
        # Tokenize text into words
        self.words = self.getTokens()

        if do_stem:
            self.doStemming()

        if do_lemet:
            self.doLemmetization()

        return self.text
    
    #function for Stemming
    def doStemming(self):
        pst = PorterStemmer()
        self.text = ""
        # for word in self.words:
        #     self.text += " ".join(st.stem(word))
        self.text = " ".join([pst.stem(word) for word in self.words])
        return self.text

    #function for Lemmetization
    def doLemmetization(self):
        # lemmatizer = WordNetLemmatizer()
        self.text = ""
        # for word in self.words:
        #     self.text += " ".join(lemmatizer.lemmatize(word))

        self.text = " ".join([Word(word).lemmatize() for word in self.words])
        return self.text
    
    #function for tokenisation
    def getTokens(self):
        return word_tokenize(self.text)
