#Name: CAD2PolygonFeatureSets

import os,json
import urllib,time
import arcpy
from arcpy import env

gdb_file = "cadtemp.gdb"
work_path = "C:/TEMP/AGS"
work_gdb_path = work_path + "/" + gdb_file

if os.path.exists(work_path):
    print "work_path exsits"
else :
    os.makedirs(work_path)

if arcpy.Exists(work_gdb_path):
    print "gdb path exists"
else :
    arcpy.CreateFileGDB_management(work_path, gdb_file)

env.workspace = work_gdb_path
env.overwriteOutput = True   

input_cad_file = arcpy.GetParameterAsText(0)
output_gdb_path = work_gdb_path;
output_featureset_name = "OutputCadFeatureSet";

try:
    cad_data =work_path+"/"+time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))+".DWG"
    print "download dwg file"
    urllib.urlretrieve(input_cad_file,cad_data)
    result = arcpy.CADToGeodatabase_conversion(cad_data,output_gdb_path,output_featureset_name,1000)
except Exception, e:
    raise e

fcs = []
for fds in arcpy.ListDatasets('OutputCadFeatureSet','feature') + ['']:
    print fds
    for fc in arcpy.ListFeatureClasses('','Polygon',fds):
        fcs.append(fc)
        print fc        

arcpy.SetParameter(1,fcs);
os.remove(cad_data)

print "cad tool excute complete"
    

