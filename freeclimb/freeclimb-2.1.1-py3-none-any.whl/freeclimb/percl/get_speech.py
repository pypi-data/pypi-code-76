class GrammarType:
    URL = 'URL'
    BULTIN = 'BUILTIN'


class BuiltInGrammar:
    ALPHANUM6 = 'ALPHANUM6'
    ANY_DIG = 'ANY_DIG'
    DIG1 = 'DIG1'
    DIG2 = 'DIG2'
    DIG3 = 'DIG3'
    DIG4 = 'DIG4'
    DIG5 = 'DIG5'
    DIG6 = 'DIG6'
    DIG7 = 'DIG7'
    DIG8 = 'DIG8'
    DIG9 = 'DIG9'
    DIG10 = 'DIG10'
    DIG11 = 'DIG11'
    UP_TO_20_DIGIT_SEQUENCE = 'UP_TO_20_DIGIT_SEQUENCE'
    VERSAY_YESNO = 'VERSAY_YESNO'


class GetSpeech(dict):

    __cmd = 'GetSpeech'

    def __init__(self, action_url):
        super().__init__()
        self.__setitem__(GetSpeech.__cmd, {})
        self.action_url(action_url)

    def action_url(self, action_url):
        self.__getitem__(GetSpeech.__cmd)['actionUrl'] = action_url
        return self

    def grammar_type(self, grammar_type):
        self.__getitem__(GetSpeech.__cmd)['grammarType'] = grammar_type
        return self

    def grammar_file(self, grammar_file):
        self.__getitem__(GetSpeech.__cmd)['grammarFile'] = grammar_file
        return self

    def grammar_rule(self, grammar_rule):
        self.__getitem__(GetSpeech.__cmd)['grammarRule'] = grammar_rule
        return self

    def play_beep(self, play_beep):
        self.__getitem__(GetSpeech.__cmd)['playBeep'] = play_beep
        return self

    def no_input_timeout_ms(self, no_input_timeout_ms):
        self.__getitem__(GetSpeech.__cmd)['noInputTimeoutMs'] = no_input_timeout_ms
        return self

    def recognition_timeout_ms(self, recognition_timeout_ms):
        self.__getitem__(GetSpeech.__cmd)['recognitionTimeoutMs'] = recognition_timeout_ms
        return self

    def confidence_threshold(self, confidence_threshold):
        self.__getitem__(GetSpeech.__cmd)['confidenceThreshold'] = confidence_threshold
        return self

    def sensitivity_level(self, sensitivity_level):
        self.__getitem__(GetSpeech.__cmd)['sensitivityLevel'] = sensitivity_level
        return self

    def speech_complete_timeout_ms(self, speech_complete_timeout_ms):
        self.__getitem__(GetSpeech.__cmd)['speechCompleteTimeoutMs'] = speech_complete_timeout_ms
        return self

    def speech_incomplete_timeout_ms(self, speech_incomplete_timeout_ms):
        self.__getitem__(GetSpeech.__cmd)['speechIncompleteTimeoutMs'] = speech_incomplete_timeout_ms
        return self

    def prompts(self, prompt):
        if 'prompts' not in self.__getitem__(GetSpeech.__cmd):
            self.__getitem__(GetSpeech.__cmd)['prompts'] = []
        self.__getitem__(GetSpeech.__cmd)['prompts'].append(prompt)
        return self

    def enforcePCI(self, enforcePCI):
        self.__getitem__(GetDigits.__cmd)['enforcePCI'] = enforcePCI
        return self
