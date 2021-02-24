# %%
if(__name__ == "__main__"):
    import sys
    sys.path.append("../../../")
else:
    import sys
    pyspacepath = "/".join(__file__.split("/")[:-4])
    sys.path.append(pyspacepath)

# %%
from pyspace.nlp.preprocessing.tokenizer.xspacytokenizer import xSpacyTokenizer

import spacy


# %%
class xSpacy:
    
    def __init__(self):
        self.spacynlp = spacy.load('en_core_web_sm')
        self.spacynlp.tokenizer = xSpacyTokenizer.create_spacytokenizer()
        
    def pipe_text(self, text):
        return self.spacynlp(text)
    
    def pipe_textlist(self, textlist):
        return list(self.spacynlp.pipe(textlist))
        
    def pipe_tokenized(self, tokenized, pipeline=["tagger","parser","ner"]):
        doc = spacy.tokens.doc.Doc(self.spacynlp.vocab, words=tokenized)
        
        for name,proc in self.spacynlp.pipeline:
            if name in pipeline:
                doc = proc(doc)
        
        return doc
    
    def pipe_tokenizedlist(self, tokenizedlist, pipeline=["tagger","parser","ner"]):
        docs = [spacy.tokens.doc.Doc(self.spacynlp.vocab, words=tokenized) for tokenized in tokenizedlist]
        
        for name,proc in self.spacynlp.pipeline:
            if name in pipeline:
                docs = list(self.spacynlp.pipe(docs))
        
        return docs
        
    @staticmethod
    def get_attr(doc, attr):
        if(hasattr(doc[0],attr+'_')):
            attr = attr+'_'
        elif(hasattr(doc[0],attr)):
            pass
        else:
            raise Exception("No such attr in spacy doc")
            
        return [getattr(token, attr) for token in doc]

# %%
# nlp = spacy.blank('tr')# nlp()
# doc = spacy.tokens.doc.Doc(nlp.vocab, words=series.sum())

# iter_idx = 0

# for row in series.values[:-1]:
#     iter_idx += len(row)
#     doc[iter_idx].sent_start = True
#     doc[iter_idx-1].pos_ = 'PUNCT'

# doc.is_parsed = True

# %%
# xspacy = xSpacy()
# text1 = "This is my first trial."
# text2 = "The second one is cool."
# list1 = [text1, text2]
# docs = xspacy.pipe_textlist(list1)
# type(docs[0]) # spacy.tokens.doc.Doc
# xspacy.get_attr(docs[0],'pos') # ['DET', 'AUX', 'PRON', 'ADJ', 'NOUN', 'PUNCT']
