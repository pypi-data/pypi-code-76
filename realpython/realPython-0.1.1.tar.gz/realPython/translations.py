from translate import Translator

def translate(text, from_lang, to_lang):
    translator= Translator(to_lang=str(to_lang), from_lang=str(from_lang))
    translation = translator.translate(str(text))
    print(translation)