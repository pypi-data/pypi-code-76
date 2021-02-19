#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: octid.py
# Author: Litao Yang, Yanan Wang
# Mail: litao.yang@monash.edu, yanan.wang1@monash.edu
# Created Time:  2021-2-1 21:40:00
#############################################

import torch
import torch.nn as nn
import torchvision.models as models
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader, ConcatDataset
from matplotlib import pyplot
from itertools import cycle
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import umap
from sklearn import svm
import os, random, shutil

class octid:
    def __init__(self, model = 'googlenet',customised_model = False, feature_dimension = 3, outlier_fraction_of_SVM = 0.03, traning_dataset=None, validation_dataset=None, unlabeled_dataset=None):
        self.model_name = model
        self.dim = feature_dimension
        self.templates_path = traning_dataset
        self.val_path = validation_dataset
        self.unknown_path = unlabeled_dataset
        self.SVM_nu = outlier_fraction_of_SVM
        if not customised_model:
            if self.model_name == 'alexnet':
                self.model = models.alexnet(pretrained=True)
            elif self.model_name == 'vgg11':
                self.model = models.vgg11(pretrained=True)
            elif self.model_name == 'vgg13':
                self.model = models.vgg13(pretrained=True)
            elif self.model_name == 'vgg16':
                self.model = models.vgg16(pretrained=True)
            elif self.model_name == 'vgg19':
                self.model = models.vgg19(pretrained=True)
            elif self.model_name == 'vgg11_bn':
                self.model = models.vgg11_bn(pretrained=True)
            elif self.model_name == 'vgg13_bn':
                self.model = models.vgg13_bn(pretrained=True)
            elif self.model_name == 'vgg16_bn':
                self.model = models.vgg16_bn(pretrained=True)
            elif self.model_name == 'vgg19_bn':
                self.model = models.vgg19_bn(pretrained=True)
            elif self.model_name == 'resnet18':
                self.model = models.resnet18(pretrained=True)
            elif self.model_name == 'resnet34':
                self.model = models.resnet34(pretrained=True)
            elif self.model_name == 'resnet50':
                self.model = models.resnet50(pretrained=True)
            elif self.model_name == 'resnet101':
                self.model = models.resnet101(pretrained=True)
            elif self.model_name == 'resnet152':
                self.model = models.resnet152(pretrained=True)
            elif self.model_name == 'densenet121':
                self.model = models.densenet121(pretrained=True)
            elif self.model_name == 'densenet169':
                self.model = models.densenet169(pretrained=True)
            elif self.model_name == 'densenet201':
                self.model = models.densenet201(pretrained=True)
            elif self.model_name == 'densenet161':
                self.model = models.densenet161(pretrained=True)
            elif self.model_name == 'inception_v3':
                self.model = models.inception_v3(pretrained=True)
            elif self.model_name == 'googlenet':
                self.model = models.googlenet(pretrained=True)
            elif self.model_name == 'shufflenet_v2_x1_0':
                self.model = models.shufflenet_v2_x1_0(pretrained=True)
            elif self.model_name == 'mobilenet_v2':
                self.model = models.mobilenet_v2(pretrained=True)
            elif self.model_name == 'resnext50_32x4d':
                self.model = models.resnext50_32x4d(pretrained=True)
            elif self.model_name == 'resnext101_32x8d':
                self.model = models.resnext101_32x8d(pretrained=True)
            elif self.model_name == 'wide_resnet50_2':
                self.model = models.wide_resnet50_2(pretrained=True)
            elif self.model_name == 'wide_resnet101_2':
                self.model = models.wide_resnet101_2(pretrained=True)
            elif self.model_name == 'mnasnet1_0':
                self.model = models.mnasnet1_0(pretrained=True)
            else:
                print('model is not available')
        elif customised_model:
            self.model = model
            self.model_name = 'customised_model'
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.Net = self.model
        self.Net.to(self.device)
        self.Net.eval()
        self.modules = self.Net.named_modules()
        for i, j in self.modules:
            self.module = j
        self.module.register_forward_hook(self.hook_fn_forward)
        self.data_transform = transforms.Compose([transforms.CenterCrop(299), transforms.ToTensor()])
        self.templates = torchvision.datasets.ImageFolder(root=self.templates_path, transform=self.data_transform)
        self.templates_dataloader = DataLoader(self.templates, batch_size=1, shuffle=False)

    def __call__(self):
        if self.val_path is None:
            os.mkdir('positive')
            os.mkdir('negative')
            self.unknown = torchvision.datasets.ImageFolder(root=self.unknown_path, transform=self.data_transform)
            self.unknown_dataloader = DataLoader(self.unknown, batch_size=1, shuffle=False)
            self.templates_result_logger = []
            self.templates_lables_logger = []
            self.unknown_result_logger = []
            self.unknown_lables_logger = []
            for i, data in enumerate(self.templates_dataloader):
                self.total_in = []
                temp_data, temp_lables = data
                temp_data = temp_data.to(self.device)
                output_temp = self.Net(temp_data)
                self.templates_lables_logger.append(temp_lables.detach().numpy())
                self.templates_result_logger.append(self.total_in[0][0].cpu().detach().numpy())
            for j, data in enumerate(self.unknown_dataloader):
                self.total_in = []
                unknown_data, unknown_lables = data
                unknown_data = unknown_data.to(self.device)
                output_unknown = self.Net(unknown_data)
                self.unknown_lables_logger.append(unknown_lables.detach().numpy())
                self.unknown_result_logger.append(self.total_in[0][0].cpu().detach().numpy())
            self.templates_lables_total = np.zeros([len(self.templates_dataloader), 1])
            self.templates_result_total = np.zeros(
                [len(self.templates_dataloader), self.templates_result_logger[0].shape[1]])

            for n in range(len(self.templates_dataloader)):
                self.templates_lables_total[n, 0] = self.templates_lables_logger[n]
            for n in range(len(self.templates_dataloader)):
                self.templates_result_total[n, :] = self.templates_result_logger[n]

            self.unknown_lables_total = np.zeros([len(self.unknown_dataloader), 1])
            self.unknown_result_total = np.zeros([len(self.unknown_dataloader), self.unknown_result_logger[0].shape[1]])
            for n in range(len(self.unknown_dataloader)):
                self.unknown_lables_total[n, 0] = self.unknown_lables_logger[n]
            for n in range(len(self.unknown_dataloader)):
                self.unknown_result_total[n, :] = self.unknown_result_logger[n]

            self.total_data = np.r_[self.templates_result_total, self.unknown_result_total]
            self.reducer = umap.UMAP(n_components=self.dim)
            self.embedding = self.reducer.fit_transform(self.total_data)
            self.UMAP_templates = self.embedding[0:len(self.templates_dataloader)]
            self.UMAP_unknown = self.embedding[len(self.templates_dataloader):(
                        len(self.templates_dataloader) + len(self.unknown_dataloader))]
            self.clf = svm.OneClassSVM(nu=self.SVM_nu, kernel='rbf')
            self.clf.fit(self.UMAP_templates)
            self.unknown_pre = self.clf.predict(self.UMAP_unknown)
            for i in range(len(self.unknown_pre)):
                if self.unknown_pre[i] == 1:
                    shutil.copy(self.unknown.imgs[i][0], 'positive')
                else:
                    shutil.copy(self.unknown.imgs[i][0], 'negative')
            if self.dim == 2:
                self.xx, self.yy = np.meshgrid(np.linspace(-10, 20, 5000), np.linspace(-10, 20, 5000))
                self.Z = self.clf.decision_function(np.c_[self.xx.ravel(), self.yy.ravel()])
                self.Z = self.Z.reshape(self.xx.shape)
                self.fig1 = plt.figure(figsize=(10, 8))
                plt.contourf(self.xx, self.yy, self.Z, levels=[0, self.Z.max()], colors='palevioletred')
                plt.scatter(self.UMAP_templates[:, 0], self.UMAP_templates[:, 1], c=self.templates_lables_total,
                            cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_traning'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig1.savefig(
                    'UMAP_projection_of_{}_{}_{}_traning.png'.format(self.model_name, self.dim, self.SVM_nu),
                    bbox_inches='tight', dpi=400)

                self.fig2 = plt.figure(figsize=(10, 8))
                plt.contourf(self.xx, self.yy, self.Z, levels=[0, self.Z.max()], colors='palevioletred')
                plt.scatter(self.UMAP_unknown[:, 0], self.UMAP_unknown[:, 1], c=self.unknown_lables_total,
                            cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_unlabeled'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig1.savefig(
                    'UMAP_projection_of_{}_{}_{}_unlabeled.png'.format(self.model_name, self.dim, self.SVM_nu),
                    bbox_inches='tight', dpi=400)
            else:
                self.fig1 = plt.figure(figsize=(10, 8))
                plt.scatter(self.UMAP_templates[:, 0], self.UMAP_templates[:, 1], c=self.templates_lables_total,
                            cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_traning'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig1.savefig(
                    'UMAP_projection_of_{}_{}_{}_traning.png'.format(self.model_name, self.dim, self.SVM_nu),
                    bbox_inches='tight', dpi=400)

                self.fig2 = plt.figure(figsize=(10, 8))
                plt.scatter(self.UMAP_unknown[:, 0], self.UMAP_unknown[:, 1], c=self.unknown_lables_total,
                            cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_unlabeled'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig2.savefig(
                    'UMAP_projection_of_{}_{}_{}_unlabeled.png'.format(self.model_name, self.dim, self.SVM_nu),
                    bbox_inches='tight', dpi=400)
        elif self.unknown_path is None:
            self.val = torchvision.datasets.ImageFolder(root=self.val_path, transform=self.data_transform)
            self.val_dataloader = DataLoader(self.val, batch_size=1, shuffle=False)
            self.templates_result_logger = []
            self.templates_lables_logger = []
            self.val_result_logger = []
            self.val_lables_logger = []
            for i, data in enumerate(self.templates_dataloader):
                self.total_in = []
                temp_data, temp_lables = data
                temp_data = temp_data.to(self.device)
                output_temp = self.Net(temp_data)
                self.templates_lables_logger.append(temp_lables.detach().numpy())
                self.templates_result_logger.append(self.total_in[0][0].cpu().detach().numpy())
            for k, data in enumerate(self.val_dataloader):
                self.total_in = []
                val_data, val_lables = data
                val_data = val_data.to(self.device)
                output_val = self.Net(val_data)
                self.val_lables_logger.append(val_lables.detach().numpy())
                self.val_result_logger.append(self.total_in[0][0].cpu().detach().numpy())
            self.templates_lables_total = np.zeros([len(self.templates_dataloader), 1])
            self.templates_result_total = np.zeros(
                [len(self.templates_dataloader), self.templates_result_logger[0].shape[1]])
            for n in range(len(self.templates_dataloader)):
                self.templates_lables_total[n, 0] = self.templates_lables_logger[n]
            for n in range(len(self.templates_dataloader)):
                self.templates_result_total[n, :] = self.templates_result_logger[n]
            self.val_lables_total = np.zeros([len(self.val_dataloader), 1])
            self.val_result_total = np.zeros([len(self.val_dataloader), self.val_result_logger[0].shape[1]])
            for n in range(len(self.val_dataloader)):
                self.val_lables_total[n, 0] = self.val_lables_logger[n]
            for n in range(len(self.val_dataloader)):
                self.val_result_total[n, :] = self.val_result_logger[n]
            self.total_data = np.r_[self.templates_result_total, self.val_result_total]
            self.reducer = umap.UMAP(n_components=self.dim)
            self.embedding = self.reducer.fit_transform(self.total_data)
            self.UMAP_templates = self.embedding[0:len(self.templates_dataloader)]
            self.UMAP_val = self.embedding[
                            len(self.templates_dataloader):(len(self.templates_dataloader) + len(self.val_dataloader))]
            self.clf = svm.OneClassSVM(nu=self.SVM_nu, kernel='rbf')
            self.clf.fit(self.UMAP_templates)
            self.val_pre = self.clf.predict(self.UMAP_val)
            self.prediction(self.val_pre, self.val_lables_total)
            self.CM_logger = []
            self.dim_logger = []
            self.acc_logger = []
            self.MCC_logger = []
            self.F_1_logger = []
            self.TP = self.CM[0, 0]
            self.FP = self.CM[0, 1]
            self.TN = self.CM[0, 2]
            self.FN = self.CM[0, 3]
            self.MCC = (self.TP * self.TN - self.FP * self.FN) / (
                        (self.TP + self.FP) * (self.TP + self.FN) * (self.TN + self.FP) * (self.TN + self.FN)) ** (0.5)
            self.F_1 = 2 * self.TP / (2 * self.TP + self.FP + self.FN)
            self.F_1_logger.append(self.F_1)
            self.MCC_logger.append(self.MCC)
            self.acc_logger.append(self.acc)
            self.CM_logger.append(self.CM)
            self.dim_logger.append(self.dim)
            self.CM_A = self.CM_logger[0]
            self.CM_test = pd.DataFrame(data=self.CM_A, columns=['TruePos', 'FalsePos', 'TrueNeg', 'FalseNeg'])
            self.acc_test = pd.DataFrame(data=self.acc_logger, columns=['acc'])
            self.dim_test = pd.DataFrame(data=self.dim_logger, columns=['dim'])
            self.F_1_test = pd.DataFrame(data=self.F_1_logger, columns=['F_1'])
            self.MCC_test = pd.DataFrame(data=self.MCC_logger, columns=['MCC'])
            self.test_prediction = pd.concat([self.dim_test, self.acc_test, self.CM_test, self.F_1_test, self.MCC_test],
                                             axis=1)
            self.test_prediction.to_csv('val_prediction_{}_{}_{}.csv'.format(self.model_name, self.dim, self.SVM_nu))
            if self.dim == 2:
                self.xx, self.yy = np.meshgrid(np.linspace(-10, 20, 5000), np.linspace(-10, 20, 5000))
                self.Z = self.clf.decision_function(np.c_[self.xx.ravel(), self.yy.ravel()])
                self.Z = self.Z.reshape(self.xx.shape)

                self.fig1 = plt.figure(figsize=(10, 8))
                plt.contourf(self.xx, self.yy, self.Z, levels=[0, self.Z.max()], colors='palevioletred')
                plt.scatter(self.UMAP_templates[:, 0], self.UMAP_templates[:, 1], c=self.templates_lables_total,
                            cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_traning'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig1.savefig(
                    'UMAP_projection_of_{}_{}_{}_traning.png'.format(self.model_name, self.dim, self.SVM_nu),
                    bbox_inches='tight', dpi=400)

                self.fig2 = plt.figure(figsize=(10, 8))
                plt.contourf(self.xx, self.yy, self.Z, levels=[0, self.Z.max()], colors='palevioletred')
                plt.scatter(self.UMAP_val[:, 0], self.UMAP_val[:, 1], c=self.val_lables_total, cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_val'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig2.savefig('UMAP_projection_of_{}_{}_{}_val.png'.format(self.model_name, self.dim, self.SVM_nu),
                                  bbox_inches='tight', dpi=400)
            else:
                self.fig1 = plt.figure(figsize=(10, 8))
                plt.scatter(self.UMAP_templates[:, 0], self.UMAP_templates[:, 1], c=self.templates_lables_total,
                            cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_traning'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig1.savefig(
                    'UMAP_projection_of_{}_{}_{}_traning.png'.format(self.model_name, self.dim, self.SVM_nu),
                    bbox_inches='tight', dpi=400)

                self.fig2 = plt.figure(figsize=(10, 8))
                plt.scatter(self.UMAP_val[:, 0], self.UMAP_val[:, 1], c=self.val_lables_total, cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_val'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig2.savefig('UMAP_projection_of_{}_{}_{}_val.png'.format(self.model_name, self.dim, self.SVM_nu),
                                  bbox_inches='tight', dpi=400)
        else:
            os.mkdir('positive')
            os.mkdir('negative')
            self.unknown = torchvision.datasets.ImageFolder(root=self.unknown_path, transform=self.data_transform)
            self.unknown_dataloader = DataLoader(self.unknown, batch_size=1, shuffle=False)
            self.val = torchvision.datasets.ImageFolder(root=self.val_path, transform=self.data_transform)
            self.val_dataloader = DataLoader(self.val, batch_size=1, shuffle=False)
            self.templates_result_logger = []
            self.templates_lables_logger = []
            self.unknown_result_logger = []
            self.unknown_lables_logger = []
            self.val_result_logger = []
            self.val_lables_logger = []
            for i, data in enumerate(self.templates_dataloader):
                self.total_in = []
                temp_data, temp_lables = data
                temp_data = temp_data.to(self.device)
                output_temp = self.Net(temp_data)
                self.templates_lables_logger.append(temp_lables.detach().numpy())
                self.templates_result_logger.append(self.total_in[0][0].cpu().detach().numpy())
            for j, data in enumerate(self.unknown_dataloader):
                self.total_in = []
                unknown_data, unknown_lables = data
                unknown_data = unknown_data.to(self.device)
                output_unknown = self.Net(unknown_data)
                self.unknown_lables_logger.append(unknown_lables.detach().numpy())
                self.unknown_result_logger.append(self.total_in[0][0].cpu().detach().numpy())
            for k, data in enumerate(self.val_dataloader):
                self.total_in = []
                val_data, val_lables = data
                val_data = val_data.to(self.device)
                output_val = self.Net(val_data)
                self.val_lables_logger.append(val_lables.detach().numpy())
                self.val_result_logger.append(self.total_in[0][0].cpu().detach().numpy())
            self.templates_lables_total = np.zeros([len(self.templates_dataloader), 1])
            self.templates_result_total = np.zeros(
                [len(self.templates_dataloader), self.templates_result_logger[0].shape[1]])
            for n in range(len(self.templates_dataloader)):
                self.templates_lables_total[n, 0] = self.templates_lables_logger[n]
            for n in range(len(self.templates_dataloader)):
                self.templates_result_total[n, :] = self.templates_result_logger[n]

            self.unknown_lables_total = np.zeros([len(self.unknown_dataloader), 1])
            self.unknown_result_total = np.zeros([len(self.unknown_dataloader), self.unknown_result_logger[0].shape[1]])
            for n in range(len(self.unknown_dataloader)):
                self.unknown_lables_total[n, 0] = self.unknown_lables_logger[n]
            for n in range(len(self.unknown_dataloader)):
                self.unknown_result_total[n, :] = self.unknown_result_logger[n]

            self.val_lables_total = np.zeros([len(self.val_dataloader), 1])
            self.val_result_total = np.zeros([len(self.val_dataloader), self.val_result_logger[0].shape[1]])
            for n in range(len(self.val_dataloader)):
                self.val_lables_total[n, 0] = self.val_lables_logger[n]
            for n in range(len(self.val_dataloader)):
                self.val_result_total[n, :] = self.val_result_logger[n]

            self.total_data = np.r_[self.templates_result_total, self.unknown_result_total, self.val_result_total]
            self.reducer = umap.UMAP(n_components=self.dim)
            self.embedding = self.reducer.fit_transform(self.total_data)
            self.UMAP_templates = self.embedding[0:len(self.templates_dataloader)]
            self.UMAP_unknown = self.embedding[len(self.templates_dataloader):(
                        len(self.templates_dataloader) + len(self.unknown_dataloader))]
            self.UMAP_val = self.embedding[(len(self.templates_dataloader) + len(self.unknown_dataloader)):(
                        len(self.templates_dataloader) + len(self.unknown_dataloader) + len(self.val_dataloader))]
            self.clf = svm.OneClassSVM(nu=self.SVM_nu, kernel='rbf')
            self.clf.fit(self.UMAP_templates)
            self.unknown_pre = self.clf.predict(self.UMAP_unknown)
            for i in range(len(self.unknown_pre)):
                if self.unknown_pre[i] == 1:
                    shutil.copy(self.unknown.imgs[i][0], 'positive')
                else:
                    shutil.copy(self.unknown.imgs[i][0], 'negative')
            self.val_pre = self.clf.predict(self.UMAP_val)
            self.prediction(self.val_pre, self.val_lables_total)
            self.CM_logger = []
            self.dim_logger = []
            self.acc_logger = []
            self.MCC_logger = []
            self.F_1_logger = []
            self.TP = self.CM[0, 0]
            self.FP = self.CM[0, 1]
            self.TN = self.CM[0, 2]
            self.FN = self.CM[0, 3]
            self.MCC = (self.TP * self.TN - self.FP * self.FN) / (
                        (self.TP + self.FP) * (self.TP + self.FN) * (self.TN + self.FP) * (self.TN + self.FN)) ** (0.5)
            self.F_1 = 2 * self.TP / (2 * self.TP + self.FP + self.FN)
            self.F_1_logger.append(self.F_1)
            self.MCC_logger.append(self.MCC)
            self.acc_logger.append(self.acc)
            self.CM_logger.append(self.CM)
            self.dim_logger.append(self.dim)
            self.CM_A = self.CM_logger[0]
            self.CM_test = pd.DataFrame(data=self.CM_A, columns=['TruePos', 'FalsePos', 'TrueNeg', 'FalseNeg'])
            self.acc_test = pd.DataFrame(data=self.acc_logger, columns=['acc'])
            self.dim_test = pd.DataFrame(data=self.dim_logger, columns=['dim'])
            self.F_1_test = pd.DataFrame(data=self.F_1_logger, columns=['F_1'])
            self.MCC_test = pd.DataFrame(data=self.MCC_logger, columns=['MCC'])
            self.test_prediction = pd.concat([self.dim_test, self.acc_test, self.CM_test, self.F_1_test, self.MCC_test],
                                             axis=1)
            self.test_prediction.to_csv('val_prediction_{}_{}_{}.csv'.format(self.model_name, self.dim, self.SVM_nu))
            if self.dim == 2:
                self.xx, self.yy = np.meshgrid(np.linspace(-10, 20, 5000), np.linspace(-10, 20, 5000))
                self.Z = self.clf.decision_function(np.c_[self.xx.ravel(), self.yy.ravel()])
                self.Z = self.Z.reshape(self.xx.shape)

                self.fig1 = plt.figure(figsize=(10, 8))
                plt.contourf(self.xx, self.yy, self.Z, levels=[0, self.Z.max()], colors='palevioletred')
                plt.scatter(self.UMAP_templates[:, 0], self.UMAP_templates[:, 1], c=self.templates_lables_total,
                            cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_traning'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig1.savefig(
                    'UMAP_projection_of_{}_{}_{}_traning.png'.format(self.model_name, self.dim, self.SVM_nu),
                    bbox_inches='tight', dpi=400)

                self.fig2 = plt.figure(figsize=(10, 8))
                plt.contourf(self.xx, self.yy, self.Z, levels=[0, self.Z.max()], colors='palevioletred')
                plt.scatter(self.UMAP_unknown[:, 0], self.UMAP_unknown[:, 1], c=self.unknown_lables_total,
                            cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_unlabeled'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig2.savefig(
                    'UMAP_projection_of_{}_{}_{}_unlabeled.png'.format(self.model_name, self.dim, self.SVM_nu),
                    bbox_inches='tight', dpi=400)

                self.fig3 = plt.figure(figsize=(10, 8))
                plt.contourf(self.xx, self.yy, self.Z, levels=[0, self.Z.max()], colors='palevioletred')
                plt.scatter(self.UMAP_val[:, 0], self.UMAP_val[:, 1], c=self.val_lables_total, cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_val'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig3.savefig('UMAP_projection_of_{}_{}_{}_val.png'.format(self.model_name, self.dim, self.SVM_nu),
                                  bbox_inches='tight', dpi=400)
            else:
                self.fig1 = plt.figure(figsize=(10, 8))
                plt.scatter(self.UMAP_templates[:, 0], self.UMAP_templates[:, 1], c=self.templates_lables_total,
                            cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_traning'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig1.savefig(
                    'UMAP_projection_of_{}_{}_{}_traning.png'.format(self.model_name, self.dim, self.SVM_nu),
                    bbox_inches='tight', dpi=400)

                self.fig2 = plt.figure(figsize=(10, 8))
                plt.scatter(self.UMAP_unknown[:, 0], self.UMAP_unknown[:, 1], c=self.unknown_lables_total,
                            cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_unlabeled'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig2.savefig(
                    'UMAP_projection_of_{}_{}_{}_unlabeled.png'.format(self.model_name, self.dim, self.SVM_nu),
                    bbox_inches='tight', dpi=400)

                self.fig3 = plt.figure(figsize=(10, 8))
                plt.scatter(self.UMAP_val[:, 0], self.UMAP_val[:, 1], c=self.val_lables_total, cmap='Spectral', s=5)
                plt.gca().set_aspect('equal', 'datalim')
                plt.colorbar(boundaries=np.arange(3) - 0.5).set_ticks(np.arange(3))
                plt.title('UMAP_projection_of_{}_{}_{}_val'.format(self.model_name, self.dim, self.SVM_nu))
                self.fig3.savefig('UMAP_projection_of_{}_{}_{}_val.png'.format(self.model_name, self.dim, self.SVM_nu),
                                  bbox_inches='tight', dpi=400)

    def hook_fn_forward(self, module, input, output):
        self.total_in.append(input)

    def prediction(self, y_pred_test, target_test):
        self.CM = np.zeros([1, 4])
        for i in range(len(y_pred_test)):
            if y_pred_test[i] == -1 and target_test[i] != 0:
                self.CM[0, 2] += 1
            elif y_pred_test[i] == -1 and target_test[i] == 0:
                self.CM[0, 3] += 1
            elif y_pred_test[i] != -1 and target_test[i] == 0:
                self.CM[0, 0] += 1
            elif y_pred_test[i] != -1 and target_test[i] != 0:
                self.CM[0, 1] += 1
        self.acc = (self.CM[0, 0] + self.CM[0, 2]) / len(y_pred_test)
