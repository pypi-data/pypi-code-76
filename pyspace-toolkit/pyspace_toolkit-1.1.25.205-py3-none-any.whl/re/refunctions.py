
import re
import string

from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

def convert_list_to_regex(input_list, lang='tr', ignorcase=True, wordboundary=True):
    out = [re.escape(t) for t in input_list]
    out = "|".join(out)
    out = f"({out})"


    if lang == 'tr' and ignorcase and wordboundary:
        out = xNormalizer.tr_normalize(out).lower()

        _ignorecase = """(?i)"""
        _wrap_start = """("""
        _wb_start = """\\b"""

        _wb_end ="""\\b"""
        _wrap_end = """)"""

        out = f"""{_ignorecase}{_wrap_start}{_wb_start}{out}{xRegex.apostrophe}{xRegex.tr_cekim_eki}{_wb_end}{_wrap_end}"""

    return out

class xRegex:

    apostrophe = """['"]{0,1}"""

    tr_kaynastirma = """([yşsn]){0,1}"""
    tr_kaynastirma_hal = """([ys]){0,1}"""
    tr_kaynastirma_tamlama = """([n]){0,1}"""
    tr_kaynastirma_yuklem = """([y]){0,1}"""

    tr_i_hal_eki = f"""({tr_kaynastirma_hal}[iıuü])"""
    tr_e_hal_eki = f"""({tr_kaynastirma_hal}[ae])"""
    tr_de_hal_eki = """([dt][ae])"""
    tr_den_hal_eki = """([dt][ae]n)"""
    tr_hal_eki = f"""({tr_i_hal_eki}|{tr_e_hal_eki}|{tr_de_hal_eki}|{tr_den_hal_eki})"""

    tr_tamlama_eki = f"""({tr_kaynastirma_tamlama}[iıuü]n)"""

    tr_cogul_eki = """(l[ae]r)"""
    tr_ki_ilgi_eki = """(k[iü])"""
    tr_ek_eylem_eki = f"""(d[iıuü]r|{tr_kaynastirma_yuklem}(d[iıuü]|m[iıuü][şs]))"""

    tr_ilgi_eki = """([iı]{0,1}[mn]([iı]z){0,1})"""
    
    tr_cekim_eki = f"""({tr_cogul_eki}{{0,1}}{tr_ilgi_eki}{{0,1}}{tr_hal_eki}{{0,1}}{tr_ki_ilgi_eki}{{0,1}}{tr_tamlama_eki}{{0,1}}{tr_ek_eylem_eki}{{0,1}})"""
    # tr_cekim_eki = """(l[ae]r){0,1}(n{0,1}[iıuü]n|d[ae]n{0,1}|y{0,1}[ae]){0,1}(ki){0,1}"""