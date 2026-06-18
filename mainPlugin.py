import os
import sys
import subprocess
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

# initialize Qt resources from file resources.py
from PyQt6 import uic
from .GeoChecker.AppKernel import AppKernel
from qgis.core import QgsMapLayerProxyModel, QgsProject, QgsVectorLayer, QgsMapLayerType, QgsWkbTypes


FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'geo_checker_dialog.ui'))

# clase ventana
class GeoCheckerDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(GeoCheckerDialog, self).__init__(parent)
        self.setupUi(self) # Esto "dibuja" la ventana
        
        #los nombres (btn_explore_linkage) deben coincidir con QT desgner
        #2da tab
        self.btn_explore_linkage.clicked.connect(self.select_linkage)
        self.btn_explore_arc.clicked.connect(self.select_arc)
        self.btn_explore_node.clicked.connect(self.select_node)
        self.btn_run.clicked.connect(lambda: self.run(2)) 
        self.btn_explore_folder_2.clicked.connect(lambda: self.select_results(2))

        #1ra tab (QGIS Import)
        self.btn_explore_folder.clicked.connect(lambda: self.select_results(1))
        self.cmb_layer_malla.layerChanged.connect(self.on_malla_layer_changed)
        self.btn_run_2.clicked.connect(lambda: self.run(1))

        # Inicializar los field combos con la capa actual de cmb_layer_malla
        initial_layer = self.cmb_layer_malla.currentLayer()
        if initial_layer:
            self.on_malla_layer_changed(initial_layer)


    #logica de los botones
    def on_malla_layer_changed(self, layer):
        """Cuando cambia la capa en cmb_layer_malla, actualiza los field combos."""
        self.cmb_field_catchment.setLayer(layer)
        self.cmb_field_groundwater.setLayer(layer)
        self.cmb_field_ds_prefix.setLayer(layer)

    def select_linkage(self):
        # Abre el buscador limitando la vista a archivos .shp
        filename, _ = QFileDialog.getOpenFileName(self, "Select Linkage File", "", "Shapefiles (*.shp)")
        if filename:
            self.lineEdit_linkage.setText(filename) # Pega la ruta en la caja de texto

    def select_arc(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Arc File", "", "Shapefiles (*.shp)")
        if filename:
            self.lineEdit_arc.setText(filename)

    def select_node(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Node File", "", "Shapefiles (*.shp)")
        if filename:
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
            #funcion principal
            appkernel = AppKernel(
                linkage=linkage_path,
                arc=arc_path,
                node=node_path,
                results_folder=results_folder,
                catchment_name=catchment_name,
                groundwater_name=groundwater_name,
                ds_prefix=ds_prefix,
            )
            appkernel.run()
            QMessageBox.information(self, "Success", "The checks have been executed correctly.")
            if sys.platform == 'win32':
                os.startfile(results_folder)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', results_folder])
            else:
                    subprocess.Popen(['xdg-open', results_folder])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while executing the checks: {str(e)}")

# clase principal del Plugin (por defecto))
class GeoCheckerPlugin:
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
