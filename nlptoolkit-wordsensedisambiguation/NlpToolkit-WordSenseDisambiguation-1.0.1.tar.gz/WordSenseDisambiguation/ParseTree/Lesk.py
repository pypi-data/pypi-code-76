from random import randrange
import random

from AnnotatedSentence.AnnotatedWord import ViewLayerType
from AnnotatedTree.ParseTreeDrawable import ParseTreeDrawable
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode import IsTurkishLeafNode
from AnnotatedTree.Processor.NodeDrawableCollector import NodeDrawableCollector
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.SynSet import SynSet
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.ParseTree.TreeAutoSemantic import TreeAutoSemantic


class Lesk(TreeAutoSemantic):

    __turkishWordNet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm
        self.__turkishWordNet = turkishWordNet

    def intersection(self, synSet: SynSet, leafList: list) -> int:
        if synSet.getExample() is not None:
            words1 = (synSet.getLongDefinition() + " " + synSet.getExample()).split(" ")
        else:
            words1 = synSet.getLongDefinition().split(" ")
        words2 = []
        for i in range(len(leafList)):
            words2.append(leafList[i].getLayerData(ViewLayerType.TURKISH_WORD))
        count = 0
        for word1 in words1:
            for word2 in words2:
                if word1.lower() == word2.lower():
                    count = count + 1
        return count

    def autoLabelSingleSemantics(self, parseTree: ParseTreeDrawable) -> bool:
        random.seed(1)
        nodeDrawableCollector = NodeDrawableCollector(parseTree.getRoot(), IsTurkishLeafNode())
        leafList = nodeDrawableCollector.collect()
        done = False
        for i in range(len(leafList)):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, leafList, i)
            maxIntersection = -1
            for j in range(len(synSets)):
                synSet = synSets[j]
                intersectionCount = self.intersection(synSet, leafList)
                if intersectionCount > maxIntersection:
                    maxIntersection = intersectionCount
            maxSynSets = []
            for j in range(len(synSets)):
                synSet = synSets[j]
                if self.intersection(synSet,leafList) == maxIntersection:
                    maxSynSets.append(synSet)
            if len(maxSynSets) > 0:
                leafList[i].getLayerInfo().setLayerData(ViewLayerType.SEMANTICS, maxSynSets[randrange(len(maxSynSets))].getId())
                done = True
        return done
