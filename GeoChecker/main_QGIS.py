from pathlib import Path
from .utils.UtilMisc_QGIS import UtilMisc
from .check.GeoChecker import GeoChecker
from .check.SuperpositionCheck import SuperpositionCheck

def run(
    linkage: Path,
    arc: Path,
    node: Path,
    results_folder: Path,
    catchment_name: str,
    groundwater_name: str,
    ds_prefix: str,
):
    #QGIS lee los archivos directo desde el disco, borrado el entorno temporal 
    cells, arcs, nodes = UtilMisc.structure_creation(
        linkage_map=str(linkage),
        arc_map=str(arc),
        node_map=str(node),
        catch_name=catchment_name,
        gw_name=groundwater_name,
        ds_prefix=ds_prefix,
    )

    #sin cambios
    geochecker = GeoChecker(
        [
            SuperpositionCheck("groundwater", "demand_site"),
            SuperpositionCheck("groundwater", "catchment"),
        ],
        folder_path=results_folder,
    )

    geochecker.setup(cells, arcs, nodes)
    geochecker.run()