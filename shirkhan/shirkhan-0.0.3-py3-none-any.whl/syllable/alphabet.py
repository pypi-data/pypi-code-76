"""
elipbe   字母表  alphabet
suzuq -> 元音 -> vowels
vzvk  -> 辅音 -> consonant
"""


class Alphabet:
    """
    elipbe   字母表  alphabet

    suzuq -> 元音 -> vowels

    vzvk  -> 辅音 -> consonant

    table

    HEMZE
    """

    HEMZE = "ئ‍"
    """
    [0] uy   母语字符
    [1] replacement 替代词[转码处理时可以参考]
    [2] is_vowels 是否元音
    """
    table = {
        "ئ": ("ئ", "^", 0), # 因分音节考虑 暂定为辅音
        "ا": ("ا", "a", 1),
        "ە": ("ە", "1", 1),
        "ې": ("ې", "e", 1),
        "ى": ("ى", "i", 1),
        "و": ("و", "o", 1),
        "ۇ": ("ۇ", "u", 1),
        "ۆ": ("ۆ", "2", 1),
        "ۈ": ("ۈ", "v", 1),
        "ب": ("ب", "b", 0),
        "پ": ("پ", "p", 0),
        "ت": ("ت", "t", 0),
        "ج": ("ج", "j", 0),
        "چ": ("چ", "q", 0),
        "خ": ("خ", "h", 0),
        "د": ("د", "d", 0),
        "ر": ("ر", "r", 0),
        "ز": ("ز", "z", 0),
        "ژ": ("ژ", "3", 0),
        "س": ("س", "s", 0),
        "ش": ("ش", "x", 0),
        "غ": ("غ", "4", 0),
        "ق": ("ق", "5", 0),
        "ف": ("ف", "f", 0),
        "ك": ("ك", "k", 0),
        "گ": ("گ", "g", 0),
        "ڭ": ("ڭ", "6", 0),
        "ل": ("ل", "l", 0),
        "م": ("م", "m", 0),
        "ن": ("ن", "n", 0),
        "ھ": ("ھ", "7", 0),
        "ۋ": ("ۋ", "w", 0),
        "ي": ("ي", "y", 0),
    }

    @staticmethod
    def alpha_info(alpha: str):
        table = Alphabet.table
        if alpha in table:
            return table.get(alpha)
        else:
            return None

    @staticmethod
    def is_vowels(alpha: str):
        info = Alphabet.alpha_info(alpha)
        if info is None:
            return info
        return info[2]


if __name__ == '__main__':
    pass
