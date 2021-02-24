from __future__ import annotations

from typing import Generator
from collections import Counter
from itertools import zip_longest
from re import finditer

codon_table = """UUU F      CUU L      AUU I      GUU V
UUC F      CUC L      AUC I      GUC V
UUA L      CUA L      AUA I      GUA V
UUG L      CUG L      AUG M      GUG V
UCU S      CCU P      ACU T      GCU A
UCC S      CCC P      ACC T      GCC A
UCA S      CCA P      ACA T      GCA A
UCG S      CCG P      ACG T      GCG A
UAU Y      CAU H      AAU N      GAU D
UAC Y      CAC H      AAC N      GAC D
UAA Stop   CAA Q      AAA K      GAA E
UAG Stop   CAG Q      AAG K      GAG E
UGU C      CGU R      AGU S      GGU G
UGC C      CGC R      AGC S      GGC G
UGA Stop   CGA R      AGA R      GGA G
UGG W      CGG R      AGG R      GGG G"""

codons = dict(zip(codon_table.split()[::2], codon_table.split()[1::2]))


def consensus(*args):
    """Return a consensus sequence from n Seq objects."""
    counts = map(Counter, zip_longest(*args))
    consensus = ""
    for c in counts:
        del c[None]
        consensus += c.most_common(1)[0][0]
    return Seq(consensus, args[0].id)


class Seq:
    """Class for nucleotide sequences"""

    def __init__(self, sequence: str, id: str = None, codons: dict = codons):
        self.sequence = sequence
        self.id = id
        self.codons = codons

    def __repr__(self):
        if not self.id:
            return f"Seq({self.sequence[:60]})"
        concat = ""
        if len(self) > 60:
            concat = "..."
        return f"Seq({self.sequence[:60]}{concat}, id='{self.id}')"

    def __str__(self):
        return self.sequence

    def __len__(self) -> int:
        return len(self.sequence)

    def __invert__(self) -> Seq:
        """Inverting a Seq object (i.e. ~Seq) will return the reverse complement of that sequence"""
        return self.reverse_complement()

    def __eq__(self, other) -> bool:
        """Compare the string representations of two Seq objects"""
        return str(self) == str(other)

    def __add__(self, other: Seq) -> Seq:
        """Adding two sequence objects (i.e. Seq1 + Seq2) returns a new Seq object that is the
        concatenation of the two objects sequences. ID is taken from eh first object"""
        new_sequence = self.sequence + other.sequence
        return Seq(new_sequence, self.id)

    def __sub__(self, other: Seq) -> int:
        """Subtracting two Seq objects (i.e. seq1 - seq2) returns the hamming difference between them"""
        return sum(i != j for i, j in zip_longest(self.sequence, other.sequence))

    def __getitem__(self, index):
        return self.sequence[index]

    def __setitem__(self, index, nt):
        self.sequence = self.sequence[:index] + nt + self.sequence[index + 1 :]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self):
            result = self[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def __contains__(self, other):
        if str(other) in str(self):
            return True
        else:
            return False

    @property
    def gc(self) -> float:
        """Return the GC content of the sequence"""
        g = self.count("G")
        c = self.count("C")
        return (g + c) / len(self) * 100

    @property
    def counts(self) -> dict:
        """Return the counts of letters in the sequence"""
        return Counter(self.sequence)

    def to_fasta(self, line_length: int = 60) -> str:
        formated_sequence = "\n".join(
            [str(s) for s in self.kmers(line_length, line_length)]
        )
        return f">{self.id}\n{formated_sequence}\n"

    def kmers(self, n: int, step: int = 1) -> Generator:
        """Return a generator for kmers of length n"""
        return (
            Seq(self.sequence[i : i + n]) for i in range(0, len(self.sequence), step)
        )

    def count(self, string: str, max_diff: int = 0) -> int:
        if max_diff == 0:
            return self.sequence.count(string)
        other = Seq(string)
        return sum((kmer - other) <= max_diff for kmer in self.kmers(len(other)))

    def substitute(self, old: str, new: str, count: int = -1):
        return Seq(self.sequence.replace(str(old), str(new), count), self.id)

    def find(self, target: str, count: int = -1, overlapping: bool = False):
        locs = []
        if overlapping and len(target) > 1:
            target = f"(?=({target}))"
        matches = finditer(target, self.sequence)
        for i, match in enumerate(matches, 1):
            locs.append(match.start())
            if i == count:
                break
        return locs

    def reverse_complement(self, rna: bool = False) -> Seq:
        complements = {"A": "T", "T": "A", "G": "C", "C": "G"}
        if rna:
            complements = {"A": "U", "U": "A", "G": "C", "C": "G"}
        revc = "".join(complements[nt] for nt in reversed(self))
        return Seq(revc, self.id)

    def transcribe(self) -> Seq:
        return Seq(self.sequence.replace("T", "U"), self.id)

    def reverse_transcribe(self) -> Seq:
        return Seq(self.sequence.replace("U", "T"), self.id)

    def translate(self) -> Seq:
        """
        Return the translated sequence.
        *Currently stop signals are ignored.*
        """
        AA = "".join(
            self.codons[self.sequence[i : i + 3]]
            for i in range(0, len(self.sequence), 3)
            if self.codons[self.sequence[i : i + 3]] != "Stop"
        )
        return Seq(AA, self.id)
