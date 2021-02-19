#!/usr/bin/env python
"""
# Author: Xiong Lei
# Created Time : Tue 29 Sep 2020 01:41:23 PM CST

# File Name: function.py
# Description:

"""

import torch
import numpy as np
import os
import scanpy as sc
from anndata import AnnData
from sklearn.metrics import silhouette_score

from .dataset import load_dataset
from .net.vae import VAE
from .net.utils import EarlyStopping
from .metrics import mixingMetric, entropy_batch_mixing
from .logger import create_logger
from .visualize import plot_umap


def SCALEX(
        data_list, 
        batch_categories=None, 
        join='inner', 
        batch_key='batch', 
        batch_name='batch',
        min_genes=600, 
        min_cells=3, 
        n_top_genes=2000, 
        batch_size=64, 
        lr=2e-4, 
        max_iteration=30000,
        seed=124, 
        gpu=0, 
        outdir='output/', 
        projection=None,
        repeat=False,
        impute=None, 
        chunk_size=20000,
        ignore_umap=False,
        verbose=False,
        assess=False,
    ):
    
#     sc.logging.print_versions()
    np.random.seed(seed) # seed
    torch.manual_seed(seed)

    if torch.cuda.is_available(): # cuda device
        device='cuda'
        torch.cuda.set_device(gpu)
    else:
        device='cpu'
    
    outdir = outdir+'/'
    os.makedirs(outdir+'/checkpoint', exist_ok=True)
    log = create_logger('', fh=outdir+'log.txt')
    if not projection:
        adata, trainloader, testloader = load_dataset(
            data_list, batch_categories, 
            join=join, 
            n_top_genes=n_top_genes,
            batch_size=batch_size, 
            chunk_size=chunk_size,
            min_genes=min_genes, 
            min_cells=min_cells,
            batch_name=batch_name, 
            batch_key=batch_key,
            log=log
        )
        
        early_stopping = EarlyStopping(patience=10, checkpoint_file=outdir+'/checkpoint/model.pt')
        x_dim, n_domain = adata.shape[1], len(adata.obs['batch'].cat.categories)
        enc = [['fc', 1024, 1, 'relu'],['fc', 10, '', '']]  # TO DO
        dec = [['fc', x_dim, n_domain, 'sigmoid']]
        model = VAE(enc, dec, n_domain=n_domain)
        log.info('model\n'+model.__repr__())
        model.fit(
            trainloader, testloader=testloader,
            lr=lr, 
            max_iteration=max_iteration, 
            device=device, 
            early_stopping=early_stopping, 
            verbose=verbose,
        )
        torch.save({'n_top_genes':adata.var.index, 'enc':enc, 'dec':dec, 'n_domain':n_domain}, outdir+'/checkpoint/config.pt')     
    else:
        state = torch.load(projection+'/checkpoint/config.pt')
        n_top_genes, enc, dec, n_domain = state['n_top_genes'], state['enc'], state['dec'], state['n_domain']
        model = VAE(enc, dec, n_domain=n_domain)
        model.load_model(projection+'/checkpoint/model.pt')
        model.to(device)
        
        adata, trainloader, testloader = load_dataset(
            data_list, batch_categories, 
            join='outer', 
            chunk_size=chunk_size,
            n_top_genes=n_top_genes, 
            min_cells=0,
            batch_name=batch_name,
            batch_key=batch_key,
            log = log
        )
#         log.info('Processed dataset shape: {}'.format(adata.shape))
        
    adata.obsm['latent'] = model.encodeBatch(testloader, device=device) # save latent rep
    if impute:
        adata.layers['impute'] = model.encodeBatch(testloader, out='impute', batch_id=impute, device=device)
    log.info('Output dir: {}'.format(outdir))
        
    if projection and (not repeat):
        ref = sc.read_h5ad(projection+'/adata.h5ad')
        adata = AnnData.concatenate(
            ref, adata, 
            batch_categories=['reference', 'query'], 
            batch_key='projection', 
            index_unique=None
        )
    adata.write(outdir+'adata.h5ad', compression='gzip')  
    if not ignore_umap: #and adata.shape[0]<1e6:
        log.info('Plot umap')
        sc.pp.neighbors(adata, n_neighbors=30, use_rep='latent')
        sc.tl.umap(adata, min_dist=0.1)
        sc.tl.leiden(adata)
        
        # UMAP visualization
        sc.settings.figdir = outdir
        sc.set_figure_params(dpi=80, figsize=(10,10), fontsize=20)
        cols = ['batch', 'celltype', 'leiden']
        color = [c for c in cols if c in adata.obs]
        if len(color) > 0:
            if projection and (not repeat):
                plot_umap(adata, cond1='projection', save='.pdf')
            else:
                sc.pl.umap(adata, color=color, save='.pdf', wspace=0.4, ncols=4)
           
        if assess:
            if len(adata.obs['batch'].cat.categories) > 1:
                entropy_score = entropy_batch_mixing(adata.obsm['X_umap'], adata.obs['batch'])
                log.info('entropy_batch_mixing: {:.3f}'.format(entropy_score))

            if 'celltype' in adata.obs:
                sil_score = silhouette_score(adata.obsm['X_umap'], adata.obs['celltype'].cat.codes)
                log.info("silhouette_score: {:.3f}".format(sil_score))

    adata.write(outdir+'adata.h5ad', compression='gzip')
        
        


