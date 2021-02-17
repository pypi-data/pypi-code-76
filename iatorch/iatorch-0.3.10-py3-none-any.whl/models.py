import sys
from io import StringIO
import warnings
import torch
import torch.nn as nn
import pytorch_lightning as pl
from iatorch.utils import parser
from iatorch.loggers.mlflow import IAMLFlowLogger

################################################################################################################################
# TEMPORARY
#
################################################################################################################################
# silence
class NullIO(StringIO):
    def write(self, txt):
        pass
         
# get name of class
def classname(cls):
    if isinstance(cls, type):
        _name = str(cls).strip("'<>'")
    else:
        _name = str(cls.__class__).strip("'<>'")
    return _name.rsplit('.', 1)[-1]

# get mlflow logger
def get_mlflow_logger(loggers):
    mlflow_logger = None
    loggers = loggers if isinstance(loggers, list) else [loggers]
    for logger in loggers:
        if isinstance(logger, IAMLFlowLogger):
            mlflow_logger = logger
    return mlflow_logger


################################################################################################################################
# LIGHTNING MODULES
#
################################################################################################################################

################################################################################################
# BasicModel
################################################################################################
class BasicModel(pl.LightningModule):
    '''
    (BasicModel) 1개 모델만을 사용하는 Model Module
    '''
    
    def __init__(self, num_classes, model, pretrained, criterion, optimizer, lr, momentum, betas, weight_decay, metrics):
        super().__init__()

        # print off
        __stdout = sys.stdout; sys.stdout = NullIO()
        
        self.num_classes = num_classes
        self.model = parser.model(model, num_classes, pretrained)
        self.criterion = parser.criterion(criterion)
        self.is_binary = parser.is_binary(criterion)
        optim_params = {
            k: v for k, v in {'lr': lr, 'momentum': momentum, 'betas': betas, 'weight_decay': weight_decay}.items() if v is not None
        }
        self.Optimizer, optim_params = parser.optimizer(optimizer, **optim_params)
        self.activation = torch.sigmoid if self.is_binary else nn.Softmax(-1)
        
        # manual hparams
        self.hparams.num_classes = num_classes
        self.hparams.model = str(self.model.__class__).strip("'<>'").split('.')[-1]
        if 'efficientnet' in model.lower():
            self.hparams.model = f"{self.hparams.model}-{model.rsplit('-', 1)[-1].upper()}"
        self.hparams.pretrained = pretrained
        self.hparams.criterion = classname(self.criterion)
        self.hparams.optimizer = classname(self.Optimizer)
        self.hparams.optim_params = optim_params
        
        # set metrics 
        self.metrics = nn.ModuleDict()
        if not isinstance(metrics, dict):
            metrics = {m: {} for m in metrics}
        for _name, kwargs in metrics.items():        
            _instance = parser.metric(_name, num_classes=self.num_classes, is_binary=self.is_binary, **kwargs)
            self.metrics[classname(_instance)] = _instance
            
        # set artifacts
        
            
        # helper
        self.sanity_check_done = False
        self.current_step = 'init'
        
        # print on
        sys.stdout = __stdout
        
        
    ################################################################
    # Calls
    ################################################################
    def forward(self, x):
        '''
        PyTorch Lightning의 foward는 Training이 아닌 Prediction에 사용 - Activation Function을 달고 있음
        Training 시 model의 계산은 training, validation, test step에서 별도로 작성하여 수행
        '''
        x = self.model(x)
        x = self.activation(x)
        return x
    
    def configure_optimizers(self):
        optimizer = self.Optimizer(self.parameters(), **self.hparams.optim_params)
        
        # logging hparams
        self.logger.log_hyperparams(self.hparams)
        
        return optimizer
    
    def info(self):
        print('Check Your Model:')
        for k, v in self.hparams.items():
            print(f'  - {k}: {v}')
        metrics = ', '.join([str(v.__class__).strip("'<>'").split('.')[-1] for k, v in self.metrics.items()])
        print(f"  - metrics: {metrics}")
            
        
    ################################################################
    # log_metrics - custom defined
    ################################################################
    def log_metrics(self):
        for _name, _instance in self.metrics.items():
            self.log(
                f"{self.current_step}/{_name}", _instance.compute(),
                on_step=False, on_epoch=True, logger=True, prog_bar=False,
            )
            _instance.reset()
            
            
    ################################################################
    # CallBacks
    ################################################################
    def on_train_epoch_start(self):
        self.sanity_check_done = True
        self.current_step = 'train'
        
    def on_validation_epoch_start(self):
        # logging - (NOTE!) log before update current_step
        if self.sanity_check_done:
            self.log_metrics()
        self.current_step = 'val'
            
    def validation_epoch_end(self, outputs):
        # logging
        self.log_metrics()
    
    def on_test_epoch_start(self):
        self.current_step = 'test'
        
    def test_epoch_end(self, outputs):
        # logging
        self.log_metrics()
        
        # save model
        self.logger.log_model(self.model)
        
        # save artifacts (only for mlflow logger)
