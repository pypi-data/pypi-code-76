from difflib import SequenceMatcher


class StringAnalysis:

    def __init__(self, string_stream):
        self.string_stream = string_stream

    def get_most_similar_word(self, word):
        scores = list(map(lambda x: SequenceMatcher(None, x, word).ratio(),
                          self.string_stream))
        max_score = max(zip(scores, range(len(scores))))[1]
        return self.string_stream[max_score]
