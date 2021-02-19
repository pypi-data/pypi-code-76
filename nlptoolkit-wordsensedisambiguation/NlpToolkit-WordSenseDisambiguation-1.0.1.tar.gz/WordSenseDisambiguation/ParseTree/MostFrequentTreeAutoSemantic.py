from AnnotatedSentence.AnnotatedWord import ViewLayerType
from AnnotatedTree.ParseTreeDrawable import ParseTreeDrawable
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode import IsTurkishLeafNode
from AnnotatedTree.Processor.NodeDrawableCollector import NodeDrawableCollector
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.SynSet import SynSet
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.ParseTree.TreeAutoSemantic import TreeAutoSemantic


class MostFrequentTreeAutoSemantic(TreeAutoSemantic):

    __turkishWordNet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm
        self.__turkishWordNet = turkishWordNet

    def mostFrequent(self, synSets: list, root: str) -> SynSet:
        if len(synSets) == 1:
            return synSets[0]
        minSense = 50
        best = None
        for synSet in synSets:
            for i in range(synSet.getSynonym().literalSize()):
                if synSet.getSynonym().getLiteral(i).getName().lower().startswith(root) or synSet.getSynonym().getLiteral(i).getName().lower().endswith(" " + root):
                    if synSet.getSynonym().getLiteral(i).getSense() < minSense:
                        minSense = synSet.getSynonym().getLiteral(i).getSense()
                        best = synSet
        return best

    def autoLabelSingleSemantics(self, parseTree: ParseTreeDrawable) -> bool:
        nodeDrawableCollector = NodeDrawableCollector(parseTree.getRoot(), IsTurkishLeafNode())
        leafList = nodeDrawableCollector.collect()
        for i in range(len(leafList)):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, leafList, i)
            if len(synSets) > 0:
                best = self.mostFrequent(synSets, leafList[i].getLayerInfo().getMorphologicalParseAt(0).getWord().getName())
                if best is not None:
                    leafList[i].getLayerInfo().setLayerData(ViewLayerType.SEMANTICS, best.getId())
        return True
