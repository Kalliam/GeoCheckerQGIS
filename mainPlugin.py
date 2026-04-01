import os
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

# initialize Qt resources from file resources.py
from PyQt6 import uic
from .GeoChecker.main_QGIS import run

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'geo_checker_dialog.ui'))

# clase ventana
class GeoCheckerDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(GeoCheckerDialog, self).__init__(parent)
        self.setupUi(self) # Esto "dibuja" la ventana
        
        # --- AQUÍ CONECTAMOS LOS BOTONES (Señales y Slots) ---
        # ATENCIÓN: Los nombres (btn_explore_linkage, etc.) deben coincidir 
        # EXACTAMENTE con el "objectName" que le pusiste a cada botón en Qt Designer.
        self.btn_explore_linkage.clicked.connect(self.select_linkage)
        self.btn_explore_arc.clicked.connect(self.select_arc)
        self.btn_explore_node.clicked.connect(self.select_node)
        self.btn_explore_folder.clicked.connect(self.select_results)
        self.btn_run.clicked.connect(self.run_checks) 

    # --- AQUÍ DEFINIMOS QUÉ HACE CADA BOTÓN ---
    def select_linkage(self):
        # Abre el buscador limitando la vista a archivos .shp
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo Linkage", "", "Shapefiles (*.shp)")
        if filename:
            self.lineEdit_linkage.setText(filename) # Pega la ruta en la caja de texto

    def select_arc(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo Arc", "", "Shapefiles (*.shp)")
        if filename:
            self.lineEdit_arc.setText(filename)

    def select_node(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo Node", "", "Shapefiles (*.shp)")
        if filename:
            self.lineEdit_node.setText(filename)

    def select_results(self):
        # Para los resultados usamos getExistingDirectory porque buscamos una CARPETA, no un archivo
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Resultados", "")
        if folder:
            self.lineEdit_folder.setText(folder)

    def run_checks(self):
        # Aquí es donde pondremos la lógica para ejecutar los chequeos
        # Por ahora solo mostramos un mensaje con las rutas seleccionadas
        linkage_path = self.lineEdit_linkage.text()
        arc_path = self.lineEdit_arc.text()
        node_path = self.lineEdit_node.text()
        results_folder = self.lineEdit_folder.text()

        # Validamos que se hayan seleccionado todos los archivos y la carpeta
        if not all([linkage_path, arc_path, node_path, results_folder]):
            QMessageBox.warning(self, "Error", "Por favor, seleccione todos los archivos y la carpeta de resultados.")
            return

        try:
            #ejecutamos la funcion principal
            run(
                linkage=linkage_path,
                arc=arc_path,
                node=node_path,
                results_folder=results_folder,
                catchment_name="Catchment",
                groundwater_name="GW",
                ds_prefix="T_Dda_AP",
            )
            QMessageBox.information(self, "Éxito", "Los chequeos se han ejecutado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al ejecutar los chequeos: {str(e)}")

# clase principal del Plugin (por defecto))
class GeoCheckerPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        self.action = QAction("Ejecutar GeoChecker", self.iface.mainWindow())
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

# class TestPlugin:

#   def __init__(self, iface):
#     # save reference to the QGIS interface
#     self.iface = iface
#     self.action = None
#     self.dialog = None

#   def initGui(self):
#     # create action that will start plugin configuration
#     self.action = QAction(QIcon("testplug:icon.png"),
#                           "Test plugin",
#                           self.iface.mainWindow())
#     self.action.setObjectName("testAction")
#     self.action.setWhatsThis("Configuration for test plugin")
#     self.action.setStatusTip("This is status tip")
#     self.action.triggered.connect(self.run)

#     # add toolbar button and menu item
#     self.iface.addToolBarIcon(self.action)
#     self.iface.addPluginToMenu("&Test plugins", self.action)

#     # connect to signal renderComplete which is emitted when canvas
#     # rendering is done
#     self.iface.mapCanvas().renderComplete.connect(self.renderTest)

#   def unload(self):
#     # remove the plugin menu item and icon
#     self.iface.removePluginMenu("&Test plugins", self.action)
#     self.iface.removeToolBarIcon(self.action)

#     # disconnect form signal of the canvas
#     self.iface.mapCanvas().renderComplete.disconnect(self.renderTest)

#   def run(self):
#     # create and show a configuration dialog or something similar
#     if not self.dialog:
#             self.dialog = GeoCheckerDialog(self.iface.mainWindow())
            
#             # (En el próximo paso conectaremos los botones aquí)
            
#     print("TestPlugin: run called!")
#     self.dialog.show()

#   def renderTest(self, painter):
#     # use painter for drawing to map canvas
#     print("TestPlugin: renderTest called!")