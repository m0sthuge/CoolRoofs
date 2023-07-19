import arcpy,os

def newGDB():
    # gets parent directory of the current ArcGIS Project file. This is where the gdb will be saved.
    project = arcpy.mp.ArcGISProject("CURRENT")
    proj_file_path = project.filePath
    pd = os.path.dirname(proj_file_path)
    
    name = input("please input a name for the output geodatabase: ")
    print()
    print("creating new geodatabase " + str(name) + "...")
    
    arcpy.management.CreateFileGDB(pd, name, "CURRENT")
    
    gdb_path = pd + "\\" + name + ".gdb"
    
    return gdb_path

def albedoBandMath(select):
    
    # albedo formula definitions that are called on in BandArithmetic. 
    # B# is the predefined variable for bands in bandArithmetic.
    droneAlbedo = "((B1 / 65535) * 0.18694) - \
        ((B2 / 65535) * 0.037936) + \
        ((B3 / 65535) * 0.34519) - \
        ((B4 / 65535) * 0.072438) + \
        ((B5 / 65535) * 0.46364) + 0.038745"
    
    wv3Albedo = "(B1 * 0.174824302) - (B2 * 0.028888428) + (B3 * 0.163480692) + \
        (B4 * 0.017530318) + (B5 * 0.140591341) + (B6 * 0.065691351) + \
        (B7 * 0.087504929) + (B8 * 0.136872282) + (B9 * 0.141542963) + \
        (B10 * 0.003559626) + (B11 * 0.06813960) - (B12 * 0.020452507) + \
        (B13 * 0.197106374) - (B14 * 0.259572854) + (B15 * 0.049763538) + (B16 * 0.049838153)"
    
    
    if select == "1":
        albedo = droneAlbedo
        
    elif select == "2":
        albedo = wv3Albedo
        
    else:
        print("error: formula value is " + str(select) +". this is outside the expected parameter.")
        return
    
    
    while True:
        print("would you like to create a new geodatabase for output albedo rasters? (y/n)")
        print()
        choice = input("selection:")
        print()
        
        if choice == "y" or choice == "Y":
            # creates a new geodatabase for output rasters
            outGDB = newGDB()
            print("Created new geodatabase at " + str(outGDB))
            print()
            break
            
        elif choice == "n" or choice == "N":
            # asks for gdb filepath
            outGDB = r"{}".format(input("enter path to geodatabase to save output albedo rasters: ").strip('"\''))
            print()
            break
    
        else:
            print("not a valid entry.")
            print()
            continue
            
    # sets target to gdb with composite images
    arcpy.env.workspace = r"{}".format(input("enter path to geodatabase with target composite rasters: ").strip('"\''))
    
    # gets all rasters in geodatabase entered above as a list.
    rasters = arcpy.ListRasters("*","All")
    totNum = len(rasters)
    
    print("calculating albedo for " + str(totNum) + " rasters")
    print()
    
    # sets count for process tracking
    count = 0
    
    # loops over all composite images in data set
    for raster in rasters:
        count += 1
        
        print("calulating albedo for " + str(count) + "/" + str(totNum) + "...")
        
        try:
            outRas = arcpy.sa.BandArithmetic(raster, albedo, 0)
            arcpy.Raster(outRas)
            
            print("albedo calculated.")
            print("saving...")

            outRas.save(str(outGDB) + "\\" + raster + "_albedo")
        
            print("saved " + str(count) + "/" + str(totNum))
            print()
                  
        except Exception as e:
            print("error occurred for raster " + str(raster))
            print("Error message: " + str(e))
            print()
            
    
    print("process complete.")
    print()
    
        
    
