# +
import spacy

import benepar
from benepar.spacy_plugin import BeneparComponent


# +
class xBeneparConstituency: # https://github.com/udnaan/self-attentive-parser
    
    def __init__(self):
        self.spacynlp = spacy.load("en_core_web_sm")
        self.spacytagger = self.spacynlp.pipeline[0][1]
        
        self.benepar = BeneparComponent("benepar_en2")
        self.benepar_wout_tagger = BeneparComponent("benepar_en2", disable_tagger=True)
        
    def parse_tokenized_constituency(self, tokenized, tagger="benepar"):
        
        if(len(tokenized) <= 1):
            raise Exception("Tokenized input length 1 is not valid.")
            
        doc = spacy.tokens.doc.Doc(self.spacynlp.vocab, words=tokenized)
        
        # doc.is_parsed = True
        for token in doc:
            token.is_sent_start = False
        doc[0].is_sent_start = True
        # doc[0].sent_start = True
        
        if(tagger == "benepar"):
            doc = self.benepar(doc)
        elif(tagger == "spacy"):
            doc = self.spacytagger(doc)
            doc = self.benepar_wout_tagger(doc)
            
        sent_span = list(doc.sents)[0]
        
        return sent_span
    
    @staticmethod
    def get_attr(spans, attr):
        
        if(attr == 'labels'):
            return [s._.labels[0] if s._.labels != () else s[0].pos_ for s in spans]

        elif(attr == 'children'):
            span = spans
            return list(span._.children)
        
        elif(attr == 'grandchildren'):
            span = spans
            childspans = list(span._.children)
            
            result = []
            for cs in childspans:
                temp = xBeneparConstituency.get_attr(cs, 'children')
                if(temp != []):
                    result += temp
                else:
                    result.append(cs)
                    
            return result
        
        elif(attr == 'phrases'):
            span = spans
            childspans = list(span._.children)
            
            result = []
            for cs in childspans:
                temp = xBeneparConstituency.get_attr(cs, 'children')
                
                if(temp != [] and len(temp) != 1 and cs._.labels[0] not in ["NP"]):
                    result += temp
                else:
                    result.append(cs)
            return result
        
            
