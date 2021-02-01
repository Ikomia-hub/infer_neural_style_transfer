from ikomia import utils, core, dataprocess
import NeuralStyleTransfer_process as processMod
import os
import cv2
from imutils import paths

#PyQt GUI framework
from PyQt5.QtWidgets import *


backend_names = {
    cv2.dnn.DNN_BACKEND_DEFAULT: "Default",
    cv2.dnn.DNN_BACKEND_HALIDE: "Halide",
    cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE: "Inference engine",
    cv2.dnn.DNN_BACKEND_OPENCV: "OpenCV",
    cv2.dnn.DNN_BACKEND_VKCOM: "VKCOM",
    cv2.dnn.DNN_BACKEND_CUDA: "CUDA",
}

target_names = {
    cv2.dnn.DNN_TARGET_CPU: "CPU",
    cv2.dnn.DNN_TARGET_OPENCL: "OpenCL FP32",
    cv2.dnn.DNN_TARGET_OPENCL_FP16: "OpenCL FP16",
    cv2.dnn.DNN_TARGET_MYRIAD: "MYRIAD",
    cv2.dnn.DNN_TARGET_VULKAN: "VULKAN",
    cv2.dnn.DNN_TARGET_FPGA: "FPGA",
    cv2.dnn.DNN_TARGET_CUDA: "CUDA FP32",
    cv2.dnn.DNN_TARGET_CUDA_FP16: "CUDA FP16",
}

backend_targets = {
    cv2.dnn.DNN_BACKEND_DEFAULT: [cv2.dnn.DNN_TARGET_CPU, cv2.dnn.DNN_TARGET_OPENCL, cv2.dnn.DNN_TARGET_OPENCL_FP16],
    cv2.dnn.DNN_BACKEND_HALIDE: [cv2.dnn.DNN_TARGET_CPU],
    cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE: [cv2.dnn.DNN_TARGET_CPU],
    cv2.dnn.DNN_BACKEND_OPENCV: [cv2.dnn.DNN_TARGET_CPU, cv2.dnn.DNN_TARGET_OPENCL, cv2.dnn.DNN_TARGET_OPENCL_FP16],
    cv2.dnn.DNN_BACKEND_VKCOM: [cv2.dnn.DNN_TARGET_CPU],
    cv2.dnn.DNN_BACKEND_CUDA: [cv2.dnn.DNN_TARGET_CUDA, cv2.dnn.DNN_TARGET_CUDA_FP16],
}

#--------------------
#- Class which implements widget associated with the process
#- Inherits core.CProtocolTaskWidget from Imageez API
#--------------------
class NeuralStyleTransferWidget(core.CProtocolTaskWidget):

    def __init__(self, param, parent):
        core.CProtocolTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = processMod.NeuralStyleTransferProcessParam()
        else:
            self.parameters = param

        self.param_changed = False

        # Create layout : QGridLayout by default
        self.grid_layout = QGridLayout()

        # Combobox for inference backend
        label_backend = QLabel("DNN backend")
        self.combo_backend = QComboBox()
        self.fill_combo_backend() 
        self.combo_backend.setCurrentIndex(self.combo_backend.findData(self.parameters.backend))
        self.combo_backend.currentIndexChanged.connect(self.on_backend_changed)

        # Combobox for inference target
        label_target = QLabel("DNN target")
        self.combo_target = QComboBox()
        self.fill_combo_target(self.parameters.backend)
        self.combo_target.setCurrentIndex(self.combo_target.findData(self.parameters.target))
        self.combo_target.currentIndexChanged.connect(self.on_param_changed)

        # Combobox for models
        label_model = QLabel("Select your model")
        self.combo_model = QComboBox()
        self.fill_combo_model()
        self.combo_model.currentIndexChanged.connect(self.on_param_changed)
        
        try:
            current_index = self.model_paths.index(self.parameters.model_path)
            self.combo_model.setCurrentIndex(current_index)
        except:
            self.combo_model.setCurrentIndex(0)            
        
        # Fill layout
        self.grid_layout.addWidget(label_backend, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.combo_backend, 0, 1, 1, 1)
        self.grid_layout.addWidget(label_target, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.combo_target, 1, 1, 1, 1)
        self.grid_layout.addWidget(label_model, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.combo_model, 2, 1, 1, 1)

        # PyQt -> Qt wrapping
        layout_ptr = utils.PyQtToQt(self.grid_layout)

        # Set widget layout
        self.setLayout(layout_ptr)

    def fill_combo_backend(self):
        for backend in backend_names:            
            self.combo_backend.addItem(backend_names[backend], backend)

    def fill_combo_target(self, backend):
        targets = backend_targets[backend]
        self.combo_target.clear()

        for target in targets:
            self.combo_target.addItem(target_names[target], target)

    def fill_combo_model(self):
        # Grab the paths to all neural style transfer models in our 'models'
        # directory, provided all models end with the '.t7' file extension
        model_path = os.path.dirname(os.path.realpath(__file__))+"/models"
        self.image_path = os.path.dirname(os.path.realpath(__file__))+"/images/"
        self.model_paths = paths.list_files(model_path, validExts=(".t7",))
        self.model_paths = sorted(list(self.model_paths))

        for i in range(len(self.model_paths)):
            tmp = os.path.basename(self.model_paths[i])
            model_path = os.path.splitext(tmp)[0]
            self.combo_model.addItem(model_path)

    def on_backend_changed(self, index):
        backend = self.combo_backend.currentData()
        self.fill_combo_target(backend)
        self.param_changed = True

    def on_param_changed(self, index):
        self.param_changed = True

    def onApply(self):
        # Apply button has been pressed
        # Get parameters from widget
        self.parameters.update = self.param_changed
        self.parameters.backend = self.combo_backend.currentData()
        self.parameters.target = self.combo_target.currentData()
        self.parameters.model_path = self.model_paths[self.combo_model.currentIndex()]
        self.parameters.image_path = self.image_path + self.combo_model.currentText() + ".jpg"
        # Send signal to launch the process
        self.emitApply(self.parameters)


#--------------------
#- Factory class to build process widget object
#- Inherits dataprocess.CWidgetFactory from Imageez API
#--------------------
class NeuralStyleTransferWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "NeuralStyleTransfer"

    def create(self, param):
        # Create widget object
        return NeuralStyleTransferWidget(param, None)
