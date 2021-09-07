from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Imageez application
# - Inherits dataprocess.CPluginProcessInterface from Imageez API
# --------------------
class NeuralStyleTransfer(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        from NeuralStyleTransfer.NeuralStyleTransfer_process import NeuralStyleTransferProcessFactory
        # Instantiate process object
        return NeuralStyleTransferProcessFactory()

    def getWidgetFactory(self):
        from NeuralStyleTransfer.NeuralStyleTransfer_widget import NeuralStyleTransferWidgetFactory
        # Instantiate associated widget object
        return NeuralStyleTransferWidgetFactory()
