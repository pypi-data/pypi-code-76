""" Functions to read in protein / nucleic sequences
"""
import re


def read_clustal(input_text, max_fields=3):
    """ Reads a ClustalW file with Multiple Sequence Alignment

    :param input_text: input data as text in the ClustalW format
    :type input_text: ``string``
    :param max_fields: number of data columns each line (2 for the original ClustalW format)
    :return: Multiple Sequence Alignment (MSA) in a JSON-like dictionary format that is :ref:`described here <msa>`
    """
    seqdic = {}
    input_text = input_text.split('\n')
    for line in input_text:
        tokens = line.split()
        if len(tokens) > max_fields or len(tokens) < 2: continue
        if not re.match("[a-zA-Z\-_]",tokens[1]): continue
        if tokens[0] in seqdic:
            z = seqdic[tokens[0]]
            z = z + tokens[1]
            seqdic[tokens[0]] = z
        else:
            seqdic[tokens[0]] = tokens[1]
    output = []
    for k, v in seqdic.items():
        output.append({"description": k, "sequence": seqdic[k].replace('.', '-').replace('~', '-')})
    return output


def read_msf(input_text):
    """ Reads a MSF file

    :param input_text: input data as text in the MSF format
    :type input_text: ``string``
    :return: Multiple Sequence Alignment (MSA) in a JSON-like dictionary format that is :ref:`described here <msa>`
    """
    return read_clustal(input_text, 2)


def read_fasta(input_text):
    """ Reads a FASTA file that contains nucleic / amino acid sequences

    The input file may contain one or more sequences, that may be aligned (i.e. an MSA) or not. Regardless the actual
    nature of the data, the sequences extracted from a given file are returned as a Multiple Sequence Alignment
    (which may comprise just a single sequence)

    :param input_text: input data as text in the FASTA format
    :type input_text: ``string``
    :return: Multiple Sequence Alignment (MSA) in a JSON-like dictionary format that is :ref:`described here <msa>`
    """
    seqdic = []
    last_header = ""
    last_seq = ""
    for line in input_text.split('\n'):
        if len(line) > 1 and line[0] == '>':
            if len(last_header) > 0:
                seqdic.append({"description": last_header, "sequence": last_seq})
                last_seq = ""
            last_header = line[1:]
        else:
            if len(line) > 2:
                last_seq += line
    if last_header not in seqdic:
        seqdic.append({"description": last_header, "sequence": last_seq})

    return seqdic

