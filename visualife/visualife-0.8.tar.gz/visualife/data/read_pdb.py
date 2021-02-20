"""Functions to parse bimolecular structures in PDB format
"""

from visualife.data import Atom, Residue, Chain, Structure


def parse_pdb_data(pdb_as_text, **kwargs):

    """Parses PDB data

    :param pdb_as_text: pdb data as a multiline text
    :type pdb_as_text: ``string``
    :param kwargs: see below

    :Keyword Arguments:
        * *skip_heteroatoms* (``boolean``) -- skip heteroatoms, ``False`` by default
        * *parse_atoms* (``boolean``) -- if ``True`` (the default), all :class:`visualife.data.Atom` objects
            will be created; when set to ``False``, this function won't extract coordinates
    :return: a list of :class:`visualife.data.Structure` objects, created from models found in the given data
    """
    if_hetatoms = kwargs.get("skip_heteroatoms", False)
    if_parse_atoms = kwargs.get("parse_atoms", True)
    structures = []
    for line in pdb_as_text.split("\n"):
        if line[0:5] == "MODEL":
            s = Structure()
            structures.append(s)
        if line[0:2] != 'AT' and line[0:4] != 'HETA': continue
        if if_hetatoms and line[0:4] == 'HETA': continue
        line = line.strip()
        rname = line[17:20]
        chainid = line[21]
        resid = int(line[23:26].strip())
        res_alt_loc = line[26]

        if len(structures) == 0 : # Make sure we have a structure
            s = Structure()
            structures.append(s)
        else : s = structures[-1]

        if len(s.chains) == 0: # Make sure we have a chain
            c = Chain(chainid)
            s.chains.append(c)
            c.owner = s
        elif s.chains[-1].chain_id != chainid :  # Make sure we have the current chain
            c = Chain(chainid)
            s.chains.append(c)
            c.owner = s
        else : c = s.chains[-1]

        if len(c.residues) == 0 :
            r = Residue(rname, resid, res_alt_loc)
            c.residues.append(r)
            r.owner = c
            s.residues.append(r)
        elif r.res_id != resid or (r.alt_loc != res_alt_loc and r.res_id == resid)  :
            r = Residue(rname, resid, res_alt_loc)
            c.residues.append(r)
            r.owner = c
            s.residues.append(r)
        else: r = c.residues[-1]

        if if_parse_atoms:
            a = parse_pdb_atom(line)
            structures[-1].atoms.append(a)
            r.atoms.append(a)
            a.owner = r

    return structures


def parse_pdb_atom(atom_line):
    """ Parses an ATOM line of a PDB file and creates a new atom.

    The returned atom doesn't belong to any residue or chain (must be appended by a user)
    
    :param atom_line: a single line of a PDB file (an ATOM field)
    :type atom_line: ``string``
    :return: a newly created :class:`visualife.data.Atom` object
    """
    atom_number = int(atom_line[6:11].strip())
    x_position = float(atom_line[30:38].strip())
    y_position = float(atom_line[38:47].strip())
    z_position = float(atom_line[47:54].strip())
    atom_name = atom_line[12:16].strip()
    atom_alt_loc = atom_line[16]
    return Atom([x_position, y_position, z_position, atom_number, atom_name, atom_alt_loc])


def write_pdb_atom(atom, res_name="UNK", chain_id='X'):
    """ Returns a string in PDB format that holds data for a given atom

    :param atom: an object to be written
    :type atom: :class:`visualife.data.Atom`
    :return: a PDB-formatted line
    """
    return "HETATM%5d %4s %s %c   1    %8.3f%8.3f%8.3f  1.00  0.00           %2s" % \
           (atom.id, atom.name, res_name, chain_id, atom.x, atom.y, atom.z, atom.element)

