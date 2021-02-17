
import sys, os, time
from functools import partial
import pytorch_lightning as pl
import torchvision.models as models
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from pytorch_lightning.metrics import functional as FM
import mlflow.pytorch


################################################################
#### TransferModel
################################################################
class TransferModel(pl.LightningModule):

    def __init__(self, num_classes, decoder=None, split_ratio=None, batch_size=None, precision=None, base_model=models.mobilenet_v2(True), pretrained=True, optimizer=optim.Adam, criterion=F.cross_entropy):
        super().__init__()
        
        # Data
        self.num_classes = num_classes
        self.decoder = decoder if decoder else {k: v for k, v in enumerate(range(num_classes))}
        self.split_ratio = split_ratio
                
        # Model
        self.base_model = base_model
        
        # Last Classifier
        base_model_output_shape = None
        for i in [-1, -2]:
            last_params = list(list(base_model.children())[i].parameters())
            if len(last_params) > 0:
                base_model_output_shape = last_params[-1].shape[0]
                break
        if not base_model_output_shape:
            sys.exit("Cannot find output shape of base_model!")
        self.classifier = nn.Linear(base_model_output_shape, self.num_classes)
        
        # Optimizer
        self.optimizer = optimizer
        self.criterion = criterion
        
        # Custom Metrics
        def get_metrics(y_hat, y):
            # For Binary Cross Entropy
            if y.dim() > 1:
                y_hat = F.sigmoid(y_hat).round()
                accuracies = dict(); precisions = dict(); recalls = dict()
                for i, c in self.decoder.items():
                    accuracies[c] = FM.accuracy(y_hat[:, i], y[:, i], num_classes=2)   # each class is binary
                    precisions[c] = FM.precision(y_hat[:, i], y[:, i], num_classes=2)   # each class is binary
                    recalls[c] = FM.recall(y_hat[:, i], y[:, i], num_classes=2)   # each class is binary
                accuracy = torch.stack(list(accuracies.values())).mean()
                precision = torch.stack(list(precisions.values())).mean()
                recall = torch.stack(list(recalls.values())).mean()
            # For Cross Entropy
            else:
                accuracy = FM.accuracy(y_hat, y, self.num_classes)
                precision = FM.precision(y_hat, y, self.num_classes)
                recall = FM.recall(y_hat, y, self.num_classes)
                recalls = None
            return accuracy, precision, recall, recalls
        
        self.get_metrics = get_metrics
        
        # Hyper Parameters (for logging)
        self.hparams = {
            'split_ratio': split_ratio,
            'num_classes': num_classes,
            'base_model': base_model.__class__.__name__,
            'pretrained': pretrained,
            'classifier': str(self.classifier),
            'batch_size': batch_size,
            'precision': precision,
            'criterion': criterion.__name__ if hasattr(criterion, '__name__') else str(criterion).strip('()'),   # LASTEST MODIFY
            'optimizer': optimizer.func.__name__ if type(optimizer) is partial else optimizer.__class__.__name__,
            **optimizer.keywords
        }
    
    #### MODEL - forward ####
    def forward(self, x):
        x = self.base_model(x)
        x = F.relu(x)
        x = self.classifier(x)
        return x
    
    #### OPTIMIZER ####
    def configure_optimizers(self):
        optimizer = self.optimizer(self.parameters())
        return optimizer    
    
    #### SAVE MODEL ####
    ## save when test is done
    def teardown(self, stage):
        if stage == 'test':
            for logger in self.logger:
                if logger.__class__.__name__ == 'MLFlowLogger':
                    run_id = logger.run_id
                    mlflow.pytorch.save_model(self, f'./results/{run_id}/model')
                    logger.experiment.log_artifacts(logger.run_id, f'./results/{run_id}')
                    print('Artifacts Saved on MLflow Server')
        
    #### LEARNING LOOP - training ####
    def training_step(self, batch, batch_idx):
        x, y, f = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        
        ## LOGGING
        result = pl.TrainResult(loss)
        accuracy, precision, recall, recalls = self.get_metrics(y_hat, y)
        
        for metric in ['accuracy', 'precision', 'recall']:
            result.log(f'train_{metric}', eval(metric), on_step=False, on_epoch=True, reduce_fx=torch.mean, sync_dist=True)

        return result

    #### LEARNING LOOP - validation ####
    def validation_step(self, batch, batch_idx):
        x, y, f = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)        
        
        ## LOGGING
        result = pl.EvalResult(checkpoint_on=loss)
        accuracy, precision, recall, recalls = self.get_metrics(y_hat, y)
        for metric in ['loss', 'accuracy', 'precision', 'recall']:
            result.log(f'val_{metric}', eval(metric), prog_bar=False, sync_dist=True)

        return result

    #### LEARNING LOOP - test ####
    def test_step(self, batch, batch_idx):
        x, y, f = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)        
        
        ## LOGGING
        result = pl.EvalResult()
        accuracy, precision, recall, recalls = self.get_metrics(y_hat, y)
        for metric in ['loss', 'accuracy', 'precision', 'recall']:
            result.log(f'test_{metric}', eval(metric), prog_bar=False, sync_dist=True)

        return result
