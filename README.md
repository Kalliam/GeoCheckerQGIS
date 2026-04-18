# GeoChecker_QGIS
GeoChecker is a tool that checks for mistakes in linkage files for WEAP-MODFLOW integrated models.
This tool is a QGIS plugin that provides a GUI for the original project built in GRASS by [Antonio Torga](https://github.com/AntonioTorga/GeoChecker)


## Manual Installation 

Since the plugin is not yet in the official QGIS repository, it must be installed manually following these steps:


### 1. Locate the plugins folder

The path depends on your operating system:

- **Windows**: `%AppData%\QGIS\QGIS4\profiles\default\python\plugins`  
- **Linux**: `~/.local/share/QGIS/QGIS4/profiles/default/python/plugins`  
- **macOS**: `~/Library/Application Support/QGIS/QGIS4/profiles/default/python/plugins`  

> **Note:** If the `plugins` folder does not exist, create it manually.



### 2. Copy the repository

- Download this repository as a **ZIP** file and extract it or clone it using **Git**.  
```
git clone <https://github.com/Kalliam/GeoCheckerQGIS.git>
```
- Move the cloned folder named **GeoChecker_QGIS** into the plugins folder located in the previous step.



### 3. Activate in QGIS

- Open (or restart) QGIS.  
- Go to the menu **Plugins > Manage and Install Plugins...**  
- Search for **GeoChecker** in the *Installed* tab.  
- Check the box to activate the plugin.

---

## Usage
Go to the menu **Plugins > Geochecker > Run GeoChecker**  

### Input Files
Select the corresponding **Shapefile (.shp)** files for:
- Linkage File.  
- WEAP Arcs.  
- WEAP Nodes.  

Fill the column names of your database (**Catchment**, **Groundwater**) and the demand site prefix.
> **Note:** To check the name values, open the attribute table of the shapefiles.

### Execute
Press the button to process.  
The results will be saved in the selected destination folder and will include:
- Connection matrices in **PDF**.  
- Error reports in **TXT** and **CSV**. 

---