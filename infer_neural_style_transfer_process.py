from ikomia import core, dataprocess
import imutils
import copy
import cv2
import os
from infer_neural_style_transfer.utils import model_zoo, download_model
from distutils.util import strtobool


# --------------------
# - Class to handle the process parameters
# - Inherits core.CProtocolTaskParam from Ikomia API
# --------------------
class NeuralStyleTransferParam(core.CWorkflowTaskParam):

    def __init__(self):
        core.CWorkflowTaskParam.__init__(self)
        # Place default value initialization here
        self.model_path = ""
        self.image_path = ""
        self.update = False
        self.backend = cv2.dnn.DNN_BACKEND_DEFAULT
        self.target = cv2.dnn.DNN_TARGET_CPU
        self.method = "instance_norm"
        self.model = "candy"

    def setParamMap(self, paramMap):
        # Set parameters values from Ikomia application
        # Parameters values are stored as string and accessible like a python dict
        self.model_path = str(paramMap["model_path"])
        self.image_path = str(paramMap["image_path"])
        self.method = str(paramMap["method"])
        self.model = str(paramMap["model"])
        self.update = strtobool(paramMap["update"])

    def getParamMap(self):
        # Send parameters values to Ikomia application
        # Create the specific dict structure (string container)
        paramMap = core.ParamMap()
        paramMap["model_path"] = str(self.model_path)
        paramMap["image_path"] = str(self.image_path)
        paramMap["method"] = str(self.method)
        paramMap["model"] = str(self.model)
        paramMap["update"] = str(self.update)
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
        self.addOutput(dataprocess.CImageIO())

        # Create parameters class
        if param is None:
            self.setParam(NeuralStyleTransferParam())
        else:
            self.setParam(copy.deepcopy(param))

    def getProgressSteps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        return 1

    def globalInputChanged(self, new_sequence):
        if new_sequence:
            param = self.getParam()
            param.update = True

    def run(self):
        # Core function of your process
        # Call beginTaskRun for initialization
        self.beginTaskRun()

        # Get input (image):
        input_img = self.getInput(0)

        # Get output (image)
        output_img = self.getOutput(0)
        output_model_img= self.getOutput(1)

        # Get parameters
        param = self.getParam()

        # Get plugin folder
        plugin_folder = os.path.dirname(os.path.abspath(__file__))

        # Load the neural style transfer model from disk
        if self.net is None or param.update:
            model_path = os.path.join(plugin_folder, "models", param.method, param.model+".t7")
            if not os.path.isfile(model_path):
                print("Downloading model...")
                download_model(param.method, param.model, os.path.join(plugin_folder, "models"))
            self.net = cv2.dnn.readNetFromTorch(model_path)
            self.net.setPreferableBackend(param.backend)
            self.net.setPreferableTarget(param.target)
            param.update = False

        # Load the input_img image, resize it to have a width of 600 pixels, and
        # then grab the image dimensions
        src_image = input_img.getImage()   
        (h_src, w_src) = src_image.shape[:2]   
        src_image = imutils.resize(src_image, width=600)
        (h, w) = src_image.shape[:2]

        # Construct a blob from the image, set the input_img, and then perform a
        # forward pass of the network
        blob = cv2.dnn.blobFromImage(src_image, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
        self.net.setInput(blob)
        dst_image = self.net.forward()

        # Reshape the output tensor, add back in the mean subtraction, and
        # then swap the channel ordering
        dst_image = dst_image.reshape((3, dst_image.shape[2], dst_image.shape[3]))
        dst_image[0] += 103.939
        dst_image[1] += 116.779
        dst_image[2] += 123.680
        dst_image /= 255.0
        dst_image = dst_image.transpose(1, 2, 0)

        # Our image is RGB so we must swap the result and resize it to the original size
        dst_image = cv2.cvtColor(dst_image, cv2.COLOR_RGB2BGR)
        dst_image = cv2.resize(dst_image, (w_src, h_src))
        output_img.setImage(dst_image)

        # set output image as current image model
        image_path = os.path.join(plugin_folder, "images", model_zoo[param.method][param.model]["img"])
        image_model = cv2.imread(image_path)
        if image_model is not None:
            image_model = cv2.cvtColor(image_model, cv2.COLOR_RGB2BGR)
            output_model_img.setImage(image_model)
        else:
            print("Error loading model image.")

        # Step progress bar:
        self.emitStepProgress()

        # Call endTaskRun to finalize process
        self.endTaskRun()


# --------------------
# - Factory class to build process object
# - Inherits dataprocess.CProcessFactory from Ikomia API
# --------------------
class NeuralStyleTransferFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set process information as string here
        self.info.name = "infer_neural_style_transfer"
        self.info.shortDescription = "Neural network method to paint given image in the style of the reference image."
        self.info.description = "Neural style transfer is an optimization technique used to take two images—a content image " \
                                "and a style reference image (such as an artwork by a famous painter)—and blend them together so the output image looks like the content image, " \
                                "but 'painted' in the style of the style reference image. " \
                                "This is implemented by optimizing the output image to match the content statistics of the content image " \
                                "and the style statistics of the style reference image. These statistics are extracted from the images using a convolutional network. " \
                                "Implementation : Adrian Rosebrock." 
        # relative path -> as displayed in Ikomia application process tree
        self.info.path = "Plugins/Python/Art"
        self.info.version = "1.0.1"
        self.info.iconPath = "icon/icon.png"
        self.info.authors = "Justin Johnson, Alexandre Alahi, Li Fei-Fei"
        self.info.article = "Perceptual Losses for Real-Time Style Transfer and Super-Resolution."
        self.info.journal = "ECCV"
        self.info.year = 2016
        self.info.license = "Free for personal or research use only"
        self.info.documentationLink = "https://www.pyimagesearch.com/2018/08/27/neural-style-transfer-with-opencv/"
        self.info.repository = "https://github.com/jcjohnson/fast-neural-style"
        self.info.keywords = "art,painting,deep learning"

    def create(self, param=None):
        # Create process object
        return NeuralStyleTransfer(self.info.name, param)
