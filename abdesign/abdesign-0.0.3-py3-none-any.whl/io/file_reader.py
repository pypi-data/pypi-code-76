from Bio.SeqIO.FastaIO import SimpleFastaParser
import os

def read_fasta(files):
    """Generator function. Reads protein sequences from FASTA file.

    Parameters
    ----------
    files : list
        List of filenames to read in.
    """
    if any(not os.path.exists(f) for f in files):
        raise ValueError("Can not find files.")

    sequences = set()

    for file in files:
        with open(file, 'r') as f:
            for _id, seq in SimpleFastaParser(f):
                sequences.add(seq.strip().upper())
    
    return sequences