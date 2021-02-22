# type: ignore
import bz2
import dataclasses
import json
import random
import typing as t
from collections import defaultdict
from functools import partial, singledispatchmethod
from pathlib import Path


STX = "\002"
ETX = "\003"
CONTROL = {STX: -1, ETX: -2, -1: STX, -2: ETX}

wcounter = partial(defaultdict, int)
datadict = partial(defaultdict, wcounter)


@dataclasses.dataclass
class Markov:
    _words: t.List[str] = dataclasses.field(default_factory=list)
    _data: t.DefaultDict[int, t.DefaultDict[int, int]] = dataclasses.field(
        default_factory=datadict
    )

    @staticmethod
    def formatdata(data: t.Dict) -> t.Dict:
        d = datadict()
        for k, p in data.items():
            d[int(k)] = wcounter({int(k): v for k, v in p.items()})
        return d

    @classmethod
    def from_corpus(cls, corpus: str) -> "Markov":
        return cls.from_sentences(sentences=corpus.splitlines())

    @classmethod
    def from_sentences(cls, sentences: t.List[str]) -> "Markov":
        m = cls()
        [m.ingest_sentence(s) for s in sentences]
        return m

    @classmethod
    def from_mseed(cls, mseed: t.Dict) -> "Markov":
        return cls(_words=mseed["_words"], _data=cls.formatdata(mseed["_data"]))

    @classmethod
    def from_mseedfile(cls, path: Path) -> "Markov":
        with bz2.open(path, "rb") as f:
            return cls.from_mseed(json.loads(f.read()))

    @property
    def key(self) -> int:
        self._key += 1
        return self._key

    @property
    def words(self):
        return set(self._words)

    @singledispatchmethod
    def add_word(self, word: str) -> None:
        if word not in self._words:
            self._words.append(word)

    @add_word.register
    def _(self, words: list) -> None:
        [self.add_word(w) for w in words]

    @singledispatchmethod
    def _get(self, k: int) -> str:
        if k in CONTROL:
            return CONTROL[k]
        else:
            return self._words[k]

    @_get.register
    def _(self, k: str) -> int:
        if k in CONTROL:
            return CONTROL[k]
        else:
            return self._words.index(k)

    @property
    def start(self) -> int:
        return CONTROL[STX]

    @property
    def end(self) -> int:
        return CONTROL[ETX]

    def ingest_bigram(self, b: t.Tuple[str, str]) -> None:
        self._data[self._get(b[0])][self._get(b[1])] += 1

    @singledispatchmethod
    def ingest_sentence(self, s: t.List[str]) -> None:
        self.add_word(s)
        s.append(ETX)
        [self.ingest_bigram(b) for b in zip([STX] + s, s)]

    @ingest_sentence.register
    def _(self, s: str) -> None:
        self.ingest_sentence(s.split())

    @singledispatchmethod
    def follows(self, leads: int) -> int:

        try:
            p, w = zip(*self._data[leads].items())
        except ValueError:
            return -2
        return random.choices(population=p, weights=w)[0]

    @follows.register
    def _(self, leads: str):
        return self.follows(self._get(leads))

    def nsentence(self, state: str = None):
        """ Return a list of ints representing a sentence. """
        if state is None:
            state = self.start
        result = []
        while state != self.end:
            result.append((state := self.follows(state)))
        return result

    def sentence(self, state: str = None):
        """ Returns a text sentence. """
        return self.translate(self.nsentence())

    def translate(self, s: t.List[int]) -> str:
        return [self._get(i) for i in s if i > 0]

    def get_text(self, sentences: int) -> str:
        return "\n".join(
            [" ".join(self.sentence()).capitalize() for i in range(sentences)]
        )

    @property
    def mseed(self):
        return {"_words": self._words, "_data": self._data}

    def save(self, path):
        with bz2.open(path, "wb") as f:
            f.write(json.dumps(self.mseed).encode("utf-8"))
