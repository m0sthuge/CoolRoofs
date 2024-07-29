# CoolRoofs
Code associated with Tokyo University of Science (TUS) X CU Denver Cool Roofs Research Project. 

These notebooks convert WorldView-3 (WV3) 16-band images and Red Edge 5-band drone imagery into Albedo Value rasters using a formula derived by the team at TUS. See their paper describing their WV3 albedo formula [here](https://www.jstage.jst.go.jp/article/jscejhe/78/2/78_I_733/_article/-char/ja/). Additionally, there is a function to Downscale rasters from a high-resolution raster to a low-resolution raster. This allows for comparing Albedo values obtained from the drone images versus those obtained from the satellite images. 

This is part of ongoing research into developing a better methodology for Deriving albedo from lower spectral resolution (and often cheaper) images like those taken by drones.

For information about ongoing research, contact Ben Crawford, PhD, at the University of Colorado Denver's Department of Geography and Environmental Science. benjamin.crawford@ucdenver.edu.

Pat Hall developed all the code, with process assistance from Rod Schubert, using the ArcPy library provided by ESRI.
