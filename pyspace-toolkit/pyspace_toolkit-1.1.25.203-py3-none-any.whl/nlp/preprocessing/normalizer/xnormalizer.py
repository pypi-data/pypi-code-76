# %%
try:
    from icu import UnicodeString, Locale
    pyicu_bool = True
except:
    pyicu_bool = False
    
import unicodedata
import multiprocessing
import re


# %%
class xNormalizer():
    
    def __init__(self):
        pass
    
    @staticmethod
    def lower(text, lang="EN"): # "TR"
        # if pyicu_bool:
        #     langlocale = Locale(lang)
        #     result = UnicodeString(text)
        #     result = result.toLower(langlocale)

        result = text
        if lang == "TR":
            result = result.replace('İ', 'i')
            result = result.replace('I', 'ı')

        result = result.lower()

        return result

    @staticmethod
    def upper(text, lang="EN"): # "TR"
        
        text = result
        if lang == "TR":
            result = result.replace( 'i', 'İ',)
            result = result.replace('ı', 'I',)

        result = result.upper()
        return result
    
    @staticmethod
    def is_control(char):
        
        # \t, \n and \r are counted as whitespace
        if char == "\t" or char == "\n" or char == "\r":
            return False
    
        cat = unicodedata.category(char)
        if cat.startswith("C"):
            return True
        return False
    
    @staticmethod
    def is_whitespace(char):
        
        # \t, \n and \r are counted as whitespace
        if char == " " or char == "\t" or char == "\n" or char == "\r":
            return True
        cat = unicodedata.category(char)
        if cat == "Zs":
            return True
        return False
    
    @staticmethod
    def clean_text_backup(text):
        output = []
        for char in text:
            cp = ord(char)
            if cp == 0 or cp == 0xfffd or xNormalizer.is_control(char):
                continue
            if xNormalizer.is_whitespace(char):
                output.append(" ")
            else:
                output.append(char)
                
        result = "".join(output).strip()
        result = re.sub("[ ]+", " ", result)
        return result

    @staticmethod
    def clean_text(text, return_replace_patterns=False):

        replace_patterns = []

        output = []
        for idx, char in enumerate(text):
            cp = ord(char)
            if cp == 0 or cp == 0xfffd or xNormalizer.is_control(char):
                replace_patterns.append((char, ""))
                continue

            if xNormalizer.is_whitespace(char):
                replace_patterns.append((char, " "))
                output.append(" ")

            else:
                output.append(char)

                
        result = "".join(output).strip()
        replace_patterns.append(("^[ ]+", ""))
        replace_patterns.append(("[ ]+$", ""))


        result = re.sub("[ ][ ]+", " ", result)
        replace_patterns.append(("[ ][ ]+", " "))


        # replace_patterns = list(set(replace_patterns))
        replace_patterns = [ v for (i,v) in enumerate(replace_patterns) if v not in replace_patterns[0:i] ]
        replace_patterns = [p for p in replace_patterns if p[0] != p[1]]

        if return_replace_patterns:
            return result, replace_patterns
        else:
            return result
    
    @staticmethod
    def clean_textlist(textlist):
        with multiprocessing.Pool(32) as p:
            textlist = p.map(xNormalizer.clean_text, textlist)
        return textlist

    @staticmethod
    def tr_normalize(word):
        
        tr_unicode_normalize = {
            'ü':'u',
            'Ü':'U',
            'ç':'c',
            'Ç':'C',
            'ş':'s',
            'Ş':'S',
            'ı':'i',
            'İ':'I',
            'ğ':'g',
            'Ğ':'G',
            'ö':'o',
            'Ö':'O',
        }

        for k, v in tr_unicode_normalize.items():
            word = word.replace('\\'+k, v).replace(k, v)
            
        # word = word.lower()
        return word