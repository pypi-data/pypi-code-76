from abc import abstractmethod

from AnnotatedTree.ParseTreeDrawable import ParseTreeDrawable
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.WordNet import WordNet


class TreeAutoSemantic:

    @abstractmethod
    def autoLabelSingleSemantics(self, parseTree: ParseTreeDrawable) -> bool:
        pass

    def getCandidateSynSets(self, wordNet: WordNet, fsm: FsmMorphologicalAnalyzer, leafList: list, index: int) -> list:
        twoPrevious = None
        previous = None
        twoNext = None
        next = None
        current = leafList[index].getLayerInfo()
        if index > 1:
            twoPrevious = leafList[index - 2].getLayerInfo()
        if index > 0:
            previous = leafList[index - 1].getLayerInfo()
        if index != len(leafList) - 1:
            next = leafList[index + 1].getLayerInfo()
        if index < len(leafList) - 2:
            twoNext = leafList[index + 2].getLayerInfo()
        synSets = wordNet.constructSynSets(current.getMorphologicalParseAt(0).getWord().getName(),
                    current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0), fsm)
        if twoPrevious is not None and twoPrevious.getMorphologicalParseAt(0) is not None and previous.getMorphologicalParseAt(0) is not None:
            synSets.extend(wordNet.constructIdiomSynSets(fsm, twoPrevious.getMorphologicalParseAt(0), twoPrevious.getMetamorphicParseAt(0),
                                                         previous.getMorphologicalParseAt(0), previous.getMetamorphicParseAt(0),
                                                         current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0)))
        if previous is not None and previous.getMorphologicalParseAt(0) is not None and next is not None and next.getMorphologicalParseAt(0) is not None:
            synSets.extend(wordNet.constructIdiomSynSets(fsm, previous.getMorphologicalParseAt(0), previous.getMetamorphicParseAt(0),
                                                         current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0),
                                                         next.getMorphologicalParseAt(0), next.getMetamorphicParseAt(0)))
        if next is not None and next.getMorphologicalParseAt(0) is not None and twoNext is not None and twoNext.getMorphologicalParseAt(0) is not None:
            synSets.extend(wordNet.constructIdiomSynSets(fsm, current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0),
                                                         next.getMorphologicalParseAt(0), next.getMetamorphicParseAt(0),
                                                         twoNext.getMorphologicalParseAt(0), twoNext.getMetamorphicParseAt(0)))
        if previous is not None and previous.getMorphologicalParseAt(0) is not None:
            synSets.extend(wordNet.constructIdiomSynSets(fsm, previous.getMorphologicalParseAt(0), previous.getMetamorphicParseAt(0),
                                                         current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0)))
        if next is not None and next.getMorphologicalParseAt(0) is not None:
            synSets.extend(wordNet.constructIdiomSynSets(fsm, current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0),
                                                         next.getMorphologicalParseAt(0), next.getMetamorphicParseAt(0)))
        return synSets

    def autoSemantic(self, parseTree: ParseTreeDrawable):
        if self.autoLabelSingleSemantics(parseTree):
            parseTree.save()
