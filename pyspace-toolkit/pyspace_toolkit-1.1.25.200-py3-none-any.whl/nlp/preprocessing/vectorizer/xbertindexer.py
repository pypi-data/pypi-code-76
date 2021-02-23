from pytorch_pretrained_bert.tokenization import BertTokenizer


# +
class xBertIndexer:
    
    def __init__(self, vocabfile, max_len=None, do_lower_case=False):
        if(vocabfile in ['bert-base-uncased', 'bert-large-uncased', 'bert-base-cased', 'bert-large-cased', 'bert-base-multilingual-uncased', 'bert-base-multilingual-cased']):
            if(max_len != None):
                berttokenizer = BertTokenizer.from_pretrained(vocabfile, max_len=max_len)
            else:
                berttokenizer = BertTokenizer.from_pretrained(vocabfile)
        else:
            if(max_len != None):
                berttokenizer = BertTokenizer(vocabfile, do_lower_case=do_lower_case, max_len=max_len)
            else:
                berttokenizer = BertTokenizer(vocabfile, do_lower_case=do_lower_case)

        self.berttokenizer = berttokenizer
        
    def convert_tokenized(self, tokenized):
        return self.berttokenizer.convert_tokens_to_ids(tokenized)
    
    def convert_tokenizedlist(self, tokenizedlist):
        return [self.convert_tokenized(tokenized) for tokenized in tokenizedlist]
    
    def inverse_tokenized(self, tokenized):
        return self.berttokenizer.convert_ids_to_tokens(tokenized)
    
    def inverse_tokenizedlist(self, tokenizedlist):
        return [self.inverse_tokenized(tokenized) for tokenized in tokenizedlist]
    
    
    