#         mlflow_logger = get_mlflow_logger(self.logger)
#         if mlflow_logger is not None:
#             mlfow_logger.log_model()
                    
    
    ################################################################
    # Training step
    ################################################################
    def training_step(self, batch, batch_idx):
        # calculate
        x, y, fp = batch
        y_hat = self.model(x)
        loss = self.criterion(y_hat, y)
        
        # log loss
        self.log("train/loss", loss, on_step=True, on_epoch=True, logger=True)
        
        # update metric - every step
        preds = self.activation(y_hat)
        for _name, _instance in self.metrics.items():
            _instance.update(preds, y)
            
        return loss
                    
        
    ################################################################
    # Validation step - logging 등을 위해서는 Sanity check 이후인지 확인해야 함
    ################################################################  
    def validation_step(self, batch, batch_idx):
        # calculate
        x, y, fp = batch
        y_hat = self.model(x)
        loss = self.criterion(y_hat, y)
        
        # log loss
        self.log("val/loss", loss, on_step=False, on_epoch=True, logger=True, prog_bar=False)
        
        # update metric - every step
        preds = self.activation(y_hat)
        for _name, _instance in self.metrics.items():
            _instance.update(preds, y)
            
    
    ################################################################
    # Test step
    ################################################################
    def test_step(self, batch, batch_idx):
        
        # calculate
        x, y, fp = batch
        y_hat = self.model(x)
        loss = self.criterion(y_hat, y)
        
        # log loss
        self.log("test/loss", loss, on_step=False, on_epoch=True, logger=True)
        
        # update metric
        preds = self.activation(y_hat)
        for _name, _instance in self.metrics.items():
            _instance.update(preds, y)


################################################################################################
# CallBackTestModel
#   개발용, Callback 동작 시점 체크
################################################################################################
class CallBackTestModel(pl.LightningModule):
    '''
    LightningModule 실험용 모델
    '''
    
    def __init__(self, num_classes, model, pretrained, criterion, optimizer, lr, momentum, betas, weight_decay, metrics):
        super().__init__()
        
        self.num_classes = num_classes
        self.model = parser.model(model, num_classes, pretrained)
        self.criterion = parser.criterion(criterion)
        self.is_binary = parser.is_binary(criterion)
        self.Optimizer, optim_params = parser.optimizer(optimizer, lr, momentum, betas, weight_decay)
        self.activation = torch.sigmoid if self.is_binary else nn.Softmax(-1)
        
        # manual hparams
        self.hparams.num_classes = num_classes
        self.hparams.model = model
        self.hparams.pretrained = pretrained
        self.hparams.criterion = criterion
        self.hparams.optimizer = optimizer
        self.hparams.optim_params = optim_params
        
        # set metrics 
        # metric은 누적 계산이 필요함(state를 기억해야 함)으로 train, val, test 각각에 대해 인스턴스화 되어야 함
        # train, val, test는 ModuleDict key로 사용할 수 없으므로 Train, Val, Test 사용
        self.metrics = nn.ModuleDict()
        for metric_name, kwargs in metrics.items():                
            metric_instance = parser.metric(metric_name, num_classes=self.num_classes, is_binary=self.is_binary, **kwargs)
            self.metrics[metric_name] = metric_instance


    ################################################################
    # Call
    ################################################################
    def forward(self, x):
        '''
        PyTorch Lightning의 foward는 Training이 아닌 Prediction에 사용 - Activation Function을 달고 있음
        Training 시 model의 계산은 training, validation, test step에서 별도로 작성하여 수행
        '''
        x = self.model(x)
        x = self.activation(x)
        return x
    
    def configure_optimizers(self):
        optimizer = self.Optimizer(self.parameters(), **self.hparams.optim_params)
        
        # logging hparams
        self.logger.log_hyperparams(self.hparams)
        
        return optimizer
    
    ################################################################
    # Callbacks - lightning은 아래 순서대로 looping
    ################################################################
    
    # FIT START
    def on_fit_start(self):
        self.i += 1
        print(f"({self.i:02}) on_fit_start")
    
    #### TRAIN START
    def on_train_start(self):
        print(f"({self.i:02}) on_train_start")
        
    ####### TRAIN EPOCH START
    def on_epoch_start(self):
        self.i += 1
        print(f"({self.i:02}) on_epoch_start")
        
    def on_train_epoch_start(self):
        '''
        *_epoch_start는 *_epoch_end다르게 on_<step>_epoch_start만 존재
        '''
        self.i += 1
        print(f"({self.i:02}) on_train_epoch_start")
    
    ########## VALIDATION EPOCH START (inside TRAIN EPOCH)
    def on_validation_epoch_start(self):
        self.i += 1
        print(f"({self.i:02}) on_validation_epoch_start")
        
    ########## VALIDATION EPOCH END (inside TRAIN EPOCH)
    def validation_epoch_end(self, outputs):
        print(f"({self.i:02}) validation_epoch_end")

    ####### TRAIN EPOCH END
    def on_epoch_end(self):
        self.i += 1
        print(f"({self.i:02}) on_epoch_end")
    
    def training_epoch_end(self, outputs):
        '''
        <step>_epoch_end는 outputs를 input으로 받고, on_<step>_epoch_end는 input이 없음
        '''
        print(f"({self.i:02}) training_epoch_end")
        
    #### TRAIN END
    def on_train_end(self):
        print(f"({self.i:02}) on_train_end")
            
    # FIT END
    def on_fit_end(self):
        self.i += 1
        print(f"({self.i:02}) on_fit_end")
