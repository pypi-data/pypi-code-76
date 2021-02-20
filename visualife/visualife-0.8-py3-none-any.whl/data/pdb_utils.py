"""Provides utility functions that operate on a PDB data structure (atoms, residues and chains).

"""
from visualife.data import Bond
from visualife.utils.text_utils import from_string

vdw_atomic_radii = {"H": 1, "C": 1.7, "N": 1.55, "O": 1.52, "P": 1.8, "S": 1.8,"SE": 1.8, "FE" : 1.7, "MO":1.8 }

vdw_interatomic_distances = {}

amino_acid_code3_to_code1 = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
                    'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
                    'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
                    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
                    'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

amino_acid_code1_to_code3 = {'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS', 'E': 'GLU', 'Q': 'GLN',
                             'G': 'GLY', 'H': 'HIS', 'I': 'ILE', 'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE',
                             'P': 'PRO', 'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL'}

kd_hydrophobicity = {'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5, 'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2,
                     'I': 4.5, 'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6, 'S': -0.8, 'T': -0.7, 'W': -0.9,
                     'Y': -1.3, 'V': 4.2, 'X': 0.0}

def create_sequence(residues):
    """Creates an amino acid sequence from a list of Residue objects.

    :param residues: (``list[Residue]``) a list of residues
    :return: amino acid sequence as a string
    """

    seq = [amino_acid_code3_to_code1.get(r.res_name, 'X') for r in residues]
    return ''.join(seq)


def create_secondary_structure(pdb_as_text, residues):
    """Reads PDB header and creates a secondary structure in FASTA format
    """
    resids = [r.locator() for r in residues]
    helix_header = []
    strand_header = []
    sec_str = ['C' for _ in range(len(resids))]

    for line in pdb_as_text.split("\n"):
        if line[0:5] == "HELIX": helix_header.append(line)
        elif line[0:5] == "SHEET": strand_header.append(line)

    for helix_line in helix_header:
        # serial = int(from_string(helix_line, 7, 11, -1))
        # helix_id = helix_line[11:14]
        # residue_name_from = helix_line[15:18]
        # residue_name_to = helix_line[27:30]
        chain_from = helix_line[19]
        residue_id_from = int(from_string(helix_line, 21, 25, -1))
        insert_from = helix_line[25]
        residue_id_to = int(from_string(helix_line, 33, 37, -1))
        chain_to = helix_line[31]
        insert_to = helix_line[37]
        l_from = "%c%d%c" % (chain_from, residue_id_from, insert_from)
        l_to = "%c%d%c" % (chain_to, residue_id_to, insert_to)

        for pos in range(resids.index(l_from),resids.index(l_to)+1):
            sec_str[pos] = 'H'

    for sheet_line in strand_header:
        # serial = int(from_string(sheet_line, 7, 10, -1))
        # strand_id = sheet_line[11:14]
        # num_strands = int(from_string(sheet_line, 14, 16, -1))
        # residue_name_from = sheet_line[17:20]
        # residue_name_to = sheet_line[28:31]
        chain_from = sheet_line[21]
        residue_id_from = int(from_string(sheet_line, 22, 26, -1))
        insert_from = sheet_line[26]
        residue_id_to = int(from_string(sheet_line, 33, 37, -1))
        chain_to = sheet_line[32]
        insert_to = sheet_line[37]

        l_from = "%c%d%c" % (chain_from, residue_id_from, insert_from)
        l_to = "%c%d%c" % (chain_to, residue_id_to, insert_to)

        for pos in range(resids.index(l_from),resids.index(l_to)+1):
            sec_str[pos] = 'E'

    return ''.join(sec_str)


def detect_bonds(a_chain) :
    """ Detects bonds between atoms of this chain

    :param a_chain: a chain of residues (a protein or a nucleic acid)
    :type a_chain: ``Chain``
    :return: a list of bonds detected
    """

    if len(vdw_interatomic_distances) == 0 : prepare_vdw_interatomic_distances()
    bonds = []
    for ri in a_chain.residues:
        iid = ri.res_id
        for rj in a_chain.residues:
            if abs(iid - rj.res_id) > 1: continue
            for ai in ri.atoms:
                x = ai.x
                y = ai.y
                z = ai.z
                for aj in rj.atoms:
                    if ai != aj :
                        r = x - aj.x
                        r2 = r*r
                        if r2 > 5.0: continue
                        r = y - aj.y
                        r2 += r*r
                        if r2 > 5.0: continue
                        r = z - aj.z
                        r2 += r*r
                        if r2 < vdw_interatomic_distances[ai.element + aj.element]:
                            b = Bond(ai, aj, "1")
                            bonds.append(b)

    return bonds


def prepare_vdw_interatomic_distances() :
    """Reads atomic radiuses and prepares distances for van der Waals interactions
    """

    for ei in vdw_atomic_radii :
        ri = vdw_atomic_radii[ei]
        for ej in vdw_atomic_radii:
            r = vdw_atomic_radii[ej] + ri
            vdw_interatomic_distances[ei+ej] = r*r*0.4