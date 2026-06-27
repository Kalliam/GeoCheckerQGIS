import os
import sys
import subprocess
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import Qt

# initialize Qt resources from file resources.py
from PyQt6 import uic
from qgis.utils import iface
from .GeoChecker.AppKernel import AppKernel
from qgis.core import Qgis, QgsMapLayerProxyModel, QgsVectorLayer, QgsWkbTypes


FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'geo_checker_dialog.ui'))


class GeoCheckerDialog(QDialog, FORM_CLASS):
    """
    GeoCheckerDialog class represents the main user interface dialog for the GeoChecker plugin.
    It manages user inputs, file selections, and triggers the execution of the checks.

    Attributes:
    ----------
    No explicitly defined attributes. All UI elements are inherited from FORM_CLASS and initialized via setupUi.

    Methods:
    --------
    on_malla_layer_changed(layer):
        Updates the field combo boxes when the grid layer changes in the QGIS import tab.
    
    select_linkage():
        Opens a file dialog to select the linkage shapefile and validates its geometry type.
    
    select_arc():
        Opens a file dialog to select the arc shapefile and validates its geometry type.
    
    select_node():
        Opens a file dialog to select the node shapefile and validates its geometry type.
    
    select_results(tab):
        Opens a directory dialog to select the output folder for the results based on the active tab.
    
    run(tab):
        Retrieves inputs from the user interface, initializes the AppKernel, and executes the checks.
    """
    def __init__(self, parent=None):
        super(GeoCheckerDialog, self).__init__(parent)
        self.setupUi(self)
        
        #btn names of widgets must match QT desgner
        #2nd tab
        self.btn_explore_linkage.clicked.connect(self.select_linkage)
        self.btn_explore_arc.clicked.connect(self.select_arc)
        self.btn_explore_node.clicked.connect(self.select_node)
        self.btn_run.clicked.connect(lambda: self.run(2)) 
        self.btn_explore_folder_2.clicked.connect(lambda: self.select_results(2))

        #1st tab (QGIS Import)
        self.cmb_layer_malla.setFilters(QgsMapLayerProxyModel.PolygonLayer)
        self.cmb_layer_nodes.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.cmb_layer_arcs.setFilters(QgsMapLayerProxyModel.LineLayer)

        self.btn_explore_folder.clicked.connect(lambda: self.select_results(1))
        self.cmb_layer_malla.layerChanged.connect(self.on_malla_layer_changed)
        self.btn_run_2.clicked.connect(lambda: self.run(1))

        # Initialize the field combos with the current layer of cmb_layer_malla
        initial_layer = self.cmb_layer_malla.currentLayer()
        if initial_layer:
            self.on_malla_layer_changed(initial_layer)

    def on_malla_layer_changed(self, layer):
        # Updates the layer fields
        self.cmb_field_catchment.setLayer(layer)
        self.cmb_field_groundwater.setLayer(layer)
        self.cmb_field_ds_prefix.setLayer(layer)

    def select_linkage(self):
        # Opens the file dialog limiting the view to .shp files
        filename, _ = QFileDialog.getOpenFileName(self, "Select Linkage File", "", "Shapefiles (*.shp)")
        if filename:
            layer = QgsVectorLayer(filename, "temp_linkage", "ogr")
            if layer.isValid() and layer.geometryType() != QgsWkbTypes.PolygonGeometry:
                QMessageBox.warning(self, "Geometry Error", "The Linkage file must be of Polygon type.")
                return
            self.lineEdit_linkage.setText(filename)

    def select_arc(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Arc File", "", "Shapefiles (*.shp)")
        if filename:
            layer = QgsVectorLayer(filename, "temp_arc", "ogr")
            if layer.isValid() and layer.geometryType() != QgsWkbTypes.LineGeometry:
                QMessageBox.warning(self, "Geometry Error", "The Arc file must be of Line type.")
                return
            self.lineEdit_arc.setText(filename)

    def select_node(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Node File", "", "Shapefiles (*.shp)")
        if filename:
            layer = QgsVectorLayer(filename, "temp_node", "ogr")
            if layer.isValid() and layer.geometryType() != QgsWkbTypes.PointGeometry:
                QMessageBox.warning(self, "Geometry Error", "The Node file must be of Point type.")
                return
            self.lineEdit_node.setText(filename)

    def select_results(self, tab):
        folder = QFileDialog.getExistingDirectory(self, "Select Results Folder", "")
        if folder:
            if tab == 1:
                self.lineEdit_folder.setText(folder)
            elif tab == 2:
                self.lineEdit_folder_2.setText(folder)


    def run(self, tab):  
        if tab == 1:
            linkage_path = self.cmb_layer_malla.currentLayer()
            arc_path = self.cmb_layer_arcs.currentLayer()
            node_path = self.cmb_layer_nodes.currentLayer()
            results_folder = self.lineEdit_folder.text()

            catchment_name = self.cmb_field_catchment.currentField()
            groundwater_name = self.cmb_field_groundwater.currentField()
            ds_prefix = self.cmb_field_ds_prefix.currentField()

        elif tab == 2:
            linkage_path = self.lineEdit_linkage.text()
            arc_path = self.lineEdit_arc.text()
            node_path = self.lineEdit_node.text()
            results_folder = self.lineEdit_folder_2.text()

            catchment_name = self.lineEdit_catchment.text().strip()
            groundwater_name = self.lineEdit_groundwater.text().strip()
            ds_prefix = self.lineEdit_ds_prefix.text().strip()
        
        if not all([linkage_path, arc_path, node_path, results_folder, catchment_name, groundwater_name, ds_prefix]):
            QMessageBox.warning(self, "Error", "Please select all files, the results folder, and the field names.")
            return

        if tab == 1:
            linkage_path = linkage_path.source().split('|')[0]
            arc_path = arc_path.source().split('|')[0]
            node_path = node_path.source().split('|')[0]

        try:
            # main task
            appkernel = AppKernel(
                linkage=linkage_path,
                arc=arc_path,
                node=node_path,
                results_folder=results_folder,
                catchment_name=catchment_name,
                groundwater_name=groundwater_name,
                ds_prefix=ds_prefix,
            )
            
            # Message Bar with infinite progress
            progress_msg = iface.messageBar().createMessage("GeoChecker", "Running plugin, please wait...")
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 0)
            progress_msg.layout().addWidget(progress_bar)
            iface.messageBar().pushWidget(progress_msg, Qgis.MessageLevel.Info)
            
            # Set wait cursor
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            QApplication.processEvents()
            
            try:
                appkernel.run()
            finally:
                # reset cursor and clean message bar
                QApplication.restoreOverrideCursor()
                iface.messageBar().clearWidgets()

            QMessageBox.information(self, "Success", "The checks have been executed correctly.")
            if sys.platform == 'win32':
                os.startfile(results_folder)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', results_folder])
            else:
                subprocess.Popen(['xdg-open', results_folder])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while executing the checks: {str(e)}")

# main class of the plugin
class GeoCheckerPlugin:
    """
    GeoCheckerPlugin class is the main entry point for the QGIS plugin.
    It handles the initialization, integration with the QGIS interface, and execution of the plugin's dialog.

    Attributes:
    ----------
    iface : QgisInterface
        Reference to the QGIS interface instance.
    
    action : QAction
        The action added to the QGIS menu to trigger the plugin.
        
    dialog : GeoCheckerDialog
        The main dialog window of the plugin.

    Methods:
    --------
    initGui():
        Initializes the plugin's graphical user interface, creating the menu action.
        
    unload():
        Removes the plugin menu item and cleans up resources when the plugin is disabled.
        
    run():
        Instantiates (if necessary) and displays the main plugin dialog.
    """
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        self.action = QAction("Run GeoChecker", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&GeoChecker", self.action)

    def unload(self):
        self.iface.removePluginMenu("&GeoChecker", self.action)
        if self.action:
            self.action.deleteLater()

    def run(self):
        if not self.dialog:
            self.dialog = GeoCheckerDialog(self.iface.mainWindow())
        self.dialog.show()
