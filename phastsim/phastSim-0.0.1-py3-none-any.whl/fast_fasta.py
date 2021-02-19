from collections import deque
import numpy as np
import os
import subprocess
import time
import mmap
import random
import matplotlib.pyplot as plt

import line_profiler
import sys
sys.path.insert(0, "/home/lukas/Desktop/phastSim/code")
sys.path.insert(0, "/home/lukas/Desktop/phastSim/scripts")
import set_args
args = set_args.arrrgs()

allelesList = ["A", "C", "G", "T"]


#%%

import numpy as np
from ete3 import Tree
import time
import sys

sys.path.insert(0, "/home/lukas/Desktop/phastSim/phastSim")
import phastSim
from importlib import reload

reload(phastSim)
# import phastSim.phastSim as phastSim


"""
Script that simulates sequence evolution along a given input phylogeny.
The algorithm (based on Gillespie approach) is fast for trees with short branches,
as for example in genomic epidemiology.
It can be instead be slower than traditional approaches when longer branch lengths are considered.

example run:
python3 efficientSimuSARS2.py --invariable 0.1 --alpha 1.0 --omegaAlpha 1.0 --scale 2.0 --hyperMutProbs 0.01
 --hyperMutRates  100.0 --codon --treeFile rob-11-7-20.newick --createFasta

Possible future extensions: 
allow multiple replicates in a single execution?
add wrapper to simulate whole sars-cov-2 genome evolution ?
CONSIDER TO EXTEND THE RANGE OF ALLOWED MODELS to allow easier specification og e.g. HKY, JC, etc?
ALLOW discretized gamma?
ALLOW INDELS ?
ALLOW TREE GENERATED ON THE GO, WITH MUTATIONS AFFECTING FITNESS and therefore birth rate of a lineage ?
allow mixtures of different models for different parts of the genome (e.g. coding and non-coding at the same time)

#SARS-CoV-2 genome annotation - not used yet but will be useful when simulating under a codon model.
#geneEnds=[[266,13468],[13468,21555],[21563,25384],[25393,26220],[26245,26472],[26523,27191],[27202,27387],
[27394,27759],[27894,28259],[28274,29533],[29558,29674]]
"""

# setup the argument parser and read the arguments from command line
parser = phastSim.setup_argument_parser()
# args = parser.parse_args()

# instantiate a phastSim run. This class holds all arguments and constants, which can be easily called as e.g.
# sim_run.args.path or sim_run.const.alleles
sim_run = phastSim.phastSimRun(args=args)
np.random.seed(args.seed)
hierarchy = not args.noHierarchy

# initialise the root genome. Reads either from file or creates a genome in codon or nucleotide mode
ref, refList = sim_run.init_rootGenome()

# set up substitution rates
mutMatrix = sim_run.init_substitution_rates()

# set up gamma rates
gammaRates = sim_run.init_gamma_rates()

# set up hypermutation rates
hyperCategories = sim_run.init_hypermutation_rates()

# set up codon substitution model
if sim_run.args.codon:
    omegas = sim_run.init_codon_substitution_model()
    gammaRates, omegas = phastSim.check_start_stop_codons(ref=ref, gammaRates=gammaRates, omegas=omegas)
else:
    omegas = None

# Loads a tree structure from a newick string in ETE2. The returned variable t is the root node for the tree.
start = time.time()
t = Tree(args.treeFile)
time1 = time.time() - start
print("Time for reading tree with ETE3: " + str(time1))

# save information about the categories of each site on a file
file = open(args.outpath + args.outputFile + ".info", "w")


genome_tree = phastSim.GenomeTree_hierarchical(
		nCodons=sim_run.nCodons,
		codon=sim_run.args.codon,
		ref=ref,
		gammaRates=gammaRates,
		omegas=omegas,
		mutMatrix=mutMatrix,
		hyperCategories=hyperCategories,
		hyperMutRates=sim_run.args.hyperMutRates,
		file=file,
		verbose=sim_run.args.verbose)

# populate the GenomeTree
genome_tree.populateGenomeTree(node=genome_tree.genomeRoot)

# normalize all rates
genome_tree.normalize_rates(scale=sim_run.args.scale)

time2 = time.time() - start
print("Total time after preparing for simulations: " + str(time2))

# NOW DO THE ACTUAL SIMULATIONS. DEFINE TEMPORARY STRUCTURE ON TOP OF THE CONSTANT REFERENCE GENOME TREE.
# define a multi-layered tree; we start the simulations with a genome tree.
# as we move down the phylogenetic tree, new layers are added below the starting tree.
# Nodes to layers below link to nodes above, or to nodes on the same layer, but never to nodes in the layer below.
# while traversing the tree, as we move up gain from a node back to its parent
# (so that we can move to siblings etc), the nodes in layers below the current one are simply "forgotten"
# (in C they could be de-allocated, but the task here is left to python automation).
genome_tree.mutateBranchETEhierarchy(t, genome_tree.genomeRoot, 1, sim_run.args.createNewick)



