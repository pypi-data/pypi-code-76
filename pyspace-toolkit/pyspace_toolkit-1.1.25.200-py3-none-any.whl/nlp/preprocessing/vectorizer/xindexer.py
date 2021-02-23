# %%
import pytorch_pretrained_bert

from tensorflow.keras.preprocessing.text import Tokenizer as KerasTokenizer


# %%
# xIdxVectorizer, xIndexer
class xIndexer:
    
    def __init__(self, xtype = 'pre', xinput = None): # xtype 'pre', 'fit'
        
        if(xtype == 'pre'):
            self.vocab = pytorch_pretrained_bert.tokenization.load_vocab(xinput)
            
        elif(xtype == 'scratch'):
            
            # default filters value is all punctuation
            # do not remove them
            kerastokenizer = KerasTokenizer(filters='')
            # keras do not assign any word with index 0
            # index 0 is a reserved index that won't be assigned to any word
            # PAD, UNKNOWN values - 0, word_count+1
            # xinput - tokenizedlist
            kerastokenizer.fit_on_texts(xinput)
            
            self.vocab = kerastokenizer.word_index
            self.vocab["[PAD]"] = 0
            self.vocab["[UNK]"] = len(self.vocab)            
            self.vocab["[CLS]"] = len(self.vocab)            
            self.vocab["[SEP]"] = len(self.vocab)
            
        self.inv_vocab = dict(zip(self.vocab.values(), self.vocab.keys()))
        
    def convert_tokenized(self, tokenized):
        result = []
        for token in tokenized:
            try:
                result.append(self.vocab[token])
            except Exception as e:
                result.append(self.vocab["[UNK]"])
        return result
    
    def convert_tokenizedlist(self, tokenizedlist):
        return [self.convert_tokenized(tokenized) for tokenized in tokenizedlist]
    
    def inverse_tokenized(self, tokenized):
        return [self.inv_vocab[idx] for idx in tokenized]
    
    def inverse_tokenizedlist(self, tokenizedlist):
        return [self.inverse_tokenized(tokenized) for tokenized in tokenizedlist]

