from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Imageez application
# - Inherits dataprocess.CPluginProcessInterface from Imageez API
# --------------------
class IkomiaPlugin(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        from infer_neural_style_transfer.infer_neural_style_transfer_process import NeuralStyleTransferFactory
        # Instantiate process object
        return NeuralStyleTransferFactory()

    def getWidgetFactory(self):
        from infer_neural_style_transfer.infer_neural_style_transfer_widget import NeuralStyleTransferWidgetFactory
        # Instantiate associated widget object
        return NeuralStyleTransferWidgetFactory()
