import random

from AnnotatedSentence.AnnotatedSentence import AnnotatedSentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.Sentence.SentenceAutoSemantic import SentenceAutoSemantic


class RandomSentenceAutoSemantic(SentenceAutoSemantic):

    __turkishWordNet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__turkishWordNet = turkishWordNet
        self.__fsm = fsm

    def autoLabelSingleSemantics(self, sentence: AnnotatedSentence) -> bool:
        random.seed(1)
        for i in range(sentence.wordCount()):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, sentence, i)
            if len(synSets) > 0:
                sentence.getWord(i).setSemantic(synSets[random.randrange(len(synSets))].getId())
        return True
