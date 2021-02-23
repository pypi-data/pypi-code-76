import multiprocessing

import spacy
from spacy.tokenizer import Tokenizer as SpacyTokenizer


class xSpacyTokenizer:
    
    def __init__(self):
        spacynlp = spacy.load('en_core_web_sm')
        spacynlp.tokenizer = xSpacyTokenizer.create_spacytokenizer()
        self.spacynlp = spacynlp
        
    def tokenize(self, text):
        result = [t.text for t in self.spacynlp.tokenizer(text)]
        return result
    
    def tokenize_list(self, textlist):
        # next statement has better performance than spacynlp.tokenizer.pipe, almost same
        result = [[t.text for t in self.spacynlp.tokenizer(text)] for text in textlist]
        return result
    
    def tokenize_sent(self, paragraph):
        spacydoc = self.spacynlp(paragraph)
        result = []
        sent = []
        
        for token in spacydoc:
            if(token.is_sent_start):
                result.append(sent)
                sent = []
            sent.append(token.text)
        if(sent != []):
            result.append(sent)
            
        return result
    
    # TODO
    def tokenize_sent_list(self, paragraphlist):
        result = []
        return result
    
    @staticmethod
    def create_spacytokenizer():
        def create_custom_tokenizer(nlp):

            my_prefix = r'[0-9]\.'

            all_prefixes_re = spacy.util.compile_prefix_regex(tuple(list(nlp.Defaults.prefixes) + [my_prefix]))

            ## custom_infixes = ['\.\.\.+', '-', '\+', ',(?=\[)', '\.(?=\[)', ',(?=\()', '\.(?=\()', '[\[\]!:$()]']
            # Handle ( that doesn't have proper spacing around it
            custom_infixes = ['\.\.\.+', '(?<=[0-9])-(?=[0-9])', '[!&:,()]']
            infix_re = spacy.util.compile_infix_regex(tuple(list(nlp.Defaults.infixes) + custom_infixes))

            suffix_re = spacy.util.compile_suffix_regex(nlp.Defaults.suffixes)   

            return SpacyTokenizer(nlp.vocab, nlp.Defaults.tokenizer_exceptions,
                             prefix_search = all_prefixes_re.search, 
                             infix_finditer = infix_re.finditer, suffix_search = suffix_re.search,
                             token_match=None)
        
        
        nlp = spacy.load('en_core_web_sm')
        # nlp.tokenizer = custom_tokenizer(nlp)
        spacytokenizer = create_custom_tokenizer(nlp)
        return spacytokenizer

