def quantity_of_atom(mol_formula,atomic_id):
    import numpy as np
    import re

    #break the metabolite atoms (a formula containing on the atoms that are part of the original metabolite) up so atoms and quantities are consecutive entries in a numpy array
    broken_mol_formula = np.array(re.findall('[A-Z][a-z]?|[0-9]+', mol_formula))
    #    '[A-Z][a-z]?|[0-9]+': A capital letter [A-Z], followed by a lowercase letter [a-z], which is optional '?', or '|' a number '[0-9]', and possibly more numbers '+'
    #    example: this command will take formula = C6H12N1O3Si1 and return broken_formula = array(['C','6','H','12','N','1','O','3','Si','1'])
    #        all components are strings

    #the number of rows of the correction matrix is equal to the quantity of the atom being corrected for that are in the fragment and the original metabolite
    atom_index = np.where(broken_mol_formula==atomic_id)[0][0]
    atom_quantity_index = atom_index+1
    atom_quantity = broken_mol_formula[atom_quantity_index]
    atom_quantity = atom_quantity.astype(np.int)

    return(atom_quantity)
