# %%
import pyspace_resources

# %%
from typing import List

try:
    from jpype import JClass, JString, getDefaultJVMPath, java, shutdownJVM, startJVM
except:
    pass
ZEMBEREK_PATH: str = pyspace_resources.__path__[0] + '/zemberek/bin/zemberek-full.jar'


# %%
class JVMController:
    __instance = None
    
    @staticmethod 
    def start():
        """ Static access method. """
        if JVMController.__instance == None:
            
            startJVM(
                getDefaultJVMPath(),
                '-ea',
                f'-Djava.class.path={ZEMBEREK_PATH}',
                convertStrings=False
            )
            JVMController.__instance = 1
    
    @staticmethod
    def stop():
        
        if JVMController.__instance != None:
            shutdownJVM()
            

            JVMController.__instance = None
    
JVMController.start()

# %%
Paths: JClass = JClass('java.nio.file.Paths')
    
TurkishTokenizer: JClass = JClass('zemberek.tokenization.TurkishTokenizer')
Token: JClass = JClass('zemberek.tokenization.Token')

TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
WordAnalysis: JClass = JClass('zemberek.morphology.analysis.WordAnalysis')
    
TurkishSentenceNormalizer: JClass = JClass('zemberek.normalization.TurkishSentenceNormalizer')

TurkishSpellChecker: JClass = JClass('zemberek.normalization.TurkishSpellChecker')

# %%
zemberek_tokenizer_v0: TurkishTokenizer = TurkishTokenizer.DEFAULT
zemberek_tokenizer_v1: TurkishTokenizer = TurkishTokenizer \
    .builder() \
    .ignoreTypes(
        Token.Type.Punctuation,
        Token.Type.NewLine,
        Token.Type.SpaceTab
    ).build()

zemberek_morphology: TurkishMorphology = TurkishMorphology.createWithDefaults()


# %%
normalizer = TurkishSentenceNormalizer(
        TurkishMorphology.createWithDefaults(),
        Paths.get(pyspace_resources.__path__[0] + '/zemberek/data/normalization'),
        Paths.get(pyspace_resources.__path__[0] + '/zemberek/data/lm/lm.2gram.slm'),
    )

# spell_checker: TurkishSpellChecker = TurkishSpellChecker(TurkishMorphology.createWithDefaults())
spell_checker = TurkishSpellChecker(TurkishMorphology.createWithDefaults())


# %%
def normalize(sentence):
    
    result = normalizer.normalize(JString(sentence))
    result = str(result)
    
    return result


# %%
def lemmatize(word):
    
    results: WordAnalysis = zemberek_morphology.analyze(JString(word))
        
    if len(list(results)):
        return str(list(results)[0].getLemmas()[0])
    else:
        return word



# %%

def tokenize(text, mode =0):
    
    if(mode == 0):
        zemberek_tokenizer = zemberek_tokenizer_v0
    elif(mode == 1):
        zemberek_tokenizer = zemberek_tokenizer_v1
    
    tokens = zemberek_tokenizer.tokenizeToStrings(JString(text))
    tokens = [str(token) for token in tokens]
    
    return tokens
