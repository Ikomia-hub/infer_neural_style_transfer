from ikomia import utils, core, dataprocess
from ikomia.utils import qtconversion
from infer_neural_style_transfer.infer_neural_style_transfer_process import NeuralStyleTransferParam
import os
import cv2
from imutils import paths
# PyQt GUI framework
from PyQt5.QtWidgets import *
from infer_neural_style_transfer.utils import model_zoo

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


# --------------------
# - Class which implements widget associated with the process
# - Inherits core.CProtocolTaskWidget from Imageez API
# --------------------
class NeuralStyleTransferWidget(core.CWorkflowTaskWidget):

    def __init__(self, param, parent):
        core.CWorkflowTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = NeuralStyleTransferParam()
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

        # Combobox for method
        label_method = QLabel("Select your method")
        self.combo_method = QComboBox()
        self.fill_combo_method()
        self.combo_method.currentTextChanged.connect(self.on_method_changed)
        self.combo_method.setCurrentText(self.parameters.method)
        self.on_method_changed(1)

        # Fill layout
        self.grid_layout.addWidget(label_backend, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.combo_backend, 0, 1, 1, 1)
        self.grid_layout.addWidget(label_target, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.combo_target, 1, 1, 1, 1)
        self.grid_layout.addWidget(label_method, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.combo_method, 2, 1, 1, 1)
        self.grid_layout.addWidget(label_model, 3, 0, 1, 1)
        self.grid_layout.addWidget(self.combo_model, 3, 1, 1, 1)

        # PyQt -> Qt wrapping
        layout_ptr = qtconversion.PyQtToQt(self.grid_layout)

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

    def fill_combo_method(self):
        for method in ["eccv16", "instance_norm"]:
            self.combo_method.addItem(method)

    def on_backend_changed(self, index):
        backend = self.combo_backend.currentData()
        self.fill_combo_target(backend)
        self.param_changed = True

    def on_param_changed(self, index):
        self.param_changed = True

    def on_method_changed(self, index):
        available_models = [k for k, v in model_zoo[self.combo_method.currentText()].items()]
        self.combo_model.clear()
        for model in available_models:
            self.combo_model.addItem(model)
        if self.parameters.model in available_models:
            self.combo_model.setCurrentText(self.parameters.model)
        else:
            self.combo_model.setCurrentText(available_models[0])

    def onApply(self):
        # Apply button has been pressed
        # Get parameters from widget
        self.parameters.update = True
        self.parameters.backend = self.combo_backend.currentData()
        self.parameters.target = self.combo_target.currentData()
        self.parameters.method = self.combo_method.currentText()
        self.parameters.model = self.combo_model.currentText()
        # Send signal to launch the process
        self.emitApply(self.parameters)


# --------------------
# - Factory class to build process widget object
# - Inherits dataprocess.CWidgetFactory from Imageez API
# --------------------
class NeuralStyleTransferWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "infer_neural_style_transfer"

    def create(self, param):
        # Create widget object
        return NeuralStyleTransferWidget(param, None)
