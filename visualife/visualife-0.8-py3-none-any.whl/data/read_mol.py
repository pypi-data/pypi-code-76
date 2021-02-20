import sys
from visualife.data import *

def parse_mol_data(mol_as_txt):
  """Reads a text in mol2 format and creates a ``Molecule`` object
  """

  llist = []
  for line in mol_as_txt.splitlines():
    llist.append(line.split())

  n_atoms = int(llist[3][0])
  n_bonds = int(llist[3][1])

  m = Molecule()
  for i in range(n_atoms):
    name = llist[i + 4][3]
    x = float(llist[i + 4][0])
    y = float(llist[i + 4][1])
    z = float(llist[i + 4][2])
    m.add_atom( Atom([x, y, z, i+1,name," "] ) )

  for j in range(n_bonds):
    atom1 = m.atoms[int(llist[j + n_atoms + 4][0])-1]
    atom2 = m.atoms[int(llist[j + n_atoms + 4][1])-1]
    type = int(llist[j + n_atoms + 4][2])
    b = Bond(atom1, atom2, type)
    m.add_bond(b)

  return m

if __name__ == "__main__" :

  inpt = open(sys.argv[1]).read()
  m = parse_mol_data(inpt)
  for a in m.atoms : print(a)
  for b in m.bonds : print(b)