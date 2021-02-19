from random import randrange
import random

from AnnotatedSentence.AnnotatedSentence import AnnotatedSentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.SynSet import SynSet
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.Sentence.SentenceAutoSemantic import SentenceAutoSemantic


class Lesk(SentenceAutoSemantic):

    __turkishWordNet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__turkishWordNet = turkishWordNet
        self.__fsm = fsm

    def intersection(self, synSet: SynSet, sentence: AnnotatedSentence) -> int:
        if synSet.getExample() is not None:
            words1 = (synSet.getLongDefinition() + " " + synSet.getExample()).split(" ")
        else:
            words1 = synSet.getLongDefinition().split(" ")
        words2 = sentence.toString().split(" ")
        count = 0
        for word1 in words1:
            for word2 in words2:
                if word1.lower() == word2.lower():
                    count = count + 1
        return count

    def autoLabelSingleSemantics(self, sentence: AnnotatedSentence) -> bool:
        random.seed(1)
        done = False
        for i in range(sentence.wordCount()):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, sentence, i)
            maxIntersection = -1
            for j in range(len(synSets)):
                synSet = synSets[j]
                intersectionCount = self.intersection(synSet, sentence)
                if intersectionCount > maxIntersection:
                    maxIntersection = intersectionCount
            maxSynSets = []
            for j in range(len(synSets)):
                synSet = synSets[j]
                if self.intersection(synSet, sentence) == maxIntersection:
                    maxSynSets.append(synSet)
            if len(maxSynSets) > 0:
                done = True
                sentence.getWord(i).setSemantic(maxSynSets[randrange(len(maxSynSets))].getId())
        return done

