def gen(text):
    import re
    tweet = text
    #Removes unicode strings like "\u002c" and "x96" 
    tweet = re.sub(r'(\\u[0-9A-Fa-f]+)',r'', tweet)       
    tweet = re.sub(r'[^\x00-\x7f]',r'',tweet)
    #convert any url to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
    #Convert any @Username to "AT_USER"
    tweet = re.sub('@[^\s]+','',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub('[\n]+', ' ', tweet)
    #Remove not alphanumeric symbols white spaces
    tweet = re.sub(r'[^\w]', ' ', tweet)
    #Removes hastag in front of a word """
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #Remove :( or :)
    tweet = tweet.replace(':)','')
    tweet = tweet.replace(':(','')
    #remove numbers
    #tweet = ''.join([i for i in tweet if not i.isdigit()]) 
    #remove multiple exclamation
    tweet = re.sub(r"(\!)\1+", ' ', tweet)
    #remove multiple question marks
    tweet = re.sub(r"(\?)\1+", ' ', tweet)
    #remove multistop
    tweet = re.sub(r"(\.)\1+", ' ', tweet)
    #Removing Punctuation
    tweet = re.sub(r'[^\w\s]','',tweet)

    tweet = tweet.strip('\'"')

    return tweet

def stopw(text, ext =[]):
    from nltk.corpus import stopwords   
    tweet = text
    #remove stop words
    stop = stopwords.words('english') + ext
    tweet = ' '.join([x for x in tweet.split() if x.lower() not in stop])

    return tweet
    
    # Funtion for Lemmetization
def lemma(text):
    tweet = text
    #lemma
    from textblob import Word
    tweet =" ".join([Word(word).lemmatize() for word in tweet.split()])

    return tweet    
    
    # Function for Stemming
def stem(text):
    from nltk.stem import PorterStemmer 
    tweet = text
    st = PorterStemmer()
    tweet=" ".join([st.stem(word) for word in tweet.split()])
    return tweet
    
    # Function for converting to Lower case
def low(text):
    tweet = text
    #Lower case
    tweet = tweet.lower()
    return tweet
    
    # Function for remving digits
def dig(text):       
    tweet = text
    #remove numbers
    tweet = ''.join([i for i in tweet if not i.isdigit()]) 
    return tweet  
    
    #Function to remove less than 2 word letters
def clean_len(text):
    tweet = text
    #remove numbers
    tweet = ' '.join([i for i in tweet.split() if len(i) >2])
    return tweet

    #Function for spell correction
def spell(text):
    from textblob import TextBlob
    tweet = text
    return str(TextBlob(text).correct())


    #Function for Countvectorization
def countvec(df):
    import pandas as pd
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer()
    count_vector=cv.fit_transform(df)
    
    return count_vector, cv.get_feature_names(), pd.DataFrame(count_vector.toarray(), columns=cv.get_feature_names())

    #Function for TFIDF
def tfidf(df):
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer()
    tfidf_vector=tfidf.fit_transform(df)
    
    return tfidf_vector, tfidf.get_feature_names(), pd.DataFrame(tfidf_vector.toarray(), columns=tfidf.get_feature_names())


# Import Library for computing frequency
def WCloud(process):
    
    allWords = ' '.join([twts for twts in process])
    import nltk
    from nltk.corpus import webtext
    #nltk.download('webtext')
    #wt_sentences = webtext.sents(allWords)
    #wt_words = webtext.words(allWordsords)

    from nltk.probability import FreqDist
    #from nltk.corpus import stopwords
    import string
        
    allWords_words = allWords.split()

    len(allWords_words)
    #len(wt_words)

    frequency_dist = nltk.FreqDist(allWords_words)
    print(frequency_dist)

    sorted_frequency_dist =sorted(frequency_dist,key=frequency_dist.__getitem__, reverse=True)
    sorted_frequency_dist

    large_words = dict([(k,v) for k,v in frequency_dist.items() if len(k)>3])

    frequency_dist = nltk.FreqDist(large_words)
    frequency_dist.plot(50, cumulative=False)

    from wordcloud import WordCloud
    wcloud = WordCloud().generate_from_frequencies(frequency_dist)

    import matplotlib.pyplot as plt
    
    plt.imshow(wcloud, interpolation='bilinear')
    plt.axis("off")
    (-0.5, 399.5, 199.5, -0.5)
    plt.show