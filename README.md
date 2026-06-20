# GeoChecker_QGIS
GeoChecker is a tool that checks for mistakes in linkage files for WEAP-MODFLOW integrated models.
This tool is a QGIS plugin that provides a GUI for the original project built in GRASS by [Antonio Torga](https://github.com/AntonioTorga/GeoChecker)


## Manual Installation 

Since the plugin is not yet in the official QGIS repository, it must be installed manually following these steps:


### 1. Locate the plugins folder

The path depends on your operating system:

| Operating System | Plugins Path |
|---|---|
| **Windows** | `%APPDATA%\QGIS\QGIS4\profiles\default\python\plugins\` |
| **Linux** | `~/.local/share/QGIS/QGIS4/profiles/default/python/plugins/` |
| **macOS** | `~/Library/Application Support/QGIS/QGIS4/profiles/default/python/plugins/` |
> [!NOTE] 
> If the "plugins" folder does not exist, create it manually.



### 2. Copy the repository

Download this repository as a **ZIP** file and extract it or clone it using **Git**.  
```
git clone <https://github.com/Kalliam/GeoCheckerQGIS.git>
```
Move the cloned folder named **GeoChecker_QGIS** into the plugins folder located in the previous step.

### 3. Install required packages
Open OSGeo4W Shell and install the required packages with:
   ```bash
   python -m pip install pandas seaborn matplotlib numpy
   ```

### 4. Activate in QGIS

Open (or restart) QGIS.  
Go to the menu **Plugins > Manage and Install Plugins...**  
Search for **GeoChecker** in the *Installed* tab.  
Check the box to activate the plugin.

---

## Usage
Go to the menu **Plugins > Geochecker > Run GeoChecker**.

Geochecker has two ways to load the input files, one per tab in the opened window:
1. **QGIS Load**: Loads the input files from the current layers in the QGIS project.
2. **Manual Load**: Loads the input files from the local file system.

### Input Files
Select the corresponding **Shapefile (.shp)** files for:
- Linkage File.  
- WEAP Arcs.  
- WEAP Nodes.  

Fill the column names of your database (**Catchment**, **Groundwater**) and the demand site prefix.
> **Note:** you can check the column names by opening the attribute table of the shapefiles.

### Execute
Press the **run** button to process.  
The results will be saved in the selected destination folder and will include:
- Connection matrices in **PDF**.  
- Error reports in **TXT** and **CSV**. 

---