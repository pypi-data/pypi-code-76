
import os, librosa, cv2, mlflow
from functools import partial
import pytorch_lightning as pl
from iatorch.audio.utils import encode_labels, one_hot_encode_labels, AudioDataset
from torch.utils.data import DataLoader

########################
# AudioDataModule
########################
class AudioDataModule(pl.LightningDataModule):

    def __init__(self, labels, prep, logger=None, binary=False, batch_size=32, shuffle=True, num_workers=None):
        super().__init__()

        # binary means one-vs-all problem        
        if binary:
            self.labels, self.encoder, self.decoder = one_hot_encode_labels(labels, verbose=False)
        else:
            self.labels, self.encoder, self.decoder = encode_labels(labels, verbose=False)
        
        # save labels.csv
        if logger:
            for l in logger:
                if l.__class__.__name__ == 'MLFlowLogger':
                    run_id = l.run_id
                    run_path = f'./results/{run_id}' 
                    if not os.path.exists(run_path):
                        os.makedirs(run_path, exist_ok=True)
                    labels.to_csv(os.path.join(run_path, 'labels.csv'), index=False, )
                    mlflow.pyfunc.save_model(
                        path=os.path.join(run_path, 'transform'),
                        python_model=prep,
                    )
                    print('Labels Saved on MLflow Server')        
        
        # Split
        split = self.labels['split'].unique().tolist()
        
        self.train_splits = ['train']
        self.val_splits = ['val']
        self.test_splits = ['test']
        
        if ("test" not in split) & ("val" not in split):
            self.test_splits = self.val_splits = ['train']    # (수정할 것) Pytorch lightning doc.에서 validation step 건너뛰는 것 찾아서 적용
        elif "test" not in split:
            self.test_splits = ['val']
        elif "val" not in split:
            self.val_splits = ['train']    # (수정할 것) Pytorch lightning으로 cross validation으로 구현
        
        # Dataset Class
        self.Dataset = AudioDataset
        
        # Prep Function (load & transforms)
        self.train_prep = partial(prep, augment=True)
        self.eval_prep = partial(prep, augment=False)

        # Parameters
        self.num_classes = len(self.encoder)
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers if num_workers else os.cpu_count()//2

    def setup(self, stage):
        if stage == 'fit' or stage is None:
            # dataset for fit
            self.train_dataset = self.Dataset(self.labels[self.labels['split'].isin(self.train_splits)], self.train_prep, )
            self.val_dataset = self.Dataset(self.labels[self.labels['split'].isin(self.val_splits)], self.eval_prep, )
        if stage == 'test' or stage is None:
            self.test_dataset = self.Dataset(self.labels[self.labels['split'].isin(self.test_splits)], self.eval_prep, )

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=self.shuffle, num_workers=self.num_workers)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, num_workers=self.num_workers)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=self.num_workers)
