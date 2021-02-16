class SayLanguage:
    ca_es = catalan_spain = "ca-ES"
    da_dk = danish_denmark = "da-DK"
    de_de = german_germany = "de-DE"
    en_au = english_australia = "en-AU"
    en_ca = english_canada = "en-CA"
    en_gb = english_united_kingdom = "en-GB"
    en_in = english_india = "en-IN"
    en_us = english_united_states = "en-US"
    es_es = english_spain = "es-ES"
    es_mx = english_mexico = "es-MX"
    fi_fi = finnish_finland = "fi-FI"
    fr_ca = french_canada = "fr-CA"
    fr_fr = french_france = "fr-FR"
    it_it = italian_italy = "it-IT"
    ja_jp = japanese_japan = "ja-JP"
    ko_kr = korean_korea = "ko-KR"
    nb_no = norwegian_norway = "nb-NO"
    nl_nl = dutch_netherlands = "nl-NL"
    pl_pl = polish_poland = "pl-PL"
    pt_br = portugese_brazil = "pt-BR"
    pt_pt = portugese_portugal = "pt-PT"
    ru_ru = russian_russia = "ru-RU"
    sv_se = swedish_sweden = "sv-SE"
    zh_cn = chinese_china = "zh-CN"
    zh_hk = chinese_hong_kong = "zh-HK"
    zh_tw = chinese_taiwan = "zh-TW"


class Say(dict):

    __cmd = 'Say'

    def __init__(self, text):
        super().__init__()
        self.__setitem__(Say.__cmd, {})
        self.text(text)

    def text(self, text):
        self.__getitem__(Say.__cmd)['text'] = text
        return self

    def loop(self, loop):
        self.__getitem__(Say.__cmd)['loop'] = loop
        return self

    def language(self, language):
        self.__getitem__(Say.__cmd)['language'] = language
        return self

    def conference_id(self, conference_id):
        self.__getitem__(Say.__cmd)['conferenceId'] = conference_id
        return self

    def enforcePCI(self, enforcePCI):
        self.__getitem__(Say.__cmd)['enforcePCI'] = enforcePCI
        return self
