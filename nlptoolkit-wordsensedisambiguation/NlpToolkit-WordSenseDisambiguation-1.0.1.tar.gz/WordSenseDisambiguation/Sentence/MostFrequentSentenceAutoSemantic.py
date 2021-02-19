from AnnotatedSentence.AnnotatedSentence import AnnotatedSentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.SynSet import SynSet
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.Sentence.SentenceAutoSemantic import SentenceAutoSemantic


class MostFrequentSentenceAutoSemantic(SentenceAutoSemantic):

    __turkishWordNet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__turkishWordNet = turkishWordNet
        self.__fsm = fsm

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

    def autoLabelSingleSemantics(self, sentence: AnnotatedSentence) -> bool:
        for i in range(sentence.wordCount()):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, sentence, i)
            if len(synSets) > 0:
                best = self.mostFrequent(synSets, sentence.getWord(i).getParse().getWord().getName())
                if best is not None:
                    sentence.getWord(i).setSemantic(best.getId())
        return True
