# %%
import numpy as np
import pandas as pd

import multiprocessing

from functools import partial
import copy

# %%

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.sparse import hstack, vstack, csr_matrix

# %%
from sklearn.base import TransformerMixin, BaseEstimator


# %%

class TokenizerTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, tokenize_func):
        
        self.tokenize_func = tokenize_func    
    
    def fit(self, X, y=None):
        return self
    
    def transform(self,X,y=None):
        
        X = [self.tokenize_func(sentence) for sentence in X]
        return X
    
class TokenTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, func):
        self.func = func
    
    def fit(self, X, y=None):
        return self
    
    def transform(self,X,y=None):
        
        X = [[self.func(token) for token in tokens] for tokens in X]
        return X
    
    

class SentenceTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, func, multi=False):
        self.func = func
        self.multi = multi
    
    def fit(self, X, y=None):
        return self
    
    def transform(self,X,y=None):
        
        if(self.multi):
            with multiprocessing.Pool(multiprocessing.cpu_count()-1) as p:
                X = p.map(self.func, X)
        else:
            X = [self.func(sentence) for sentence in X]
        
        return X
    
    


# %%

class WordvectorTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, get_word_vector_func):
        self.get_word_vector_func = get_word_vector_func
        pass
    
    def fit(self, X, y=None):            
        return self
    
    def transform(self,X,y=None):
        
        X = [[ self.get_word_vector_func(token) for token in tokens] for tokens in X]
        return X
    
class WordvectorDiscreteTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, q=10):
        
        self.q = q    
    
    def fit(self, X, y=None):
        wv = np.array( [token for tokens in X for token in tokens] )
        
        dimbins = []
        for i in range(wv.shape[1]):
            bins = pd.qcut(wv[:,i], self.q, labels=range(self.q), retbins=True)[1]
            bins[0] = -np.inf
            bins[-1] = np.inf
            
            dimbins.append(bins)
        
        self.dimbins = dimbins
        
        return self
    
    def transform(self,X,y=None):
        
        X = [ self.make_discrete(tokens) for tokens in X]
        return X
    
    def make_discrete(self, tokens):
        
        
        def prefix(discrete_i, dim_i):
            return str(discrete_i) + '_' + str(dim_i)
        
        
        tokens = np.array(tokens)
        result = []
        
        for i in range(tokens.shape[1]):
            temp = tokens[:,i]
            temp = pd.cut(temp, bins=self.dimbins[i], labels=False, include_lowest=True)
            temp = list(map(partial(prefix, i), temp))
            result.append(temp)
        
        result = [dim for dims in result for dim in dims]
        
        return result



# %%

class SupervisedMergedTfidfTransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self, **tfidfvectorizerargs):
        
        self.tfidf = TfidfVectorizer(**tfidfvectorizerargs)
        
        pass
    
    def fit(self, X, y):
        
        df = pd.DataFrame()
        df['X'] = X
        df['y'] = y
        docs = df.groupby('y').sum()['X']
        
        self.tfidf.fit(docs)
        
        return self
    
    def transform(self, X):
        
        return self.tfidf.transform(X)
        
        
    def set_params(self, **kwargs):
        self.__init__(**kwargs)
    
    
