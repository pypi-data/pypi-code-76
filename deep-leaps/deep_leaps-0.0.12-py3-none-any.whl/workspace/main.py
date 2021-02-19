import torch
from deepleaps.app.app import App
from deepleaps.dataloader.DataLoader import DataLoaderController
from deepleaps.trainer.TrainerContainer import TrainerContainer
from deepleaps.ipc.ThreadCommand import MultipleProcessorController
from deepleaps.ipc.RunningGraphController import RunnableModuleController
import os

print('Device id: ', torch.cuda.current_device())
print('Available: ', torch.cuda.is_available())
print('Property: ', torch.cuda.get_device_properties(0))

def main(configs):
    if isinstance(configs, list):
        App.register_from_config_list(configs)
    else:
        App.register(configs)
        App.instance().update()
    DataLoaderController.register()
    command_controller = RunnableModuleController.register()

#    App.instance().config.App.DEBUG = True
    try:
        command_controller.run()
    except Exception as e:
        print(e)
    finally:
        MultipleProcessorController.instance().remove_all_process()

if __name__ == '__main__':
    config_list_paths = ['resource/configs/default.yaml']
    main(config_list_paths)