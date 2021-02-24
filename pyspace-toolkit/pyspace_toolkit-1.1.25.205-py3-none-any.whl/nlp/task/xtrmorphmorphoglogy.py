import multiprocessing


class xTrmorphMorphology:
    
    def __init__(self):
        pass
    
    @staticmethod
    def trmorph_command(text):
        trmorph_command = """
        """
        return trmorph_command
    
    @staticmethod
    def parse(text):
        morph = ! xTrmorphMorphology.trmorph_command(text)

        tokens = morph.split("\n")
        tokens_subtokens = [token.split('@@@') for token in tokens]
        return tokens_subtokens
    
    @staticmethod
    def parse_list(textlist):
        with multiprocessing.Pool(32) as p:
            result = p.map(xTrmorphMorphology.parse, textlist)
        return result
    
    @staticmethod
    def tokenize(text):
        tokens_subtokens = xTrmorphMorphology.parse(text, mode)
        subtokens = []; [subtokens.extend(token_subtokens) for token_subtokens in tokens_subtokens]

        return subtokens
    
    @staticmethod
    def tokenize_list(textlist):
        with multiprocessing.Pool(32) as p:
            result = p.map(xTrmorphMorphology.tokenize, textlist)
        return result

