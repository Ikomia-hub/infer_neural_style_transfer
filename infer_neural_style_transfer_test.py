import logging
import cv2
from ikomia.utils.tests import run_for_test
from infer_neural_style_transfer.utils import model_zoo
from ikomia.core import task

logger = logging.getLogger(__name__)


def test(t, data_dict):
    logger.info("===== Test::infer neural style transfer =====")
    logger.info("----- Use default parameters")
    img = cv2.imread(data_dict["images"]["detection"]["coco"])
    input_img_0 = t.getInput(0)
    input_img_0.setImage(img)
    for method, models in model_zoo.items():
        for model_name, _ in models.items():
            params = task.get_parameters(t)
            params["model_name"] = model_name
            params["method"] = method
            task.set_parameters(t, params)
    return run_for_test(t)
