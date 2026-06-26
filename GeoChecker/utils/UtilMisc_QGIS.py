import random
from qgis.core import QgsVectorLayer, NULL
from qgis.PyQt.QtCore import QCoreApplication

class UtilMisc:

    @staticmethod
    def generate_word(length: int = 5, prefix: str = "mapset_"):
        _signs = "abcdefghijklmnopqrstuvwxyz1234567890"

        word = ""
        for i in range(length):
            word += random.choice(_signs)

        return prefix + word

    @staticmethod
    def structure_creation(
        linkage_map: str,
        arc_map: str,
        node_map: str,
        catch_name: str,
        gw_name: str,
        ds_prefix: str,
    ):
        """_summary_

        Parameters
        ----------
        linkage_map : str
            Name assigned to the map created when Linkage file was imported to the mapset.
        arc_map : str
            Name assigned to the map created when the WEAP Arc file was imported to the mapset.
        node_map : str
            Name assigned to the map created when the WEAP Arc file was imported to the mapset.

        Returns
        -------

        dict
            Dict representing the cells of the linkage file. Has the following structure:
            {Cell ID :
                {
                    'catchment': catchment name,
                    'groundwater': groundwater name,
                    'demand_site': list of demand site names,
                    'cell_area': float of the area
                }
            }
        dict
            Dict representing the cells Arcs of the WEAP Model. Has the following structure:
            {Arc ID :
                {
                    'type_id': geometry type ID of the arc,
                    'src_id': source node ID (or None),
                    'dst_id': destination node ID (or None)
                }
            }
        dict
            Dict representing the Nodes of the WEAP Model. Has the following structure:
            {Node ID :
                {
                    'type_id': geometry type ID,
                    'name': node name,
                    'cat': node internal ID (used by 'pygrass library')
                }
            }
        """
        
        # ---------------------------------------------------------
        # Grid
        # ---------------------------------------------------------
        cells = dict()
        linkage_layer = QgsVectorLayer(linkage_map, "linkage", "ogr") 

        field_names = linkage_layer.fields().names()
        demand_attrs = [
            attr for attr in field_names if attr.startswith(ds_prefix)
        ]

        for i, feature in enumerate(linkage_layer.getFeatures()):
            if i % 1000 == 0:
                QCoreApplication.processEvents()

            cat = feature.id()
            catch_raw = feature[catch_name]
            gw_raw = feature[gw_name]
            area = feature.geometry().area()

            catch = str(catch_raw).strip() if catch_raw != NULL and catch_raw else None
            gw = str(gw_raw).strip() if gw_raw != NULL and gw_raw else None
            
            demand_sites = []
            for attr in demand_attrs:
                val = feature[attr]
                # demand sites cleanup
                if val != NULL and val:
                    demand_sites.append(str(val).strip())
            demand_sites = list(set(demand_sites)) # removing duplicates
       
            if None in demand_sites:
                demand_sites.remove(None)

            cells[cat] = {
                "catchment": [catch],
                "groundwater": [gw],
                "demand_site": demand_sites,
                "cell_area": area,
            }

        # ---------------------------------------------------------
        # Arcs
        # ---------------------------------------------------------
        arcs = dict()
        arc_layer = QgsVectorLayer(arc_map, "arcs", "ogr")

        for feature in arc_layer.getFeatures():
            obj_id = feature["ObjID"]
            type_id_raw = feature["TypeID"]
            type_id = int(type_id_raw) if type_id_raw != NULL else 0
            src_id = feature["SrcObjID"]
            dst_id = feature["DestObjID"]
            arcs[obj_id] = {
                "type_id": type_id,
                "src_id": src_id,
                "dst_id": dst_id,
            }
            
        # ---------------------------------------------------------
        # Nodes
        # ---------------------------------------------------------
        nodes = dict()
        node_layer = QgsVectorLayer(node_map, "nodes", "ogr")

        for feature in node_layer.getFeatures():
            obj_id = feature["ObjID"]
            type_id_raw = feature["TypeID"]
            type_id = int(type_id_raw) if type_id_raw != NULL else 0
            
            name_raw = feature["name2"]
            name = str(name_raw).strip() if name_raw != NULL else ""
   
            cat = feature.id()
            nodes[obj_id] = {
                "type_id": type_id,
                "name": name,
                "cat": cat,
            }

        return cells, arcs, nodes