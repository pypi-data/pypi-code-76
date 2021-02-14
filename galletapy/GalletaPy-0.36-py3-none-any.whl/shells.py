import numpy as np
from scipy.special import factorial2
import pubchempy as pcp

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources
from . import basis


class shell:
    def __init__(self,l,exp,coef,coord):
        self.l = l
        self.exp = exp
        self.coef = coef
        self.coord = np.array(coord)
        self.k = len(exp)
        
        #normalizacion
        for i in range(self.k):
            coef[i] = coef[i]*(2*exp[i]/np.pi)**(3/4)*(4*exp[i])**(l/2)
            
        norm = 0
        for j in range(self.k):
            for k in range(self.k):
                norm += coef[j]*coef[k]*(np.pi/(exp[j]+exp[k]))**(3/2)/(2*(exp[j]+exp[k]))**(l)

        for i in range(self.k):
            coef[i] = coef[i]/np.sqrt(norm)
        
        self.orientaciones = []
        i = 0
        for lx in range(l,-1,-1):
            for ly in range(l-lx,-1,-1):
                lz = l-lx-ly
                self.orientaciones.append([i,lx,ly,lz])      
                i = i + 1

        self.N = np.ones(int((l+1)*(l+2)/2))
        for i,lx,ly,lz in self.orientaciones:
            self.N[i] = np.sqrt(1/(factorial2(2*lx-1)*factorial2(2*ly-1)*factorial2(2*lz-1)))

class shell_pair:
    def __init__(self,g_a,g_b):
        
        self.g_a = g_a
        self.g_b = g_b
        
        self.exp = np.add.outer(g_a.exp, g_b.exp).flatten()
        self.coef = np.multiply.outer(g_a.coef, g_b.coef).flatten()
        
        self.coord = []
        self.ab = []
        for i in range(g_a.k):
            for j in range(g_b.k):
                self.coord.append((g_a.exp[i]*g_a.coord+g_b.exp[j]*g_b.coord)/(g_a.exp[i]+g_b.exp[j]))
                self.ab.append((g_a.exp[i],g_b.exp[j]))

                
        self.alpha = []
        for i in range(g_a.k):
            for j in range(g_b.k):
                self.alpha.append((g_a.exp[i]*g_b.exp[j])/(g_a.exp[i]+g_b.exp[j]))
                                
        self.k = len(self.exp)

def get_set_of_shells(element,coord,basis_name):

    element = element.upper()
    shells = []
    
    # Open basis file
    f = pkg_resources.open_text(basis, basis_name+".bas")    
    #f = open("basis/"+basis_name+".bas","r")

    # Find_atom
    atom_found = False
    for line in f:
        if(atom_found):
            break
        splitted_line = line.split()
        if(len(splitted_line)>0):
            if("O-" in splitted_line[0]):
                if(splitted_line[1] == element):
                    atom_found=True

    # Pass the scheme contraction info line
    for line in f:
        num_of_shells = int(line)
        break
    
    # Read shells
    new_shell = True
    idx_shell = 0
    idx_prim = 0
    for line in f:
        splitted_line = line.split()
        #If new shell, read angular momentum and number of primitives
        if new_shell:
            idx_shell += 1
            idx_prim = 0        
            idx,l,num_of_primitives = int(splitted_line[0]),int(splitted_line[1]),int(splitted_line[2])
            exp = []
            coef = []
            new_shell = False
            continue
        #If not a new shell, read exponents and coefficients
        if not new_shell:
            idx_prim += 1
            exp.append(float(splitted_line[0]))
            coef.append(float(splitted_line[1]))
            if(idx_prim == num_of_primitives):
                shells.append(shell(l,exp,coef,coord))
                #If all shells readed, break, else, read new shell
                if(idx_shell == num_of_shells):
                    break
                else:
                    new_shell = True
            continue
    f.close()
    
    return shells       

def get_all_shells_from_pubchempy_name(name,basis_name):
    c = pcp.get_compounds(name, 'name')
    cid = c.cid
    c = pcp.Compound.from_cid(cid,record_type='3d')
    dic = c.to_dict(properties=['atoms'])
    shells = []
    for atom in dic['atoms']:
        shells += get_set_of_shells(atom['element'],(atom['x'],atom['y'],atom['z']),basis_name)
    return shells

def get_all_shells_from_pubchempy_cid(cid,basis_name):
    c = pcp.Compound.from_cid(cid,record_type='3d')
    dic = c.to_dict(properties=['atoms'])
    shells = []
    for atom in dic['atoms']:
        shells += get_set_of_shells(atom['element'],(atom['x'],atom['y'],atom['z']),basis_name)
    return shells

def get_all_shells_from_xyz(molecule,basis_name):
    molecule = molecule.split()
    natoms = int(len(molecule)/4)
    shells = []
    for atom in range(natoms):
        shells += get_set_of_shells(molecule[atom*4],(float(molecule[atom*4+1]),float(molecule[atom*4+2]),float(molecule[atom*4+3])),basis_name)
    return shells
