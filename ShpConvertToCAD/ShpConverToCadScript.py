 # Name: ExportToCAD.py
 # Description: Create an AutoCAD DWG
import os
import shutil
import urllib,time 
import zipfile
import arcpy
from arcpy import env

work_path = "C:/TEMP/AGS/EXPORT"

if os.path.exists(work_path):
    print "output_path exsits"
else :
    os.makedirs(work_path)

env.workspace = work_path
env.overwriteOutput = True
 
input_shape_file=arcpy.GetParameterAsText(0)
output_type = "DWG_R2010"
output_file = work_path + "/export.dwg"

try:
    shape_zip=work_path+"/"+time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))+".zip"
    shape_folder = work_path+"/"+time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
    print 'download shapfile zip'
    urllib.urlretrieve(input_shape_file,shape_zip)

    if os.path.isfile(shape_zip):
       f=zipfile.ZipFile(shape_zip,'r')
       for file in f.namelist():
           f.extract(file,shape_folder)
       f.close()
       os.remove(shape_zip)
    else:
        print "shape zip is not exsits"
    file_list = os.listdir(shape_folder)
    for file_name in file_list:
      if os.path.splitext(file_name)[1] == '.shp':
       arcpy.ExportCAD_conversion(shape_folder+"/"+file_name, output_type, output_file, "IGNORE_FILENAMES_IN_TABLES", "OVERWRITE_EXISTING_FILES", "")
       break
except Exception,e:
     raise e
     print arcpy.GetMessages()
arcpy.SetParameter(1,output_file)
shutil.rmtree(shape_folder)
print "export cad excute complete"

