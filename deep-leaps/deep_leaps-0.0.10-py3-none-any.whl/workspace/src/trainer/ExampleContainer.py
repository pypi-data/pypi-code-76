from deepleaps.app.app import SingletoneInstance, App
from deepleaps.dataloader.DataLoader import DataLoaderController
from deepleaps.trainer.TrainerContainer import TrainerContainer
from deepleaps.ipc.RunningGraphController import RunnableModuleController
from deepleaps.model.BaseModel import BaseModel
from deepleaps.app.app import App
from tqdm import tqdm
import torch
from deepleaps.app.Exceptions import *

class ExampleContainer(TrainerContainer):
    def __init__(self, config):
        super(ExampleContainer, self).__init__(config)

        # REQUIRED
        self.LOSSES = None
        self.OPTIMIZER = None
        self.MODEL = None
        self.VAL_LOSSES = None

    def step(self, sample):
        self.sample = sample
        self.sample = self.MODEL(self.sample)

    def train(self):
        try:
            main_graph = RunnableModuleController.instance().get_current_main_module()
            self.step(next(main_graph.iter))
            self.OPTIMIZER.zero_grad()
            loss = self.LOSSES(self.sample)
            loss.backward()
            self.OPTIMIZER.step()
            main_graph.tqdm.set_postfix_str("loss: {}".format(loss))
            main_graph.total_step += 1
        except StopIteration:
            raise MainGraphStepInterrupt
        return

    def test(self):
        try:
            with torch.no_grad():
                main_graph = RunnableModuleController.instance().get_current_main_module()
                self.step(next(main_graph.iter))
                loss = self.VAL_LOSSES(self.sample)
                main_graph.tqdm.set_postfix_str("loss: {}".format(loss))
                main_graph.total_step += 1
        except StopIteration:
            raise MainGraphStepInterrupt
        return
