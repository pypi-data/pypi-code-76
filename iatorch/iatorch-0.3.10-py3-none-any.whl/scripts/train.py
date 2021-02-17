import click, os, logging
import cv2, torch
from nptdms import TdmsFile
from iautils.audio import transforms as iat    # audio.transforms는 모든 image.transforms를 내부에서 load
from torchvision.transforms import ToTensor

from ..utils import parser
from ..db.utils import require_local_database
from ..data import MediaFolderDataLoader
from ..models import BasicModel
from ..trainers import BasicTrainer


################################################################################################################################
# TRAIN SCRIPTS
#
################################################################################################################################

################################################################
# image folder
################################################################
def train_image_folder(
    data_dir,
    # data options
    val_ratio=0.2, augments='basic', no_shuffle=False,
    # model & criterion
    model='efficientnet-b0', no_pretrained=False, criterion='bce',
    # optimizer
    optimizer='adam', automatic_optimization=False, lr=0.01, momentum=0.9, betas=(0.9, 0.99), weight_decay=0,
    # batch, epochs, and early stopping
    batch_size=8, min_epochs=1, max_epochs=100, monitor='val/loss', early_stop=0, patience=5,
    # set devices
    num_workers=None, cpu=False, half_precision=False, 
    # reproducability
    seed=None,
    # logging
    results_dir='results', experiment_name='Default', run_name='noname', user=None,
    # etc.
    silence=False,
    # return trainer before train
    return_=False,
):
    '''
    주이진 이미지 폴더를 데이터셋으로 Transfer Learning 수행
    (Note) 이미지 폴더는 train/OK, train/NG, ..., test/OK, test/NG, ... 과 같이 'split/label' 구조로 되어 있어야 함
    
    '''

    ##############################################################################################
    # 0. Initialize
    #     임의수정 불필요
    ##############################################################################################
    
    # SET SEED - 재현성 확보를 위한 random seed 설정
    if seed is not None:
        pl.seed_everything(seed)

        
    ##############################################################################################
    # 1. SET loader & transform
    #     filepath로부터 model의 input data를 생성 (filepath - (loader) -> numpy array -> (transform) -> tensor)
    ##############################################################################################
    # SET LOADER
    def loader(fp):
        return cv2.imread(fp)

    # SET FEATURE EXTRACTION TRANSFORM
    transform = {
        'train': iat.Compose([iat.Resize((224, 224)), ]),
        'test': iat.Compose([iat.Resize((224, 224)), ]),
    }

    # ADD AUGMENTATIONS - train transforms only
    augments_ = parser.augmentations(augments)
    if augments_ is not None:
        transform['train'].transforms.extend(augments_)

    # pytorch 사용 시에 마지막 transform은 반드시 ToTensor()
    for k, v in transform.items():
        v.transforms.append(ToTensor())


    ##############################################################################################
    # 2. SET dataset (trainset, testset)
    #     주어진 data_dir의 하위 폴더 'train'으로부터 trainset, 'test'로부터 testset 생성 (자동)
    ##############################################################################################
    # SET DATALOADER ARGUMENTS
    data_args = {
        'criterion': criterion,      # binary, multi-class or multi-label 구분을 위해 필요
        'val_ratio': val_ratio,      # trainset을 train/validation으로 나눌 때 validation ratio 
        'batch_size': batch_size,
        'shuffle': not no_shuffle,
        'num_workers': num_workers,
        'pin_memory': True if not cpu and torch.cuda.is_available() else False,
    }

    # CREATE DATALOADER
    data = MediaFolderDataLoader(data_dir, loader=loader, transform=transform, **data_args)

    # PRINT DATA INFO
    data.info()
    print('')


    ##############################################################################################
    # 3. SET model
    #     model 이름, criterion 이름, optimizer 이름과 parameter로부터 학습 모델 생성 (자동)
    ##############################################################################################
    # SET MODEL ARGUMENTS
    model_args = {
        'model': model,
        'pretrained': not no_pretrained,
        'criterion': criterion,
        'optimizer': optimizer,
        'lr': lr,
        'momentum': momentum,
        'betas': betas,
        'weight_decay': weight_decay,
        'metrics': ['acc', 'f1', 'precision', 'recall'],
    }

    # CREATE MODEL
    model = BasicModel(num_classes=data.num_classes, **model_args)

    # PRINT MODEL INFO
    model.info()
    print('')


    ##############################################################################################
    # 4. SET logger and trainer
    #     logger 및 trainer 설정
    ##############################################################################################
    # train arguments
    train_args = {
        # logger info
        'experiment_name': experiment_name,
        'run_name': run_name,
        'user': user,
        'data_dir': data_dir,
        'results_dir': results_dir,
        # batchs, epochs, and early stopping
        'batch_size': batch_size,
        'min_epochs': min_epochs,
        'max_epochs': max_epochs,
        'monitor': monitor,
        'early_stop': early_stop,
        'patience': patience,
        # set devices
        'cpu': cpu,
        'half_precision': half_precision,
        # etc
        'silence': silence,
    }

    # CREATE TRAINER
    trainer = BasicTrainer(**train_args)

    # PRINT TRAINER INFO
    trainer.info()
    print('')

    if return_:
        return data, model, trainer

    ##############################################################################################
    # 5. DO TRAIN
    # 
    ##############################################################################################
    print("[START TRAINING]")
    trainer.fit(model, data)
    trainer.test()
    
    return True


