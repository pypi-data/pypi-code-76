#!python
"""
# Author: Xiong Lei
# Created Time : Wed 10 Jul 2019 08:42:21 PM CST

# File Name: munit.py
# Description:

"""


import argparse
from scalex.function import SCALEX



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Single-Cell Analysis via Latent feature Extraction Universally')
    
    parser.add_argument('--data_list', '-d', type=str, nargs='+', default=[])
    parser.add_argument('--batch_categories', '-b', type=str, nargs='+', default=None)
    parser.add_argument('--join', type=str, default='inner')
    parser.add_argument('--batch_key', type=str, default='batch')
    parser.add_argument('--batch_name', type=str, default='batch')
    
    parser.add_argument('--min_genes', type=int, default=600)
    parser.add_argument('--min_cells', type=int, default=3)
    parser.add_argument('--n_top_genes', type=int, default=2000)
#     parser.add_argument('--processed', action='store_true')
    
#     parser.add_argument('--concat', action='store_true')
    parser.add_argument('--projection', '-p', default=None)
    parser.add_argument('--impute', type=str, default=None)
    parser.add_argument('--outdir', '-o', type=str, default='output/')
    
    parser.add_argument('--lr', type=float, default=2e-4)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('-g','--gpu', type=int, default=0)
    parser.add_argument('--max_iteration', type=int, default=30000)
    parser.add_argument('--seed', type=int, default=124)
    parser.add_argument('--chunk_size', type=int, default=20000)
    parser.add_argument('--ignore_umap', action='store_true')
    parser.add_argument('--repeat', action='store_true')
    parser.add_argument('--assess', action='store_true')
#     parser.add_argument('--beta', type=float, default=0.5)
#     parser.add_argument('--hid_dim', type=int, default=1024)
#     parser.add_argument('--eval', action='store_true')

    args = parser.parse_args()

    
    adata = SCALEX(
        args.data_list, 
        batch_categories=args.batch_categories, 
        join=args.join, 
        batch_key=args.batch_key, 
        min_genes=args.min_genes, 
        min_cells=args.min_cells, 
        n_top_genes=args.n_top_genes, 
        batch_size=args.batch_size, 
        lr=args.lr, 
        max_iteration=args.max_iteration, 
        impute=args.impute,
        batch_name=args.batch_name, 
        seed=args.seed, 
        gpu=args.gpu, 
        outdir=args.outdir, 
        projection=args.projection, 
        chunk_size=args.chunk_size,
        ignore_umap=args.ignore_umap,
        repeat=args.repeat,
        verbose=True,
        assess=args.assess
    )
