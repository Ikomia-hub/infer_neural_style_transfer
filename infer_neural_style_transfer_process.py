from ikomia import core, dataprocess
import imutils
import copy
import cv2
import os
import numpy as np
from infer_neural_style_transfer.utils import model_zoo, download_model


# --------------------
# - Class to handle the process parameters
# - Inherits core.CProtocolTaskParam from Ikomia API
# --------------------
class NeuralStyleTransferParam(core.CWorkflowTaskParam):

    def __init__(self):
        core.CWorkflowTaskParam.__init__(self)
        # Place default value initialization here
        self.update = False
        self.backend = cv2.dnn.DNN_BACKEND_DEFAULT
        self.target = cv2.dnn.DNN_TARGET_CPU
        self.method = "instance_norm"
        self.model_name = "candy"

    def set_values(self, paramMap):
        # Set parameters values from Ikomia application
        # Parameters values are stored as string and accessible like a python dict
        self.backend = int(paramMap["backend"])
        self.target = int(paramMap["target"])
        self.method = str(paramMap["method"])
        self.model_name = str(paramMap["model_name"])
        self.update = True

    def get_values(self):
        # Send parameters values to Ikomia application
        # Create the specific dict structure (string container)
        paramMap = {}
        paramMap["method"] = str(self.method)
        paramMap["model_name"] = str(self.model_name)
        paramMap["backend"] = str(self.backend)
        paramMap["target"] = str(self.target)
        return paramMap


# --------------------
# - Class which implements the process
# - Inherits core.CProtocolTask or derived from Ikomia API
# --------------------
class NeuralStyleTransfer(dataprocess.C2dImageTask):

    def __init__(self, name, param):
        dataprocess.C2dImageTask.__init__(self, name)
        self.net = None
        # Add input_img/output of the process here
        self.add_output(dataprocess.CImageIO())

        # Create parameters class
        if param is None:
            self.set_param_object(NeuralStyleTransferParam())
        else:
            self.set_param_object(copy.deepcopy(param))

    def get_progress_steps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        return 1

    def run(self):
        # Core function of your process
        # Call begin_task_run for initialization
        self.begin_task_run()

        # Get input (image):
        input_img = self.get_input(0)

        # Get output (image)
        output_img = self.get_output(0)
        output_model_img = self.get_output(1)

        # Get parameters
        param = self.get_param_object()

        # Get plugin folder
        plugin_folder = os.path.dirname(os.path.abspath(__file__))

        # Load the neural style transfer model from disk
        if self.net is None or param.update:
            model_path = os.path.join(plugin_folder, "models", param.method, param.model_name + ".t7")
            if not os.path.isfile(model_path):
                print("Downloading model...")
                download_model(param.method, param.model_name, os.path.join(plugin_folder, "models"))
            self.net = cv2.dnn.readNetFromTorch(model_path)
            self.net.setPreferableBackend(param.backend)
            self.net.setPreferableTarget(param.target)
            # temporary fix for a bug in net.forward when model is not reloaded
            #param.update = False

        # Load the input_img image, resize it to have a width of 600 pixels, and
        # then grab the image dimensions
        src_image = input_img.get_image()   
        (h_src, w_src) = src_image.shape[:2]   
        src_img_resize = imutils.resize(src_image, width=600)
        (h, w) = src_img_resize.shape[:2]

        # Construct a blob from the image, set the input_img, and then perform a
        # forward pass of the network
        blob = cv2.dnn.blobFromImage(src_img_resize, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
        self.net.setInput(blob)
        dst_image = self.net.forward()

        # Reshape the output tensor, add back in the mean subtraction, and
        # then swap the channel ordering
        dst_image = dst_image.reshape((3, dst_image.shape[2], dst_image.shape[3]))
        dst_image[0] += 103.939
        dst_image[1] += 116.779
        dst_image[2] += 123.680
        dst_image = dst_image.transpose(1, 2, 0)

        # Conversion float to uint8
        max_value = np.max(dst_image, axis=(0, 1))
        max_value= np.where(max_value > 255, max_value, 255)
        min_value = np.min(dst_image, axis=(0, 1))
        min_value = np.where(0 > min_value, min_value, 0)
        dst_image = (dst_image - min_value) / (max_value - min_value) * 255
        dst_image = dst_image.astype(dtype='uint8')

        # Our image is RGB so we must swap the result and resize it to the original size
        dst_image = cv2.cvtColor(dst_image, cv2.COLOR_RGB2BGR)
        dst_image = cv2.resize(dst_image, (w_src, h_src))
        output_img.set_image(dst_image)

        # set output image as current image model
        image_path = os.path.join(plugin_folder, "images", model_zoo[param.method][param.model_name]["img"])
        image_model = cv2.imread(image_path)
        if image_model is not None:
            image_model = cv2.cvtColor(image_model, cv2.COLOR_RGB2BGR)
            output_model_img.set_image(image_model)
        else:
            print("Error loading model image.")

        # Step progress bar:
        self.emit_step_progress()

        # Call end_task_run to finalize process
        self.end_task_run()


# --------------------
# - Factory class to build process object
# - Inherits dataprocess.CProcessFactory from Ikomia API
# --------------------
class NeuralStyleTransferFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set process information as string here
        self.info.name = "infer_neural_style_transfer"
        self.info.short_description = "Neural network method to paint given image in the style of the reference image."
        # relative path -> as displayed in Ikomia application process tree
        self.info.path = "Plugins/Python/Art"
        self.info.version = "1.1.3"
        self.info.icon_path = "icon/icon.png"
        self.info.authors = "Justin Johnson, Alexandre Alahi, Li Fei-Fei"
        self.info.article = "Perceptual Losses for Real-Time Style Transfer and Super-Resolution."
        self.info.journal = "ECCV"
        self.info.year = 2016
        self.info.license = "Free for personal or research use only"
        self.info.documentation_link = "https://www.pyimagesearch.com/2018/08/27/neural-style-transfer-with-opencv/"
        self.info.repository = "https://github.com/Ikomia-hub/infer_neural_style_transfer"
        self.info.original_repository = "https://github.com/jcjohnson/fast-neural-style"
        self.info.keywords = "art,painting,deep learning"
        self.info.algo_type = core.AlgoType.INFER
        self.info.algo_tasks = "IMAGE_GENERATION"

    def create(self, param=None):
        # Create process object
        return NeuralStyleTransfer(self.info.name, param)
