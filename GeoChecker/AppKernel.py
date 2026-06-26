from pathlib import Path
from .utils.UtilMisc_QGIS import UtilMisc
from .check.GeoChecker import GeoChecker
from .check.SuperpositionCheck import SuperpositionCheck


class AppKernel:
    def __init__(self, linkage: Path, arc: Path, node: Path, results_folder: Path, catchment_name: str, groundwater_name: str, ds_prefix: str):
        self.linkage = linkage
        self.arc = arc
        self.node = node
        self.results_folder = results_folder
        self.catchment_name = catchment_name
        self.groundwater_name = groundwater_name
        self.ds_prefix = ds_prefix
        
        self.cells = None
        self.arcs = None
        self.nodes = None
        
        self.checks = [
            SuperpositionCheck("groundwater", "demand_site"),
            SuperpositionCheck("groundwater", "catchment"),
        ]

    # group arcs by type and return a dictionary 
    def _group_arcs_by_type(self):
        arcs_type = {}
        for obj_id, arc_data in self.arcs.items():
            t = arc_data.get("type_id")
            if t not in arcs_type:
                arcs_type[t] = {}
            arcs_type[t][obj_id] = arc_data
        return arcs_type

    def load_data(self):
        # QGIS reads the files directly from the disk, deleting the temporary environment 
        self.cells, self.arcs, self.nodes = UtilMisc.structure_creation(
            linkage_map=str(self.linkage),
            arc_map=str(self.arc),
            node_map=str(self.node),
            catch_name=self.catchment_name,
            gw_name=self.groundwater_name,
            ds_prefix=self.ds_prefix,
        )

    def run_general_checks(self):
        geochecker = GeoChecker(self.checks, folder_path=self.results_folder)
        geochecker.setup(self.cells, self.arcs, self.nodes)
        geochecker.run()

    def run_specific_reports(self, target_arc_types=None):
        if target_arc_types is None:
            target_arc_types = [7, 8, 22]
            
        arcs_by_type = self._group_arcs_by_type()
        
        # check by arc type
        for arc_type in target_arc_types:
            if arc_type in arcs_by_type:
                # create subfolder for specific report
                type_folder = Path(self.results_folder) / f"type_{arc_type}"
                type_folder.mkdir(parents=True, exist_ok=True)
                
                type_geochecker = GeoChecker(self.checks, folder_path=type_folder)
                
                # we pass only the arcs filtered by this type
                type_geochecker.setup(self.cells, arcs_by_type[arc_type], self.nodes)
                type_geochecker.run()

    def run(self):
        self.load_data()
        self.run_general_checks()
        self.run_specific_reports()