def albedoCalc():
    print("image albedo calculator v1.30, 7.18.23")
    print("Code developed by Pat Hall & Rod Schubert and CU Denver GAMLab, 2023.")
    print("All albedo formulas created by Tokyo University of Science, 2023.")
    print("...")
    print("...")
    print()
    
    while True:
        print("would you like to:")
        print("(1) calculate albedo for 5-band drone image")
        print("(2) calculate albedo for 16-band wv3 image")
        print("(3) upscale high resolution raster for comparison with low resolution raster")
        print("(e) exit program")
        print()

              
        select = input("selection: " )
        print()
    
        if select == "1":
            print("opening drone Image Albedo Calculator...")
            print()
            albedoBandMath(select)   
        
        elif select == "2":
            print("opening World View 3 Image Albedo Calculator...")
            print()
            albedoBandMath(select)
            
        elif select == "3":
            print("Opening Raster Upscale Tool...")
            print()
            reScaleRasterbyMedian()
                  
        elif select == "e":
            print("end program.")
            break
              
        else:
            print("Not a valid input.")
            continue
                  
    
    

import arcpy, os
from arcpy.ia import *
from sys import argv

def reScaleRasterbyMedian():  # RasterComparisonResample
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True
    
    debug = True
    if debug == True:
        wv3Gdb = r"C:\Users\pathall\OneDrive - The University of Colorado Denver\GAM\Ben Crawford - Cool Roofs\Arc Project\CoolRoofs_Albedo_WV3Rasters.gdb"
        droneGdb = r"C:\Users\pathall\OneDrive - The University of Colorado Denver\GAM\Ben Crawford - Cool Roofs\Arc Project\CoolRoofs_Albedo_DroneRasters.gdb"
        outGDB = r"C:\Users\pathall\OneDrive - The University of Colorado Denver\GAM\Ben Crawford - Cool Roofs\Arc Project\CoolRoofs_Albedo_DroneRasters_Upscaled.gdb"
        out_ZonalStatGdb = r"C:\Users\pathall\OneDrive - The University of Colorado Denver\GAM\Ben Crawford - Cool Roofs\Arc Project\CoolRoof_Albedo_Drone_ZonalStats.gdb"
        
        print("Debug mode active")
        print("wv3Gdb = " + str(wv3Gdb))
        print("droneGdb = " + str(droneGdb))
        print("outGDB = " + str(outGDB))
        print("out_ZonalStatGdb " + str(out_ZonalStatGdb))
        print()
        
        arcpy.env.workspace = droneGdb
        droneRasters = arcpy.ListRasters("*","All")
        droneRasters = sorted(droneRasters)
        totNum_Drone = len(droneRasters)
        
    
        print()
        print("Found " + str(totNum_Drone) + " rasters to process.")
        print()
    
        arcpy.env.workspace = wv3Gdb
        wv3Rasters = arcpy.ListRasters("*","All")
        wv3Rasters = sorted(wv3Rasters)
        totNum_wv3 = len(wv3Rasters)
    
        print()
        print("Found " + str(totNum_wv3) + " rasters to scale to.")
        print()

   
    # gets rasters to be processed from two databases.
    else:
        print()
        print("The Raster Upscale Tool will take the median of all cells of the higher resolution raster and display it at the level of a lower resolution raster. This allows for direct comparison of the same object from two different resolution rasters.")
        print("Raster Upscale Tool requires 2 geodatabases as input. The first is the geodatatabase with higher resolution images,") 
        print("the second is the geodatabase with lower resolution images.")
        print("Both geodatabases need to have rasters ordered the same way. (i.e. gdb1: droneRoof1,droneRoof2, etc. gdb2: wv3Roof1, wv3Roof2, etc.)")
        print("Both geodatabases should have the same number of rasters.")
        print()
        droneGdb = r"{}".format(input("Enter the path to the geodatabase with higher resolution rasters: ").strip('"\''))
        arcpy.env.workspace = droneGdb
        droneRasters = arcpy.ListRasters("*","All")
        droneRasters = sorted(droneRasters)
        totNum_Drone = len(droneRasters)
    
        print()
        print("Found " + str(totNum_Drone) + " rasters to process.")
        print()
    
        wv3Gdb = r"{}".format(input("Enter the path to the geodatabase lower resolution rasters you want to scale to: ").strip('"\''))
        arcpy.env.workspace = wv3Gdb
        wv3Rasters = arcpy.ListRasters("*","All")
        wv3Rasters = sorted(wv3Rasters)
        totNum_wv3 = len(wv3Rasters)
    
        print()
        print("Found " + str(totNum_wv3) + " rasters to scale to.")
        print()

        print("Would you like to send output rasters to an existing database (e) or make a new geodatabase (n)?")
        print()
        select = input()
        print()
   
        while True:
            if select == "e":
                outGDB = r"{}".format(input("enter path to geodatabase to save output albedo rasters: ").strip('"\''))
                print()
                break

            elif select == "n":
                outGDB = newGDB()
                print()
                break

            else:
                print("not a valid entry. please select:")
                print("(e) Use an existing geodatabase")
                print("(n) Create a new geodatabase")
                print()
                return

        print("Would you like to send output Zonal Statistics Tables to an existing database (e) or make a new geodatabase (n)?")
        print()
        select = input()
        print()

        while True:
            if select == "e":
                out_ZonalStatGdb = input("Enter the path to output geodatabase for zonal statistics tables: ").strip('"\'')
                print()
                break

            elif select == "n":
                out_ZonalStatGdb = newGDB()
                print()
                break

            else:
                print("not a valid entry.")
                print("(e) Use an existing geodatabase")
                print("(n) Create a new geodatabase")
                print()
                return
    
    # modelRaster sets the environement paramenters for cell size and snapRaaster to the currently processing raster.
    #modelRaster = arcpy.Raster("Roof1_WV3_CompositeBand_albedo")
    
    print("setting Constants....")
    Simplify_polygons = False
    print("Simplify_polygons = "+ str(Simplify_polygons))
    Zone_Field = "GRIDCODE"
    print("Zone_Field = " + str(Zone_Field))
    Ignore_NoData_in_Calculations = True
    print("Ignore_NoData_in_Calculations = " + str(Ignore_NoData_in_Calculations))
    Value_field = "MEDIAN"
    print("out_RasterPixelValue = " + str(Value_field))
    print()
    print()
    
    count = 0
    wv3Index = -1
    
    for droneRaster in droneRasters:
        
        count += 1

        print("Scaling raster " + str(count) + "/" + str(totNum_Drone) + "...")
        print()
        print("HighRes Raster: " + str(droneRaster))
        print()
        print("Finding LowRes Raster...")
        wv3Index += 1
        currentWv3Ras = wv3Rasters[wv3Index]
        print("Found LowRes Raster: " + str(currentWv3Ras))
        print()
       
        
        
        # Process 1: Raster Calculator (Raster Calculator) (ia). used to remove decimals (can't conver raster to polygon unless pixel values are integers)
        print("step 1/6: removing decimals.")
        print("creating temp layer...")
        tempIntRas = "c:\\Users\\hpatrick\\onedrive - the university of colorado denver\\GAM\\ben crawford - cool roofs\\arc project\\ph_coolroofs_v2.gdb\\tempIntRas"
        Raster_Calculator = tempIntRas
        print("temp layer " + str(tempIntRas) + " created.")
              
              
        print("removing decimal places...")
        with arcpy.EnvManager(cellSize=currentWv3Ras, compression="LZ77", \
        outputCoordinateSystem='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]', \
        snapRaster=currentWv3Ras):
            tempIntRas = RasterCalculator([currentWv3Ras],["x"],"x * 1000000")
            print("decimal places removed.")
            #tempIntRas.save(str(Raster_Calculator))
            #print("temp layer saved.")  
            print("...")


        # Process 2: Int (Int) (ia)| converting the raster into an integer. 
        print("step 2/6: converting pixel value to Integer.")
        print("creating temp layer...")
        tempIntRas2 = "C:\\Users\\hpatrick\\OneDrive - The University of Colorado Denver\\GAM\\Ben Crawford - Cool Roofs\\Arc Project\\ph_coolroofs_v2.gdb\\tempIntRas2"
        Int = tempIntRas2
        print("temp layer " + str(tempIntRas2) + " created.")
              
              
        print("converting pixel values...")
        with arcpy.EnvManager(cellSize=currentWv3Ras, snapRaster=currentWv3Ras):
            tempIntRas2 = arcpy.sa.Int(tempIntRas)
            print("pixel values converted.")
            #tempIntRas2.save(Int)
            #print("temp layer saved.")
            print("...")

        # Process 3: Raster to Polygon (Raster to Polygon) (conversion) | Converting to a polygon so we can use as a grid in Zonal statistics 
        print("step 3/6: Raster to Polygon Conversion.")
        print("creating temp layer...")
        
        #tempRas2Poly currently relies on there being an existing feature class at the specified locaion
        #could use an if statement in future?
        
        tempRas2Poly = r"C:\Users\pathall\OneDrive - The University of Colorado Denver\GAM\Ben Crawford - Cool Roofs\Arc Project\PH_CoolRoofs_v2.gdb\tempR2P"
        print("temp layer " + str(tempRas2Poly) + " created.")
          
        print("converting raster to polygon...")      
        with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
            arcpy.conversion.RasterToPolygon(in_raster=tempIntRas2, out_polygon_features=tempRas2Poly, simplify=Simplify_polygons, raster_field="VALUE", create_multipart_features="MULTIPLE_OUTER_PART", max_vertices_per_feature=None)
        print("raster to polygon conversion completed.")
        print("...")
              
        # Process 4: Zonal Statistics as Table (Zonal Statistics as Table) (ia) finding Stats of all pixels from high res images that fall in a single lower res pixel.
        print("step 4/6: Creating Zonal Statistics Table.")  
        tableName = str(droneRaster) + "stats"
        print("calculating Zonal statistics for " + str(tableName) + "...")
        Roofstats = str(out_ZonalStatGdb) + "\\" + tableName
        with arcpy.EnvManager(workspace = droneGdb):
            arcpy.ia.ZonalStatisticsAsTable(in_zone_data=tempRas2Poly, zone_field=Zone_Field, in_value_raster=droneRaster, out_table=Roofstats, ignore_nodata=Ignore_NoData_in_Calculations, statistics_type="ALL", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
        print("table saved to " + str(Roofstats))
        print("...")


        # Process 5: Join Field (Join Field) (management) joining stats of high res image to the polygon genrated from low res image
        print("step 5/6: Join " + str(tableName) +  "to LowRes polygon.")
        print("joining on " + str(Zone_Field) + "...")
        tempRas2Poly_2_ = arcpy.management.JoinField(in_data=tempRas2Poly, in_field=Zone_Field, join_table=Roofstats, join_field="Gridcode", fields=[], fm_option="NOT_USE_FM")
        print(str(tableName) + "joined to polygon.")
        print("...")  
              
        # Process 6: Polygon to Raster (Polygon to Raster) (conversion) 
        print("step 6/6: Convert polygon to raster.")
        print("converting polygon using " + str(Value_field) + " as pixel value...")
        out_RasFinal = str(outGDB) + "\\" + droneRaster + "_UpScale"
        arcpy.conversion.PolygonToRaster(in_features=tempRas2Poly_2_, value_field=Value_field, out_rasterdataset=out_RasFinal, cell_assignment="CELL_CENTER", priority_field="NONE", cellsize="0.088", build_rat="BUILD")

        print("polygon to raster conversion complete.")
        print("output raster: " + str(droneRaster) + "_UpScale")
        print("raster location: " + str(out_RasFinal))
        print()
        print()
        


