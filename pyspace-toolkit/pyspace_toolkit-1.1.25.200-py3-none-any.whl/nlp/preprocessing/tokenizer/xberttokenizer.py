from pytorch_pretrained_bert.tokenization import BertTokenizer


# +
class xBertTokenizer:
    
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
        
    def tokenize(self, text):
        result = self.berttokenizer.tokenize(text)
        return result
    
    
