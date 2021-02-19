#!/usr/bin/env python
"""
# Author: Xiong Lei
# Created Time : Mon 18 Nov 2019 01:16:06 PM CST

# File Name: vae.py
# Description:

"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm
from collections import defaultdict
import sys

from .layer import *
from .loss import *


class VAE(nn.Module):
    def __init__(self, enc, dec, n_domain=1):
        """
        enc: encoder structure config
        dec: decoder structure config
        n_domain: number of different domains
        """
        super().__init__()
        x_dim = dec[-1][1]
        z_dim = enc[-1][1]
        self.encoder = Encoder(x_dim, enc)
        self.decoder = NN(z_dim, dec)
        self.n_domain = n_domain
        self.x_dim = x_dim
        self.z_dim = z_dim
    
    def load_model(self, path):
        pretrained_dict = torch.load(path, map_location=lambda storage, loc: storage)                            
        model_dict = self.state_dict()
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
        model_dict.update(pretrained_dict) 
        self.load_state_dict(model_dict)
        
    def encodeBatch(
            self, 
            dataloader, 
            device='cuda', 
            out='latent', 
            batch_id=None,
            return_idx=False, 
            eval=False
    ):
        self.to(device)
        if eval:
            self.eval()
        else:
            self.train()
        indices = np.zeros(dataloader.dataset.shape[0])
        if out == 'latent':
            output = np.zeros((dataloader.dataset.shape[0], self.z_dim))
            
            for x,y,idx in dataloader:
                x = x.float().to(device)
                z = self.encoder(x)[1] # z, mu, var
                output[idx] = z.detach().cpu().numpy()
                indices[idx] = idx
        elif out == 'impute':
            output = np.zeros((dataloader.dataset.shape[0], self.x_dim))
            if batch_id is None:
                batch_id = 0
            else:
                batch_id = list(dataloader.dataset.adata.obs['batch'].cat.categories).index(batch_id)
            for x,y,idx in dataloader:
                x = x.float().to(device)
                z = self.encoder(x)[1] # z, mu, var
                output[idx] = self.decoder(z, torch.LongTensor([batch_id]*len(z))).detach().cpu().numpy()
        indices = np.zeros(dataloader.dataset.shape[0])
        if return_idx:
            return output, indices
        else:
            return output
    
    def fit(
            self, 
            dataloader, 
            testloader=None,
            lr=2e-4,
            max_iteration=30000,
            beta=0.5,
            early_stopping=None,
            device='cuda',  
            verbose=False,
        ):
        """
        Fit model
        """
        self.to(device)
        optim = torch.optim.Adam(self.parameters(), lr=lr, weight_decay=5e-4)
        n_epoch = int(np.ceil(max_iteration/len(dataloader)))
        
        with tqdm(range(n_epoch), total=n_epoch, desc='Epochs') as tq:       
            for epoch in tq:
                tk0 = tqdm(enumerate(dataloader), total=len(dataloader), leave=False, desc='Iterations', disable=(not verbose))
                epoch_loss = defaultdict(float)
                for i, (x, y, idx) in tk0:
                    x, y = x.float().to(device), y.long().to(device)

                    # loss
                    z, mu, var = self.encoder(x)
                    recon_x = self.decoder(z, y)
                    recon_loss = F.binary_cross_entropy(recon_x, x) * x.size(-1)  ## TO DO
                    kl_loss = kl_div(mu, var) 
            
                    loss = {'recon_loss':recon_loss, 'kl_loss':0.5*kl_loss} 
                    
                    optim.zero_grad()
                    sum(loss.values()).backward()
                    optim.step()
                    
                    for k,v in loss.items():
                        epoch_loss[k] += loss[k].item()
                        
                    info = ','.join(['{}={:.3f}'.format(k, v) for k,v in loss.items()])
                    tk0.set_postfix_str(info)
                    

                epoch_loss = {k:v/(i+1) for k, v in epoch_loss.items()}
                epoch_info = ','.join(['{}={:.3f}'.format(k, v) for k,v in epoch_loss.items()])
                tq.set_postfix_str(epoch_info) 
                    
                early_stopping(sum(epoch_loss.values()), self)
                if early_stopping.early_stop:
                    print('EarlyStopping: run {} epoch'.format(epoch+1))
                    break       
                    
        
                