#%%
#
# def collect_mutations(node):
#     # collect mutations until hitting leaf
#     sites = []
#     chars = []
#     c_sites = []
#     c_chars = []
#
#     mutations = []
#     clen = 0
#     chain = []
#     n_leaf = 1
#
#     print(len(node.mutations))
#     for m in node.mutations:
#         sites.append(m[0])
#         chars.append(allelesList[m[2]])
#
#     mutations.append(len(node.mutations))
#
#
#     # once leaf is hit, return
#     if node.is_leaf():
#         print("hit leaf")
#
#         # return sites, chars, mutations, clen, chain
#
#     # pass to children
#     else:
#         c_sites = []
#         c_chars = []
#         for c in node.children:
#             print("visiting child")
#             ss, cs, ms, clen, chain, n_leaf = collect_mutations(node=c)
#
#             c_sites.extend(ss)
#             c_chars.extend(cs)
#             mutations.extend(ms)
#             clen += 1
#
#     chain.append(clen)
#     clen = 0
#
#     n_leaf += 1
#
#     sites.extend(c_sites)
#     chars.extend(c_chars)
#
#     return sites, chars, mutations, clen, chain, n_leaf
#
#
# def write_genome_fast(tree):
#     total_sites = deque()
#     total_chars = deque()
#
#     # some random offset
#     offset = 1e5
#     curr_offset = 0
#     total_mutations = 0
#
#     sites, chars = collect_mutations(node=tree)
#
#     return total_sites, total_chars, total_mutations





def execute(command):
    # create the unix process
    running = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               encoding='utf-8', shell=True)
    # run on a shell and wait until it finishes
    stdout, stderr = running.communicate()


def edit_sites(filename, sites, new_characters, headers, header_positions):
    # open the file
    with open(filename, mode="r+") as f:
        # instantiate a memory map with writing acess
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
        # loop through the sites we want to change and assign new characters
        for s in range(sites.shape[0]):
            # print(f"editing {sites[s]} {new_characters[s]}")
            mm[sites[s]: sites[s] + 1] = new_characters[s].encode('ascii')

        # loop through again to change headers
        for h in range(len(headers)):
            mm[header_positions[h]: header_positions[h] + 7] = f'{headers[h]} '.encode('ascii')

        # flush the changes from memory to disk
        mm.flush()


# try a non recursive way

def collect_mutations(tree, offset, header_len, line_len):
    sites = deque()
    chars = deque()
    current_offset = header_len

    for leaf in tree.iter_leaves():
        c_node = leaf
        leaf_sites = deque()
        leaf_chars = deque()

        while True:
            anc = c_node.up
            if not anc:
                break
            # for m in anc.mutations:
            ls = [m[0] for m in anc.mutations]
            lc = [allelesList[m[2]] for m in anc.mutations]
            leaf_sites.extend(ls)
            leaf_chars.extend(lc)
                # leaf_sites.append(m[0])
                # leaf_chars.append(allelesList[m[2]])
            c_node = anc

        for m in leaf.mutations:
            leaf_sites.append(m[0])
            leaf_chars.append(allelesList[m[2]])

        # done with one leaf
        # calc offsets and append
        leaf_sites = np.array(leaf_sites, dtype='int')
        # divide by line length to account for multi line fasta
        leaf_sites = leaf_sites + np.floor_divide(leaf_sites, line_len) + 1

        leaf_sites = leaf_sites + current_offset

        current_offset += offset

        sites.extend(leaf_sites)
        chars.extend(leaf_chars)

    return sites, chars


def write_genome_fast(tree, ref):
    # get length of reference file in bytes for the offset
    offset = os.stat(ref).st_size

    with open(ref, "r") as file:
        first = file.readline().strip()
        second = file.readline().strip()
    header_len = len(first)
    line_len = len(second)


    sites, chars = collect_mutations(tree, offset, header_len, line_len)

    n_tips = len(tree)

    # unix command that appends a file to itself "n_copies" times
    command = f"yes {ref} | head -n {n_tips} | xargs cat >ref.fa"

    # generate headers
    headers = range(100000, 100000 + n_tips)
    header_positions = (np.arange(n_tips) * offset) + 1


    # generate random sites and random characters
    execute(command)
    chars = list(chars)
    sites = np.array(sites)

    # # try if sorting makes it faster
    # sorting = np.argsort(sites)
    # sites = sites[sorting]
    # chars = chars[sorting]


    edit_sites("ref.fa", sites, chars, headers, header_positions)



#%%
#
#
# lp = line_profiler.LineProfiler()
#
# # execute2 = lp(execute)
# edit_sites = lp(edit_sites)
# collect_mutations = lp(collect_mutations)
# write_genome_fast = lp(write_genome_fast)


#%%

ref = "phastSim/example/MN908947.3.fasta"
tic = time.time()
write_genome_fast(tree=t, ref=ref)
toc = time.time()
print(toc - tic)


tic = time.time()
genome_tree.write_genome(tree=t, output_path='./', output_file='old', refList=refList)
toc = time.time()
print(toc - tic)


# lp.print_stats()

# import matplotlib.pyplot as plt
# plt.plot(sites, '.')
# plt.show()

