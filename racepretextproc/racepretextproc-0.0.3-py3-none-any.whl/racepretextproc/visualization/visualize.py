from wordcloud import WordCloud as wc
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize


class WordCloud:
    """
    Create word cloud from text
    """
    wc_obj: wc = None

    def __init__(self, **kwargs):
        self.wc_obj = wc(**kwargs)

    def show(self, text):
        """
        Show word cloud for give text.
        This method will process the text by Splits a long text into words, eliminates the stopwords.
        :param text: Text to plot wordcloud
        :return: None
        """
        wcloud = self.wc_obj.generate_from_text(text)
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()


class FrequencyDist:
    """
    Class to plot frequency distribution for a given text
    """

    def __init__(self):
        print("Frequency distribution constructor")

    @staticmethod
    def show(text, min_length=3, nof_large_words=50):
        """
        Show words frequency distribution of give text
        :param text: text to plot frequency distribution
        :param min_length: minimum length of the word to consider
        :param nof_large_words: No. of maximum words to plot on graph
        :return:

        :Notes
        ---------
        Given :param text will be not do any preprocessing including lower case, punctuation and others.
        """
        # Convert text to words array using NLTK word tokenizer
        wt_words = word_tokenize(text)
        # Create frequency distribution for a tokenized text
        frequency_dist = FreqDist(wt_words)
        # Filter the words with given minimum length
        large_words = dict([(k, v) for k, v in frequency_dist.items() if len(k) >= min_length])
        # Create frequency distribution for large words
        frequency_dist = FreqDist(large_words)
        # show distribution map
        frequency_dist.plot(nof_large_words, cumulative=False)
