#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
import re
import pymorphy2


words_pattern = re.compile(r'[\w\-]+')


def words_iterator(text):
    for w in words_pattern.findall(text):
        yield w


class Pymorphy2Processor:
    parse = pymorphy2.MorphAnalyzer().parse

    def parse_names(self, text):
        """Метод ищет в тексте все имена."""
        parse = self.parse
        # probability score threshold
        prob_thresh = 0.4
        L = []
        for word in words_iterator(text):
            for p in parse(word):
                if 'Name' in p.tag and p.score >= prob_thresh:
                    L.append(p.normal_form)
                    break
                elif 'Patr' in p.tag and p.score >= prob_thresh:
                    L.append(word)
                    break
        return L