################################################################################################################################
# CLI - CLICK
#
################################################################################################################################

################################################################
# train
################################################################
@click.group()
def cli():
    pass
    

################################################################
# cli > train > image_folder
################################################################
@cli.command()
@click.pass_context
@click.argument('data-dir', type=click.Path(exists=True))
@click.option('-o', '--results-dir', default='./results', type=str, show_default=True, help='MLflow trackinng uri')
@click.option('-v', '--val-ratio', default=0.2, type=float, show_default=True, help='Validation Ratio of Trainset')
@click.option('--augments', default='basic', type=str, show_default=True, help='Select Augmentations')
@click.option('--no-shuffle', is_flag=True, show_default=True, help='Do Not Shuffle Train Dataloader')
@click.option('-m', '--model', default='mobilenet_v2', type=str, show_default=True, help='Select a Network Model')
@click.option('--no-pretrained', is_flag=True, show_default=True, help='Not Using Pretrained Weights')
@click.option('-b', '--batch-size', default=16, type=int, show_default=True, help='Batch Size')
@click.option('--min-epochs', default=1, type=int, show_default=True, help='Maximum Epochs')
@click.option('-e', '--max-epochs', default=100, type=int, show_default=True, help='Maximum Epochs')
@click.option('-c', '--criterion', default='CrossEntropy', type=str, show_default=True, help='Select a Loss Function')
@click.option('--optimizer', default='Adam', type=str, show_default=True, help='Select a Optimizer')
@click.option('--lr', default=0.001, type=float, show_default=True, help='Learning Rate for Optimizer')
@click.option('--momentum', default=0.9, type=float, show_default=True, help='Momentum for Optimizer')
@click.option('--betas', default=(0.9, 0.99), nargs=2, type=(float, float), show_default=True, help='Betas for Optimizer')
@click.option('--weight-decay', default=0, type=float, show_default=True, help='Weight Decay for Optimzier')
@click.option('--monitor', default='val/loss', type=str, show_default=True, help='Monitored Value, e.g. var_loss, var_accuracy')
@click.option('--early-stop', default= 0.01, type=float, show_default=True, help='Early Stop Criterion')
@click.option('--patience', default=3, type=int, show_default=True, help='Early Stop Patience Number')
@click.option('--num-workers', default=None, show_default=True, help='Number of Workers for Data Preprocessing')
@click.option('--cpu', is_flag=True, show_default=True, help='Forced CPU Mode')
@click.option('--half-precision', is_flag=True, show_default=True, help='Half Precision (16-bit) Learning')
@click.option('--seed', default=None, type=int, show_default=True, help='Fixed Random Seed for Reproducibility')
@click.option('-n', '--experiment-name', default='Default', show_default=True, help='Project Name, e.g. sound/cooktop, vision/ddrotor')
@click.option('-r', '--run-name', default=None, show_default=True, help='Run Name for Logging, e.g. hparams_tuning')
@click.option('--user', default=None, show_default=True, help='Username')
@click.option('--silence', is_flag=True, show_default=True, help='Progress Bar Off')
def image_folder(ctx, data_dir, **kwargs):
    train_image_folder(data_dir, **kwargs)
    

################################################################################################################################
# main
#
################################################################################################################################
if __name__=="__main__":
    cli(obj={})
