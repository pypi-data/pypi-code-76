from typing import List
from .seq import Seq


def read_fasta(path_to_fasta_file: str = None, lines: list = None) -> List[Seq]:
    """Turn the lines of a fasta file into a list of Seq objects"""
    if path_to_fasta_file:
        with open(path_to_fasta_file) as f:
            lines = f.readlines()
    sequences = []
    full_seq = []
    for line in reversed(lines):
        if line.startswith(">"):
            sequences.append(Seq(sequence="".join(full_seq[::-1]), id=line.strip()[1:]))
            full_seq = []
            continue
        full_seq.append(line.strip())
    return sequences[::-1]  # return order
