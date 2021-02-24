# %%
import multiprocessing
from functools import partial


# %%
class xHasimMorphology:
    
    def __init__(self):
        pass
    
    @staticmethod
    def hasim_base_command(text):
        hasim_base_command = """
        """
        return hasim_base_command
    @staticmethod
    def hasim_nll_command(text):
        hasim_nll_command = """
        """
        return hasim_nll_command
    
    @staticmethod
    def parse(text, mode='base'): # mode 'base','nll'
        if(mode == 'base'):
            morph = ! xHasimMorphology.hasim_base_command(text)
        elif(mode == 'nll'):
            morph = ! xHasimMorphology.hasim_nll_command(text)

        tokens = morph.split("\n")
        tokens_subtokens = [token.split('@@@') for token in tokens]
        return tokens_subtokens
    
    @staticmethod
    def parse_list(textlist, mode='base'):
        with multiprocessing.Pool(32) as p:
            result = p.map(partial(xHasimMorphology.parse, mode=mode), textlist)
        return result
    
    @staticmethod
    def tokenize(text, mode='base'):
        tokens_subtokens = xHasimMorphology.parse(text, mode)
        subtokens = []; [subtokens.extend(token_subtokens) for token_subtokens in tokens_subtokens]

        return subtokens
    
    @staticmethod
    def tokenize_list(textlist, mode='base'):
        with multiprocessing.Pool(32) as p:
            result = p.map(partial(xHasimMorphology.tokenize, mode=mode), textlist)
        return result

