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

    # Generar reportes especificos
    target_arc_types = [7, 8, 22]
    
    # Agrupar arcos por tipo 
    arcs_by_type = {}
    for obj_id, arc_data in arcs.items():
        t = arc_data.get("type_id")
        if t not in arcs_by_type:
            arcs_by_type[t] = {}
        arcs_by_type[t][obj_id] = arc_data

    for arc_type in target_arc_types:
        if arc_type in arcs_by_type:
            # Crear subcarpeta para el reporte especifico
            type_folder = Path(results_folder) / f"type_{arc_type}"
            type_folder.mkdir(parents=True, exist_ok=True)
            
            type_geochecker = GeoChecker(
                [
                    SuperpositionCheck("groundwater", "demand_site"),
                    SuperpositionCheck("groundwater", "catchment"),
                ],
                folder_path=type_folder,
            )
            # Pasamos solo los arcos filtrados por este tipo
            type_geochecker.setup(cells, arcs_by_type[arc_type], nodes)
            type_geochecker.run()