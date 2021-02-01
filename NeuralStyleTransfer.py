from ikomia import dataprocess
import NeuralStyleTransfer_process as processMod
import NeuralStyleTransfer_widget as widgetMod


#--------------------
#- Interface class to integrate the process with Imageez application
#- Inherits dataprocess.CPluginProcessInterface from Imageez API
#--------------------
class NeuralStyleTransfer(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        #Instantiate process object
        return processMod.NeuralStyleTransferProcessFactory()

    def getWidgetFactory(self):
        #Instantiate associated widget object
        return widgetMod.NeuralStyleTransferWidgetFactory()