class SupervisedCdfidfTransformer(BaseEstimator, TransformerMixin):
    ## TODO : add tf to the formula, (keep binary countvectorizer for df calculations)
    ## TODO : ngram with skips of a window
    
    def __init__(self, min_cdf=0.05 , **countvectorizerargs):
        
        countvectorizerargs_temp = copy.deepcopy(countvectorizerargs)
        countvectorizerargs_temp['binary'] = True
        self.binaryvectorizer = CountVectorizer(**countvectorizerargs_temp)
        self.min_cdf = min_cdf
        
        pass
    
    def fit(self, X, y):
        
        binary_features = self.binaryvectorizer.fit_transform(X).toarray()
        vocab = self.binaryvectorizer.get_feature_names()
        N = binary_features.shape[0]
        
        binary_features_df = pd.DataFrame(binary_features, columns = vocab)
        binary_features_df['<y>'] = y
        
        class_data = [[],[]]
        for intent, group in binary_features_df.groupby('<y>'):
            class_data[0].append(len(group))
            class_data[1].append(group.drop(columns=['<y>']).sum(axis=0).apply(lambda x: x if x/len(group) > self.min_cdf else 0).values)
        
        self.df = df = np.array(class_data[1]).sum(axis=0)
        
        cdf_idf = []
        for class_count, class_features in zip(*class_data):
            cdf_idf.append( (np.power(10,(class_features / class_count))-1) * np.log( (N - class_count + 1) / (df - class_features +1)) )
        
    
        self.cdf_idf = csr_matrix(np.array(cdf_idf))
        
        return self

    def transform(self, X, y=None):
        
        X = self.binaryvectorizer.transform(X)
        
        row_repeater = csr_matrix(np.ones([X.shape[0],1]))

        def f1(X, cdf_iodf_i):
            nz = np.nonzero(cdf_iodf_i)[1]
            return X[:,nz].multiply(row_repeater * cdf_iodf_i[:,nz])
        X = hstack( [f1(X, cdf_iodf_i) for cdf_iodf_i in self.cdf_idf ] )
        
        return X
    
    def set_params(self, **kwargs):
        self.__init__(**kwargs)
    
    def get_feature_names(self):
        
        feature_names = []
        
        tfv_vocab = np.array(self.binaryvectorizer.get_feature_names())
        
        for idx, cdf_iodf_i in enumerate(self.cdf_idf):
            prefix = "c" + str(idx) + "_"
            nz = np.nonzero(cdf_iodf_i)[1]
            feature_names.extend([prefix + term for term in tfv_vocab[nz]])
        
        feature_names = np.array(feature_names)
        return feature_names
    
    @staticmethod
    def __notes__():
        
        
        
        # class_temp = [{},{}]
        # for intent, group in bf_df.groupby('<y>'):
        #     class_temp[0][intent] = len(group)
        #     class_temp[1][intent] = group.drop(columns=['<y>']).sum(axis=0).apply(lambda x: x if x/len(group) > self.min_cdf else 0).values

        # self.df = df = np.array(list(class_temp[1].values())).sum(axis=0)

        # cdf_iodf = []
        # for class_count, class_features in zip(list(class_temp[0].values()), list(class_temp[1].values())):
        #     cdf_iodf.append( (np.power(10,(class_features / class_count))-1) * np.log( (dc - class_count + 1) / (df - class_features +1)) )




        # class_temp = [{},{}]
        # for intent, group in bf_df.groupby('<y>'):
        #     class_temp[0][intent] = len(group)
        #     class_temp[1][intent] = group.drop(columns=['<y>']).sum(axis=0).apply(lambda x: x if x/len(group) > self.min_cdf else 0).values

        # self.df = df = np.array(list(class_temp[1].values())).sum(axis=0)

        # cdf_iodf = []
        # for i in class_temp[0]:
        #     cdf_iodf.append( (np.power(10,(class_temp[1][i] / class_temp[0][i]))-1) * np.log( (dc - class_temp[0][i] + 1) / (df - class_temp[1][i] +1)) )




        # cdf_dict = {} # intent term document frequency dictionary
        # cdc_dict = {} # intent document count dictionary
        # for intent, group in bf_df.groupby('<y>'):
        #     group_count = len(group)
        #     cdc_dict[intent] = group_count
        #     cdf_dict[intent] = group.drop(columns=['<y>']).sum(axis=0).apply(
        #         lambda x: x if x/group_count > self.min_cdf else 0).values

        # self.df = df = np.array(list(cdf_dict.values())).sum(axis=0)


        # cdf_iodf = []
        # for idx, intent in enumerate(cdf_dict.keys()):
        #     cdf_i = cdf_dict[intent]
        #     cdc_i = cdc_dict[intent]

        #     cdf_iodf_i = (np.power(10,(cdf_i / cdc_i))-1) * np.log( (dc - cdc_i + 1) / (df - cdf_i +1))
        #     cdf_iodf.append(cdf_iodf_i)

        
        #############3
        
        # prefix = np.array(["c"+str(idx)+"_"]*len(nz))
        # feature_names.append(np.char.add(prefix, tfv_vocab[nz]))
            
        # X = hstack(
        #     [
        #         X[:,np.nonzero(cdf_iodf_i)[1]].multiply(
        #         row_repeater* cdf_iodf_i[:,np.nonzero(cdf_iodf_i)[1]])
        #         for cdf_iodf_i in self.cdf_iodf
        #     ]
        # )
        
        # row_count = X.shape[0]
        # row_repeater = csr_matrix(np.ones([row_count,1]))
        # intent_count = self.cdf_iodf.shape[0]
        # intent_repeater = csr_matrix(np.ones([intent_count,1]))
        
        #############################3
        
        # X = self.tf.transform(X).toarray()
        # X = np.array([np.array([X_i*cdf_iodf_i for cdf_iodf_i in self.cdf_iodf]).reshape(-1) for X_i in X])

        # X = scipy.sparse.vstack([ scipy.sparse.csr_matrix( hstack([scipy.sparse.csr_matrix(X_i).multiply(scipy.sparse.csr_matrix(cdf_iodf_i)) for cdf_iodf_i in self.cdf_iodf]).reshape(-1)) for X_i in X])

        # self.cdf_iodf = csr_matrix(self.cdf_iodf)
        # X = vstack([ 
        #     csr_matrix( 
        #         hstack([
        #             X_i.multiply(cdf_iodf_i) 
        #             for cdf_iodf_i in self.cdf_iodf])
        #     ) for X_i in X])


        # cdf_iodf = hstack([row_repeater*cdf_iodf_i for cdf_iodf_i in self.cdf_iodf])
        # X = vstack([(intent_repeater*X_i).reshape(1,-1) for X_i in X])
        # X = X.multiply(cdf_iodf)


        # X = vstack([(intent_repeater*X_i).multiply(self.cdf_iodf).reshape(1,-1) for X_i in X])
        
        
        
        # cargs = {'tokenizer':lambda x:x, 'preprocessor':lambda x:x, 'ngram_range':(1,1), 'min_df':1, }
        # scdfidf = SupervisedCdfidfTransformer(**cargs)
        # scdfidf.fit(df['preprocessed'].values[:n], df['Intent'].values[:n])
        # X = scdfidf.transform(df['preprocessed'].values[:n], df['Intent'].values[:n])
        
        pass
