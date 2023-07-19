# geoTiffBatchExport v1.0, 7.14.23
# Code developed by Pat Hall and CU Denver GAMLab, 2023.

import arcpy
import os

def batchExTiff(select):

    if select == "y":
        out_name = input("please name new destination file: ")  
        print()
        out_pd = r"{}".format(input("enter path to destination file parent directory: ").strip('"\''))
        out_path = out_pd + "\\" + out_name
        os.mkdir(out_path)
        print()

    if select == "n": 
        out_path = r"{}".format(input("Enter path to destination file: ").strip('"\''))
        print()

    in_gdb = r"{}".format(input("Enter path to geodatabase with rasters for export: ").strip('"\''))
    print()
   
    # Set the environment workspace to the input geodatabase
    arcpy.env.workspace = in_gdb
    arcpy.env.compression = "LZW"
    arcpy.env.parallelProcessingFactor = 0
    
    #set .lyrx file to use as symbology template. 
    #symbology_template = r"{}".format(input("input filepath to .lyrx file to use as symbology template: ").strip('"\''))
    
    # Get a list of all raster datasets in the geodatabase
    rasters = arcpy.ListRasters()
    tot_num = len(rasters)
    
    print()
    print("exporting " + str(tot_num) + " geoTiffs.")
    print()
    
    count = 0
    
    # Loop through each raster dataset and export as GeoTIFF
    for raster in rasters:
        count += 1
        
        print("exporting raster " + str(count) + "/" + str(tot_num) + "...")
        # Generate the output file path
        out_raster = os.path.join(out_path, raster + ".tif")

        #print("formatting symbology...")
        
        #set symbology for raster from template
        # doesn't impact the export currently... which is annoying. I think I need to manually set
        # the renderer. Look at GraduatedColorsRenderer if you want to take another crack at this.
        # arcpy.management.ApplySymbologyFromLayer(raster, symbology_template)
        
        print("saving...")
        
        # Export the raster as GeoTIFF
        #arcpy.management.CopyRaster(out_layer, output_raster, "", "", "", "NONE", "NONE", "", "NONE", "NONE","COG")
        #arcpy.management.CopyRaster(raster, output_raster, "", "", "", "NONE", "NONE", "", "NONE", "NONE")
        
        arcpy.management.CopyRaster(raster, out_raster, "", "", "", "NONE", "NONE", "", "NONE", "NONE","COG")
        
    
        print("saved.")
        
        
        # Print the exported file path
        print(f"Exported: {out_raster}")
        print()

    print("Raster export completed.")

                              
def geoTiffBatchExport():                                           
    print("geoTiffBatchExport v1.0, 7.14.23")
    print("Code developed by Pat Hall and CU Denver GAMLab, 2023.")
    print("...")
    print("...")
    print()
                              
    while True:
        print("Do you want to export rasters as geoTiffs? (y/n)")    
        print()
        select = input()
        print()
        
        if select == "y":                     
            print("Do you want to create a new output folder for geoTiffs? (y/n)")
            print()

              
            select = input()
            print()
                              
            if select == "y" or select == "n":
                batchExTiff(select)
                x = False
                              
                              
            else:
                print("input invalid. Please select (y/n)")
                continue
        
        elif select == "n":
            print("end program.")
            print()
            break
        
        else:
            print("input invalid. Please select (y/n)")
            continue
    
