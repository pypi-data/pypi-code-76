import os
import time
from datetime import datetime

import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication
from ruamel.yaml import YAML

from ..OpFlowLab import OpFlowLab


class Singleton:
    """Alex Martelli implementation of Singleton (Borg)
    http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html"""
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class opFlowLabConfig(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        if self.hasLoaded():
            pass
        else:
            self.mainFolderPath = None
            self.imageFilePath = None
            self.forwardFolderPath = None
            self.reverseFolderPath = None
            self.segmentationFolderPath = None

            self.velocity_type = "Dense"
            self.extension_type = "*.bin"
            self.velocity_dtype = "float16"
            self.kernel_size = 5

            self.flowMatch_folder = "FlowMatch"
            self.pairwise_threshold_distance = 10
            self.min_object_size = None
            self.max_object_size = None
            self.save_velocities_as_tif = False

            self.flowPath_folder = "flowPath"
            self.start_frame = 0
            self.frames = 10
            self.spacing = 8
            self.max_tracers = None

            self.flowTracer_folder = "FlowTracer"
            self.use_random_tracers = True
            self.save_initial_tracer_pos = True
            self.tracer_no = 10000
            self.grid_spacing = 16
            self.alpha = 0

            self.flowWarp_folder = "FlowWarp"

            self.derivative = None
            self.derivative_matrix = None

            self.colormap = "None"
            self.smoothing = None
            self.colormap_min = -1.5
            self.colormap_max = 1.5

            self.images = []
            self.log_file = ""

            self.action_count = 1

            self.settingsPath = os.path.join(os.path.expanduser("~"), "OpFlowLab_settings.yaml")
            self.executablePath = None

            self.loadSettings()

            self._loaded = True

    def getInstance(self):
        return self._instance

    def hasInstance(self):
        return hasattr(self, "_instance")

    def hasLoaded(self):
        return hasattr(self, "_loaded")

    def setattr(self, attr, value):
        self.__setattr__(attr, value)
        if self.hasInstance:
            setattr(self.getInstance(), attr, value)

    def initialize(self):
        self._instance = OpFlowLab(self.mainFolderPath, self.imageFilePath,
                                   self.forwardFolderPath, self.reverseFolderPath,
                                   self.segmentationFolderPath,
                                   velocity_type=self.velocity_type, velocity_dtype=self.velocity_dtype,
                                   velocity_ext_type=self.extension_type,
                                   image_ext_type="*.tif",
                                   kernel_size=5
                                   )

    def createLogFile(self):
        yaml = YAML()

        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_file = "log-{}.yaml".format(now)

        yaml_dict = {self.mainFolderPath: {}}

        with open(os.path.join(self.mainFolderPath, self.log_file), 'w') as file:
            yaml.dump(yaml_dict, file)

        self.action_count = 1

    def saveParameters(self, action, parameter_list):
        yaml = YAML()

        if not os.path.isfile(os.path.join(self.mainFolderPath, self.log_file)):
            self.createLogFile()

        with open(os.path.join(self.mainFolderPath, self.log_file), 'r') as file:
            yaml_dict = yaml.load(file)

        output_dict = yaml_dict[self.mainFolderPath]
        action_name = "action_{}".format(self.action_count)
        output_dict[action_name] = {"action": action}
        if type(parameter_list) == list:
            for param in parameter_list:
                if param == "start_frame":
                    output_dict[action_name][param] = self.__getattribute__(param)+1
                else:
                    output_dict[action_name][param] = self.__getattribute__(param)
        else:
            for key, value in parameter_list.items():
                output_dict[action_name][key] = value

        yaml_dict[self.mainFolderPath] = output_dict

        with open(os.path.join(self.mainFolderPath, self.log_file), 'w') as file:
            yaml.dump(yaml_dict, file)

        self.action_count += 1

    def loadSettings(self):
        yaml = YAML()

        if not os.path.isfile(self.settingsPath):
            self.saveSettings()

        else:
            with open(self.settingsPath, 'r') as file:
                settings_dict = yaml.load(file)

            self.executablePath = settings_dict["executablePath"]
            self.flowMatch_folder = settings_dict["flowMatch_folder"]
            self.flowPath_folder = settings_dict["flowPath_folder"]
            self.flowWarp_folder = settings_dict["flowWarp_folder"]
            self.flowTracer_folder = settings_dict["flowTracer_folder"]

    def saveSettings(self):
        yaml = YAML()

        settings_dict = {"executablePath": self.executablePath,
                         "flowMatch_folder": self.flowMatch_folder,
                         "flowPath_folder": self.flowPath_folder,
                         "flowWarp_folder": self.flowWarp_folder,
                         "flowTracer_folder": self.flowTracer_folder}

        with open(self.settingsPath, 'w') as file:
            yaml.dump(settings_dict, file)


class opFlowLabWorker(QObject):
    progressSignal = pyqtSignal(int)
    finishSignal = pyqtSignal()
    startSignal = pyqtSignal()
    updateSignal = pyqtSignal()
    timeSignal = pyqtSignal(float)

    def __init__(self):
        super(QObject, self).__init__()
        self.config = opFlowLabConfig()
        self.__abort = False

    def isImageLoaded(self):
        return self.config.hasInstance()

    def runFlowMatch(self):
        self.__abort = False
        self.startSignal.emit()
        try:
            instance = self.config.getInstance()

            # create output folders
            flowx_output_directory = os.path.join(self.config.mainFolderPath, self.config.flowMatch_folder, 'flowx')
            os.makedirs(flowx_output_directory, exist_ok=True)

            flowy_output_directory = os.path.join(self.config.mainFolderPath, self.config.flowMatch_folder, 'flowy')
            os.makedirs(flowy_output_directory, exist_ok=True)

            time_list = np.array([])

            for img_no in range(instance.length-1):
                QCoreApplication.processEvents()

                if self.__abort is True:
                    self.finishSignal.emit()
                    return
                else:
                    start = time.time()
                    self.progressSignal.emit(int(100 * img_no / (instance.length-1)))
                    total_number, matched_number = instance.flowMatch_iteration(img_no,
                                                                                flowx_output_directory, flowy_output_directory,
                                                                                pairwise_threshold_distance=self.config.pairwise_threshold_distance,
                                                                                min_object_size=self.config.min_object_size,
                                                                                max_object_size=self.config.max_object_size,
                                                                                save_velocity_as_tif=self.config.save_velocities_as_tif,
                                                                                )
                    time_list = np.append(time_list, time.time()-start)
                    self.timeSignal.emit(np.mean(time_list)*(instance.length - 1 - (img_no + 1)))

                print("  Frame {}: Matching success - {} out of {} [{:.2f}%]".format(img_no+1, matched_number, total_number,
                                                                                     100*matched_number/total_number))

            self.progressSignal.emit(int((100 * (img_no+1)) / (instance.length-1)))

            print("Updating instance with FlowMatch velocity flows")
            self.config.forwardFolderPath = os.path.join(self.config.mainFolderPath, self.config.flowMatch_folder)
            instance.initialize_forward_velocities(self.config.forwardFolderPath)
            self.updateSignal.emit()
        finally:
            self.finishSignal.emit()

    def runFlowPath(self):
        self.__abort = False
        self.startSignal.emit()
        try:
            instance = self.config.getInstance()
            self.config.images = []

            # create output folders
            flow_trace_folder = os.path.join(self.config.forwardFolderPath, self.config.flowPath_folder)
            os.makedirs(flow_trace_folder, exist_ok=True)

            tracer_pos, all_pos_index, x_array_shape = instance.flowPath_initialization(frames=self.config.frames,
                                                                                        spacing=self.config.spacing,
                                                                                        max_tracers=self.config.max_tracers)

            time_list = np.array([])

            for img_no in range(self.config.start_frame, instance.length - 1):
                QCoreApplication.processEvents()
                if self.__abort is True:
                    self.finishSignal.emit()
                    return
                else:
                    start = time.time()
                    self.progressSignal.emit(int(100 * (img_no - self.config.start_frame)
                                                 / (instance.length - self.config.start_frame - 1)))

                    tracer_pos, output_image = instance.flowPath_iteration(img_no, tracer_pos, all_pos_index, x_array_shape,
                                                                           flow_trace_folder,
                                                                           alpha=self.config.alpha,
                                                                           img_frame=instance.image[img_no],
                                                                           frames=self.config.frames,
                                                                           spacing=self.config.spacing,
                                                                           )

                    self.config.images.append(output_image)
                    self.updateSignal.emit()
                    time_list = np.append(time_list, time.time()-start)
                    self.timeSignal.emit(np.mean(time_list)*(instance.length - 1 - (img_no + 1)))

            self.progressSignal.emit(int(100 * (img_no - self.config.start_frame + 1)
                                         / (instance.length - self.config.start_frame - 1)))
        finally:
            self.finishSignal.emit()

    def runFlowTracer(self):
        self.__abort = False
        self.startSignal.emit()
        try:
            instance = self.config.getInstance()
            self.config.images = []

            output_folder = os.path.join(self.config.forwardFolderPath, self.config.flowTracer_folder)
            os.makedirs(output_folder, exist_ok=True)

            tracer_centroids, color = instance.flowTracer_initialization(save_initial_tracer_pos=self.config.save_initial_tracer_pos,
                                                                         use_random_tracers=self.config.use_random_tracers,
                                                                         tracer_no=self.config.tracer_no,
                                                                         spacing=self.config.grid_spacing,
                                                                         segmentation_filelist=self.config.segmentationFolderPath,
                                                                         )

            time_list = np.array([])

            for img_no in range(self.config.start_frame, instance.length - 1):
                QCoreApplication.processEvents()
                if self.__abort is True:
                    self.finishSignal.emit()
                    return
                else:
                    start = time.time()
                    self.progressSignal.emit(int(100 * (img_no - self.config.start_frame)
                                                 / (instance.length - self.config.start_frame - 1)))

                    if img_no == self.config.start_frame:
                        # save first image
                        output_image = instance.flowTracer_first_frame(output_folder,
                                                                       self.config.start_frame,
                                                                       tracer_centroids, color,
                                                                       )
                        self.config.images.append(output_image)

                    tracer_centroids, output_image = instance.flowTracer_iteration(output_folder,
                                                                                   img_no,
                                                                                   tracer_centroids, color,
                                                                                   )

                    self.config.images.append(output_image)
                    self.updateSignal.emit()
                    time_list = np.append(time_list, time.time()-start)
                    self.timeSignal.emit(np.mean(time_list)*(instance.length - 1 - (img_no + 1)))

            self.progressSignal.emit(int(100 * (img_no - self.config.start_frame + 1)
                                         / (instance.length - self.config.start_frame - 1)))
        finally:
            self.finishSignal.emit()

    def runFlowWarp(self):
        self.__abort = False
        self.startSignal.emit()
        try:
            instance = self.config.getInstance()
            self.config.images = []

            output_folder = os.path.join(self.config.forwardFolderPath, self.config.flowWarp_folder)
            os.makedirs(output_folder, exist_ok=True)

            time_list = np.array([])

            for img_no in range(self.config.start_frame, instance.length - 1):
                QCoreApplication.processEvents()
                if self.__abort is True:
                    self.finishSignal.emit()
                    return
                else:
                    start = time.time()
                    self.progressSignal.emit(int(100 * (img_no - self.config.start_frame)
                                                 / (instance.length - self.config.start_frame - 1)))

                    nrmse, output_image = instance.flowWarp_iteration(img_no, output_folder)
                    print("Frame {}: Normalized root mean squared error = {}".format(img_no + 1, nrmse))

                    output_image = np.moveaxis(output_image, 0, -1)
                    display_image = np.zeros(output_image.shape[:2] + (3,))
                    display_image[..., :2] = output_image
                    self.config.images.append(display_image)
                    self.updateSignal.emit()
                    time_list = np.append(time_list, time.time() - start)
                    self.timeSignal.emit(np.mean(time_list) * (instance.length - 1 - (img_no + 1)))

            self.progressSignal.emit(int(100 * (img_no - self.config.start_frame + 1)
                                         / (instance.length - self.config.start_frame - 1)))
        finally:
            self.finishSignal.emit()

    def runDerivative(self):
        self.__abort = False
        self.startSignal.emit()
        try:
            instance = self.config.getInstance()
            self.config.images = []

            # create output folders
            output_folder = os.path.join(self.config.forwardFolderPath, self.config.derivative)
            os.makedirs(output_folder, exist_ok=True)
            derivative_string = '{derivative}_{{:03d}}.tif'.format(derivative=self.config.derivative)

            time_list = np.array([])

            for img_no in range(self.config.start_frame, instance.length - 1):
                QCoreApplication.processEvents()
                if self.__abort is True:
                    self.finishSignal.emit()
                    return
                else:
                    start = time.time()
                    self.progressSignal.emit(int(100 * (img_no - self.config.start_frame)
                                                 / (instance.length - self.config.start_frame - 1)))

                    output_image = instance.flowDerivative_iteration(output_folder, img_no,
                                                                     self.config.derivative_matrix,
                                                                     derivative_string,
                                                                     smoothing=self.config.smoothing,
                                                                     colormap_min=self.config.colormap_min,
                                                                     colormap_max=self.config.colormap_max,
                                                                     colormap=self.config.colormap,
                                                                     )

                    self.config.images.append(output_image)
                    self.updateSignal.emit()
                    time_list = np.append(time_list, time.time()-start)
                    self.timeSignal.emit(np.mean(time_list)*(instance.length - 1 - (img_no + 1)))

            self.progressSignal.emit(int(100 * (img_no - self.config.start_frame + 1)
                                         / (instance.length - self.config.start_frame - 1)))
        finally:
            self.finishSignal.emit()

    def terminateCalculation(self):
        self.__abort = True
