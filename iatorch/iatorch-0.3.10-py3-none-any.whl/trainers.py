import sys, socket, getpass
from datetime import datetime
import importlib
import sys

import torch
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ProgressBar
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning.callbacks.model_checkpoint import ModelCheckpoint
from .db.utils import require_local_database
from .loggers.mlflow import IAMLFlowLogger

if importlib.util.find_spec('ipywidgets') is not None:
    from tqdm.auto import tqdm
else:
    from tqdm import tqdm

################################################################################################################################
# CALLBACKS
#   PyTorch-Lightning Callbacks for Trainer
################################################################################################################################

################################################################
# Progress bar - default progress bar 사용 시 print line 밀리는 것 보완 (validation progress bar off)
################################################################
class SimpleProgressBar(ProgressBar):
    '''
    pytorch-lightning의 ProgressBar 사용 시 valiation epoch마다 line break 발생하여 print 지저분해짐
    SimpleProgressBar는 validation epoch의 progress bar를 off하여 line break 문제 회피
    '''
    
    def init_validation_tqdm(self):
        """ Override this to customize the tqdm bar for validation. """
        bar = tqdm(
            desc='Validating',
            position=(2 * self.process_position + 1),
            disable=True, # self.is_disabled,
            leave=False,
            dynamic_ncols=True,
            file=sys.stdout
        )
        return bar
    
    def on_validation_start(self, trainer, pl_module):
        super().on_validation_start(trainer, pl_module)
        if not trainer.running_sanity_check:
            self._update_bar(self.main_progress_bar)  # fill up remaining

    def on_validation_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx):
        super().on_validation_batch_end(trainer, pl_module, outputs, batch, batch_idx, dataloader_idx)
        if self._should_update(self.val_batch_idx, self.total_val_batches):
            self._update_bar(self.main_progress_bar)

    def on_validation_end(self, trainer, pl_module):
        super().on_validation_end(trainer, pl_module)
        self.main_progress_bar.set_postfix(trainer.progress_bar_dict)
        
    
################################################################################################################################
# TRAINER MODULES
#   PyTorch-Lightning Trainer
################################################################################################################################

################################################################
# BasicTrainer
################################################################
class BasicTrainer(Trainer):
    '''
    BasicTrainer, pytorch_lightning trainer에 logger, progress_bar callback만 정의해서 넘기는 형태
    Main code 간결하게 하기 위해서 따로 뽑음
    '''
    
    def __init__(
        self, 
        # logger
        experiment_name='Default', run_name=None, user=None, data_dir=None, results_dir='results',
        # batch, epochs and early stopping
        batch_size=8, min_epochs=1, max_epochs=100, monitor='var/loss', early_stop=0, patience=3,
        # set devices
        cpu=False, half_precision=False,
        # etc
        silence=False,
    ):  
        # parse tracking_uri and artifact_root (weights_save_path)
        tracking_uri, artifact_root = require_local_database(results_dir)
        
        # [LOGGER] set logger
        logger = IAMLFlowLogger(
            tracking_uri=tracking_uri, artifact_root=artifact_root, experiment_name=experiment_name,
            tags={
                'mlflow.runName': run_name if run_name is not None else datetime.now().strftime('%Y%m%d%H%M%S'), 
                'mlflow.user': getpass.getuser() if user is None else user, 
                'mlflow.source.name': sys.argv[0].rsplit('/', 1)[-1], 
                'data': f"{socket.getfqdn()}:{data_dir if data_dir is not None else '<unknown>'}",
            },
        )

        # [CALLBACK] set early-stopping
        early_stopping = EarlyStopping(monitor=monitor, min_delta=early_stop, patience=patience, mode='max')
        
        # [CALLBACK] set progress bar
        bar = SimpleProgressBar()
        
        # SET TRAINER ARGUMENTS
        gpus = torch.cuda.device_count() if not cpu else 0
        accelerator = 'ddp' if gpus > 1 else None
        precision = 16 if half_precision and gpus != 0 else 32
        train_args = {
            'gpus': gpus,
            'accelerator': accelerator,
            'precision': precision,
            'min_epochs': min_epochs,
            'max_epochs': max_epochs,
            'logger': logger,
            'callbacks': [early_stopping, bar, ], # bar
            'log_every_n_steps': int(128/batch_size),            # data 128개 학습마다 log
            'flush_logs_every_n_steps': int(1024/batch_size),    # data 1,024개 학습마다 write log
            'weights_summary': None,
            'weights_save_path': artifact_root,
        }
        
        # init 
        super(BasicTrainer, self).__init__(**train_args)
        if silence:
            self.progress_bar_callback.disable()
        
    def info(self):
        '''
        Traniner의 Summary 출력
        '''
        _early = None
        for cb in self.callbacks:
            if isinstance(cb, EarlyStopping):
                _early = cb
        
        _mlflow_logger = None
        if isinstance(self.logger, list):
            for cb in self.logger:
                if isinstance(cv, IAMLFlowLogger):
                    _mlflow_logger = cb
        else:
            if isinstance(self.logger, IAMLFlowLogger):
                _mlflow_logger = self.logger
            
        print(f"Check Your Trainer:")
        print(f"  - Max epochs is {self.max_epochs}.")
        if _early is not None:
            print(f"  - Stop early when the decrease in '{_early.monitor}' is below {_early.min_delta} for {_early.patience} times.")
        if _mlflow_logger is not None:
            print(f"  - MlFLow logger is ready.")
            print(f"    . (tracking_uri:experiment_name) {_mlflow_logger._tracking_uri}:{_mlflow_logger._experiment_name}")
            print(f"    . (artifact_root) {_mlflow_logger._mlflow_client._tracking_client.store.artifact_root_uri}")
        print(f"  - Train on {self.gpus} gpu(s) w/ {self.precision}-bit precision")
