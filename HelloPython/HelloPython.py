import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
#from PyQt4.QtWidgets import (QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem)
from qt import (QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem)
from girder_client import GirderClient
import sys

apiUrl='http://192.168.0.11:8080/api/v1'
username = 'aaaa'
password = 'abc123'

#
# HelloPython
#


class HelloPython(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "HelloPython" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    #self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.contributors = ["Yuli Zhang (Z2AI.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
It performs a simple thresholding on the input volume and optionally captures a screenshot.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# HelloPythonWidget
#

class HelloPythonWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)




    ##########################   add by zyl
    # HelloWorld button
    helloWorldButton = qt.QPushButton("Hello World!")
    helloWorldButton.toolTip = "Print 'Hello World' in standard output."
    parametersFormLayout.addWidget(helloWorldButton)
    helloWorldButton.connect('clicked(bool)', self.onHelloWorldButtonClicked)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.helloWorldButton = helloWorldButton


    ############ add a button for test
    #Tree Test
    treeButton = qt.QPushButton("Show the Tree")
    treeButton.toolTip = "Print 'this is a tree button.'"
    parametersFormLayout.addWidget(treeButton)
    treeButton.connect('clicked(bool)', self.onTreeButtonClicked)
    #treeButton.connect('clicked(bool)', self.onHelloWorldButtonClicked)

    self.layout.addStretch(1)
    self.treeButton = treeButton

    #############  add test end

  def onHelloWorldButtonClicked(self):
    logic = HelloPythonLogic()
    result = logic.process()
    qt.QMessageBox.information(slicer.util.mainWindow(),
                               'Slicer Test Python', result)


    ########## for onTreeButtonClicked
  def onTreeButtonClicked(self):
    logic = Girder_python(apiUrl, username, password)
    tree = TreeWidgetDemo(logic)
    #result = logic.print_folder(tree_info, 0)
    tree.show()
    qt.QMessageBox.information(slicer.util.mainWindow(),
                               'Tree', result)


    ##########  onTreeButtonClicked end
    ############################  add end



    # parametersFormLayout.addRow("Image threshold", self.imageThresholdSliderWidget)

    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    self.enableScreenshotsFlagCheckBox.checked = 0
    self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = HelloPythonLogic()
    enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    imageThreshold = self.imageThresholdSliderWidget.value
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), imageThreshold, enableScreenshotsFlag)

#
# HelloPythonLogic
#

class HelloPythonLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
#####  add by  zyl
  def process(self):
    return "Hello world!"

  def process1(self):
    return "lalalalaal!"

#####    add end

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    slicer.util.delayDisplay('Take screenshot: '+description+'.\nResult is available in the Annotations module.', 3000)

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == slicer.qMRMLScreenShotDialog.FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog.ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog.Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog.Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog.Green:
      # green slice window
      widget = lm.sliceWidget("Green")
    else:
      # default to using the full window
      widget = slicer.util.mainWindow()
      # reset the type so that the node is set correctly
      type = slicer.qMRMLScreenShotDialog.FullLayout

    # grab and convert to vtk image data
    qimage = ctk.ctkWidgetsUtils.grabWidget(widget)
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, 1, imageData)

  def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

    # Capture screenshot
    if enableScreenshots:
      self.takeScreenshot('HelloPythonTest-Start','MyScreenshot',-1)

    logging.info('Processing completed')

    return True





######################### add class Girder_python by zyl

#
#   Girder_python
#

class Girder_python(GirderClient):
# -----------------------------Init------------------------

  def __init__(self, apiUrl, username, password):
    super(Girder_python, self).__init__(apiUrl=apiUrl)
    self.authenticate(username, password)

# ---------------------------Get foder structure----------------------------
  def get_folder_structure(self, id, is_collection=False):
    if is_collection:
      folder_list = self.listFolder(id, parentFolderType='collection')
      item_list = None
    else:
      folder_list = self.listFolder(id, parentFolderType='folder')
      item_list = self.listItem(id, text=None, name=None, limit=None, offset=None)

    l = []
    for folder in folder_list:
      t = (folder['_id'], folder['name'], 'folder', self.get_folder_structure(folder['_id'], False))
      l.append(t)

    if item_list:
      for item in item_list:
        t = (item['_id'], item['name'], 'item', [])
        l.append(t)

    #print(l)
    return l

  def get_all_collections(self):
    collection_list = self.listCollection()
    l = []
    for collection in collection_list:
      t = (collection['_id'], collection['name'], 'collection', self.get_folder_structure(collection['_id'], True))
      l.append(t)

    #print(l)
    return ('000000', 'root', 'root', l)


  def print_folder(self, entity, level):
    print('{}{}_{}'.format('+' * (level * 5), entity[1], entity[0]))
    # pdb.set_trace()
    for i in entity[3]:
      # pdb.set_trace()
      self.print_folder(i, level + 1)


# -----------------------------class TreeWidgetDemo------------------------
class TreeWidgetDemo(QMainWindow):

  def create_node(self, root, entity):
    child = QTreeWidgetItem(root)
    child.setText(0, entity[1])
    child.setToolTip(0, '{}_{}'.format(entity[0], entity[2]))
    for grandson in entity[3]:
      self.create_node(child, grandson)

    return child

  # ---Init------------------------------------------------------------------
  def __init__(self, gc, parent=None):
    self.gc = gc

    super(TreeWidgetDemo, self).__init__(parent)
    self.setWindowTitle('girder_Structure')
    self.tree = QTreeWidget()
    self.tree.setHeaderLabels(['GirderTree'])

    tree_info = Girder_python.get_all_collections(gc)
    root = self.create_node(self.tree, tree_info)
    self.tree.addTopLevelItem(root)
    self.tree.clicked.connect(self.onTreeClicked)

    self.setCentralWidget(self.tree)

  # ---OnTreeClicked------------------------------------------------------------------
  def onTreeClicked(self, qmodelindex):
    item = self.tree.currentItem()
    name = item.text(0)
    id_girder, type_girder = item.toolTip(0).split('_')
    print("name={}, id={}, type={}".format(name, id_girder, type_girder))

    if type_girder != 'item':
      return

    print("start to download item")
    download_path = 'girder_download'
    if not os.path.exists(download_path):
      os.makedirs(download_path)
    self.gc.downloadItem(id_girder, download_path)
    print("finish downloading item")