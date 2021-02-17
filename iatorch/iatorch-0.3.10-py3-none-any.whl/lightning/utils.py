import sys, getpass, socket, torch
import pandas as pd
from torchvision import models
from efficientnet_pytorch import EfficientNet
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from functools import partial
from iatorch.audio.utils import make_labels
from pytorch_lightning.callbacks import Callback, EarlyStopping, GpuUsageLogger, ModelCheckpoint
from pytorch_lightning.loggers import MLFlowLogger, TensorBoardLogger


################################################################################################################################
# PARSER
################################################################################################################################
def parser(data_dir, labels, experiment_name, run_name, split_ratio, model, no_pretrained, criterion, optimizer, lr, momentum, betas, weight_decay, 
           batch_size, epochs, monitor, early_stop, patience, tracking_uri, tensorboard, cpu, half_precision, seed):    
    
    ################################################################
    # 0. Parser
    ################################################################
    
    #### Train-Val-Test Split ####
    split_ratio = {s: r for s, r in zip(['train', 'val', 'test'], list(split_ratio)) if r > 0}
    
    #### Pretrained ####
    pretrained = not no_pretrained
    
    #### Criterion
    if criterion.lower().replace('_', '').replace('-', '') in ['crossentropy', 'crossentropyloss']:
        criterion = 'CrossEntropyLoss'
        binary = False
    elif criterion.lower().replace('_', '').replace('-', '') in ["bcewithlogitsloss", "onevsall", "bce"]:
        criterion = "BCEWithLogitsLoss"
        binary = True
    else:
        print(f"ERROR!!! criterion {criterion} is not available")
    
    #### Optimizer
    if optimizer.lower() == 'adam':
        optimizer = 'Adam'
        optimizer_params = {'lr': lr, 'betas': betas, 'weight_decay': weight_decay}
    elif optimizer.lower() == 'adamw':
        optimizer = 'AdamW'
        optimizer_params = {'lr': lr, 'betas': betas, 'weight_decay': weight_decay}
    elif optimizer.lower() == 'sparseadam':
        optimizer = 'SparseAdam'
        optimizer_params = {'lr': lr, 'betas': betas, 'weight_decay': weight_decay}
    elif optimizer.lower() == 'sgd':
        optimizer = 'SGD'
        optimizer_params = {'lr': lr, 'momentum': momentum, 'weight_decay': weight_decay}
    else:
        print(f"ERROR!!! optimizer {optimizer} is not available")
    
    #### Forced CPU mode
    if not cpu:
        gpus = torch.cuda.device_count()
        precision = 16 if half_precision else 32
        distributed_backend = 'ddp' if gpus > 1 else None
    
    min_delta = early_stop
    
    
    ################################################################
    # 1. Logger
    ################################################################
    
    loggers = []

    # MLflow Logger
    if True:
        mlflow_logger = MLFlowLogger(
            experiment_name=experiment_name,
            tracking_uri=tracking_uri,
            tags={
                'mlflow.runName': run_name,
                'mlflow.user': getpass.getuser(),
                'mlflow.source.name': sys.argv[0],
                'data_dir': f'{socket.getfqdn()}:{data_dir}',
                'labels': labels if labels else 'inferred from subdir name',
            }
        )
        loggers.append(mlflow_logger)
        run_id = mlflow_logger.run_id
        
    # Tensorboard logger
    if tensorboard:
        tensorflow_logger = TensorBoardLogger(
            save_dir='./logs',
        )
        loggers.append(tensorflow_logger)
        
    
    ################################################################
    # 1. SET DATA
    ################################################################
    
    #### args data
    args_data = {
#         'run_id': run_id,
        'logger': loggers,
        'batch_size': batch_size,
        'binary': binary,
    }
    
    
    ################################################################
    # 2. SET MODEL
    ################################################################
    
    #### Model
    if 'efficientnet' in model.lower():
        if model == "efficientnet":
            model = "efficientnet-b0"
        base_model = EfficientNet.from_pretrained(model) if pretrained else EfficientNet.from_name(model)
    else:
        base_model = eval(f'models.{model}({pretrained})')
        
    #### Criterion & Optimizer
    criterion = eval(f'nn.{criterion}()')
    optimizer = partial(eval(f'optim.{optimizer}'), **optimizer_params)
        
    #### args model
    args_model = {
        'split_ratio': '|'.join([f"{k}_{v}" for k, v in split_ratio.items()]),
        'base_model': base_model,
        'pretrained': pretrained,
        'batch_size': batch_size,
        'precision': f'{precision}-bit',
        'criterion': criterion,
        'optimizer': optimizer,
    }
    
    ################################################################
    # 3. SET TRAINER
    ################################################################

    #### Callbacks   
    # Early stopping
    early_stop_callback = EarlyStopping(monitor, min_delta, patience)
    # Checkpoint
    checkpoint_callback = ModelCheckpoint(
        filepath='./ckpts/_{epoch:03d}_{val_loss:.3f}_{val_accuracy:.3f}',
        prefix=f'{experiment_name.replace("/", "_")}|{run_name}',
    )
    # Verbose Callbacks
    class VerboseCallback(Callback):
        def on_train_start(self, trainer, pl_module):
            print(' ')
        def on_train_end(self, trainer, pl_module):
            print(' ')
    callbacks = [VerboseCallback()]
    
    #### args trainer
    args_trainer = {
        'gpus': gpus,
        'precision': precision,
        'max_epochs': epochs,
        'checkpoint_callback': checkpoint_callback,
        'early_stop_callback': early_stop_callback,
        'callbacks': callbacks,
        'logger': loggers,
    }
    if distributed_backend:
        arg_trainer['distributed_backend'] = distributed_backend
    
    return split_ratio, args_data, args_model, args_trainer


################################################################################################################################
# PREP LABELS
################################################################################################################################
def prep_labels(datadir, labels=None, split={'train': 0.7, 'val': 0.15, 'test': 0.15}, exts=["wav", "tdms"], use_dask=False, min_sample=1, random_state=777, verbose=True):
    
    # 
    user_labels = labels
    
    # labels inferred from subdirs
    labels = make_labels(datadir, exts=exts, use_dask=use_dask)
    
    # replace label column if labels.csv is given
    if user_labels:
        user_labels = pd.read_csv(user_labels) 
        if 'filename' not in user_labels.columns:
            user_labels['filename'] = [f.rsplit('/', 1)[-1] for f in user_labels['filepath']]
        labels = pd.merge(labels.drop(columns='label'), user_labels[['filename', 'label']], "inner", "filename")
        
    # split labels
    if 'split' not in labels.columns:
        labs = sorted(labels['label'].unique())
        sorted_split = {k: v for k, v in sorted(split.items(), key=lambda item: item[1])}
        
        dfs = []
        for lab in labs:
            dfLab = labels[labels['label']==lab]
            denom = 1
            for i, (split_key, split_ratio) in enumerate(sorted_split.items()):
                n_remains = len(dfLab)
                n = min(n_remains, max(round(n_remains* split_ratio/denom), min_sample))
                dfSplit = dfLab.sample(n=n, random_state=random_state)
                dfSplit['split'] = split_key
                dfs.append(dfSplit)
                dfLab = dfLab.drop(dfSplit.index)
                denom = denom - split_ratio
        labels = pd.concat(dfs)
    
    if verbose:
        print(f'<DATA> {datadir}')
        print(labels.pivot_table('filepath', 'label', 'split', aggfunc='count')[split.keys()].to_markdown())
        print('')
    
    return labels.sort_index()
