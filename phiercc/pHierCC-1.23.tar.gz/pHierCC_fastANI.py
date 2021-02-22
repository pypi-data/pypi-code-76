#!/usr/bin/env python

# pHierCC.py
# pipeline for Hierarchical Clustering of cgMLST
#
# Author: Zhemin Zhou
# Lisence: GPLv3
#
# New assignment: pHierCC -p <allelic_profile> -o <output_prefix>
# Incremental assignment: pHierCC -p <allelic_profile> -o <output_prefix> -i <old_cluster_npz>
# Input format (tab delimited):
# ST_id gene1 gene2
# 1 1 1
# 2 1 2
# ...

import sys, gzip, logging, click
import pandas as pd, numpy as np
from multiprocessing import Pool #, set_start_method
from scipy.spatial import distance as ssd
from scipy.cluster.hierarchy import linkage
try :
    from getDistance import getDistance
except :
    from .getDistance import getDistance

logging.basicConfig(format='%(asctime)s | %(message)s', stream=sys.stdout, level=logging.INFO)

def read_fastANI(profile_file) :
    ids, dist = {}, []
    with gzip.open(profile_file, 'rt') as fin :
        for line in fin :
            part = line.strip().split('\t')
            if part[0] not in ids :
                ids[part[0]] = len(ids)
            if part[1] not in ids :
                ids[part[1]] = len(ids)
            while len(dist) < len(ids) :
                for d in dist :
                    d.append(75.)
                dist.append([75. for d in dist[0]] if len(dist)>0 else [75.])
            i1, i2 = ids[part[0]], ids[part[1]]
            dist[i1][i2] = float(part[2])
    dist = np.array(dist)
    idx = dist.T > dist
    dist[idx] = dist.T[idx]
    np.fill_diagonal(dist, 100.)
    return ids, 100-dist

def prepare_mat(profile_file) :
    mat = pd.read_csv(profile_file, sep='\t', header=None, dtype=str).values
    allele_columns = np.array([i == 0 or (not h.startswith('#')) for i, h in enumerate(mat[0])])
    mat = mat[1:, allele_columns].astype(int)
    mat = mat[mat.T[0]>0]
    return mat

@click.command()
@click.option('-p', '--profile', help='[INPUT] name of a profile file consisting of a table of columns of the ST numbers and the allelic numbers, separated by tabs. Can be GZIPped.',
                        required=True)
@click.option('-o', '--output',
                        help='[OUTPUT] Prefix for the output files consisting of a  NUMPY and a TEXT version of the clustering result. ',
                        required=True)
@click.option('-s', '--stepwise', 
                        help='increase <stepwise> % distance each level. The minimum ANI level is set to the mimimum value in the given matrix. (Default: 0.01)',
                        default=0.01, type=float)
@click.option('-n', '--n_proc', help='[INPUT; optional] Number of processes (CPUs) to use (Default: 4).', default=4, type=int)
def phierCC(profile, output, stepwise, n_proc):
    '''pHierCC takes a file containing allelic profiles (as in https://pubmlst.org/data/) and works
    out hierarchical clusters of the full dataset based on a minimum-spanning tree.'''
    pool = Pool(n_proc)

    profile_file, cluster_file = profile, output + '.npz'

    ids, dist = read_fastANI(profile_file)
    max_dist = np.max(dist)
    steps = np.arange(np.ceil(max_dist/stepwise).astype(int)+1, dtype=float)*stepwise
    dist = (dist/stepwise).astype(int)
    #n_loci = mat.shape[1] - 1

    logging.info(
        'Loaded in fastANI results of {0} genomes with maximum distance of {1}. Preparing {2} levels.'.format(
            len(ids), max_dist, len(steps)))
    logging.info('Start HierCC assignments')

    # prepare existing clusters

    res = np.repeat(np.arange(dist.shape[0]), len(steps) + 1).reshape(dist.shape[0], -1)
    logging.info('Start Single linkage clustering')
    slc = linkage(ssd.squareform(dist), method='single')

    descendents = [ [m] for m in np.arange(len(ids)) ] + [None for _ in np.arange(dist.shape[0]-1)]
    for idx, c in enumerate(slc.astype(int)) :
        n_id = idx + dist.shape[0]
        d = sorted([int(c[0]), int(c[1])], key=lambda x:descendents[x][0])
        min_id = min(descendents[d[0]])
        descendents[n_id] = descendents[d[0]] + descendents[d[1]]
        for tgt in descendents[d[1]] :
            res[tgt, c[2]+1:] = res[min_id, c[2]+1:]

    res.T[0] = np.arange(dist.shape[0])
    np.savez_compressed(cluster_file, hierCC=res, ids=ids)

    id2 = sorted([[i, n] for n, i in ids.items()])

    with gzip.open(output + '.HierCC.gz', 'wt') as fout:
        fout.write('#Genome\t{0}\n'.format('\t'.join(['HC{0:.3f}'.format(id) for id in steps])))
        for r in res[np.argsort(res.T[0])]:
            fout.write( '{0}\t'.format(id2[r[0]][1]) + '\t'.join([str(rr) for rr in r[1:]]) + '\n')

    logging.info('NPZ  clustering result (for production mode): {0}.npz'.format(output))
    logging.info('TEXT clustering result (for visual inspection and HCCeval): {0}.HierCC.gz'.format(output))
    pool.close()

if __name__ == '__main__':
    phierCC(sys.argv[1:])

