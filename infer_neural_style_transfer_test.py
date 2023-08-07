import logging
import cv2
from ikomia.utils.tests import run_for_test
from infer_neural_style_transfer.utils import model_zoo

logger = logging.getLogger(__name__)


def test(t, data_dict):
    logger.info("===== Test::infer neural style transfer =====")
    logger.info("----- Use default parameters")
    img = cv2.imread(data_dict["images"]["detection"]["coco"])
    input_img_0 = t.get_input(0)
    input_img_0.set_image(img)
    for method, models in model_zoo.items():
        for model_name, _ in models.items():
            params = t.get_parameters()
            params["model_name"] = model_name
            params["method"] = method
            t.set_parameters(params)
    return run_for_test(t)
