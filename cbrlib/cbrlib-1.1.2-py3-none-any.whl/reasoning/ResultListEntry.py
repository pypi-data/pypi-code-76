from cbrlib.model import AssemblyObject


class ResultListEntry:

    def __init__(self, similarity: float, case: AssemblyObject):
        self.similarity = similarity
        self.case = case

    def __lt__(self, other):
        if not isinstance(other, ResultListEntry) or other.similarity < self.similarity:
            return False
        return True

    def __gt__(self, other):
        if not isinstance(other, ResultListEntry) or other.similarity > self.similarity:
            return False
        return True

    def __eq__(self, other):
        if not isinstance(other, ResultListEntry) or other.similarity != self.similarity:
            return False
        return True

    def __str__(self):
        return f'{self.similarity} {self.case.to_serializable()}'

    def __repr__(self):
        return f'{self.similarity} {self.case.to_serializable()}'

    def to_serializable(self):
        return {
            'similarity': self.similarity,
            'case': self.case.to_serializable()
        }
