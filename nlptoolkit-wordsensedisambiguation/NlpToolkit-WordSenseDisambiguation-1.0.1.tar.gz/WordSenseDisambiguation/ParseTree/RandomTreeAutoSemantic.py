from random import randrange
import random

from AnnotatedSentence.AnnotatedWord import ViewLayerType
from AnnotatedTree.ParseTreeDrawable import ParseTreeDrawable
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode import IsTurkishLeafNode
from AnnotatedTree.Processor.NodeDrawableCollector import NodeDrawableCollector
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.ParseTree.TreeAutoSemantic import TreeAutoSemantic


class RandomTreeAutoSemantic(TreeAutoSemantic):

    __turkishWordNet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm
        self.__turkishWordNet = turkishWordNet

    def autoLabelSingleSemantics(self, parseTree: ParseTreeDrawable) -> bool:
        random.seed(1)
        nodeDrawableCollector = NodeDrawableCollector(parseTree.getRoot(), IsTurkishLeafNode())
        leafList = nodeDrawableCollector.collect()
        for i in range(len(leafList)):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, leafList, i)
            if len(synSets) > 0:
                leafList[i].getLayerInfo().setLayerData(ViewLayerType.SEMANTICS, synSets[randrange(len(synSets))].getId())
        return True
