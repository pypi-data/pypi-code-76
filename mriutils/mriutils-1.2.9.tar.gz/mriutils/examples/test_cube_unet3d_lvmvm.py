#!/usr/bin/env python

import sys
sys.path.append("..")

# [0] configure
data_path = 'lvmvm/'
save_path = 'processed/lvmvm/'
input_shape = (50, 128, 128, 4)
label_shape = (50, 128, 128, 1)
channels = 4
n_classes = 2
save_name = 'cube_unet3d_1000e_2b.hdf5'
save_path = 'processed/lvmvm/pred/'

# [1] process data
from datasets.lvmvm import LoadH5
lh5 = LoadH5(data_path, save_path)
data = lh5.read()
lh5.save()

# [2] load data
from utils.load_data import LoadData
ld = LoadData(save_path)
ld.load_data_dict()
train, test, mode_list = ld.data_split()

from utils.resize import Resize
res = Resize(train, 'data', input_shape)
train = res.run()
res = Resize(test, 'label', label_shape)
test = res.run()

# [3] build the model
from models.modules.losses import Loss
from models.modules.metrics import Metric
from models.cube_unet3d import CUBE_UNet3D
model = CUBE_UNet3D(input_shape, model_level = 2, n_classes = 2, loss = 'dice', metric = 'dice')

# [4] train the model
from train import Train
training = Train(model, train, channels, n_classes)
training.train(mode_list[0], mode_list[1], epochs = 1000, batch_size = 2, save_name = save_name)

# [5] test the model
from test import Test
testing = Test(model, save_name, channels, n_classes, test)
testing.test(mode_list[0], mode_list[1], save_path)
