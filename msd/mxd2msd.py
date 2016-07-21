import arcpy
import os,json
input_mxd_file = arcpy.GetParameterAsText(0)
output_msd_file=arcpy.GetParameterAsText(1)
mxd = arcpy.mapping.MapDocument(input_mxd_file)
df = arcpy.mapping.ListDataFrames(mxd)[0]
arcpy.mapping.ConvertToMSD(mxd, output_msd_file, df, "NORMAL", "NORMAL")