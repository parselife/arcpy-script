# -*- coding:utf-8 -*-
import arcpy
from arcpy import env
import os
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

# 创建ArcSDE数据库连接文件
def CreateSdeConnection(out_folder_path,out_name,instance,username,password):
    try:
        arcpy.CreateDatabaseConnection_management(out_folder_path,
                                          out_name,
                                          "ORACLE",
                                          instance,
                                          "DATABASE_AUTH",
                                          username,
                                          password,
                                          "SAVE_USERNAME")
    except Exception, e:
         arcpy.AddError(e.message);

# 对要素类进行数据比较 未找到差异时将为“真”，在检测到差异时则为“假”
def CompareFeatureClass(base_features,test_features):
    try:

        # Set local variables
        sort_field = "OBJECTID"
        compare_type = "ALL"
        ignore_option = "IGNORE_M;IGNORE_Z;IGNORE_EXTENSION_PROPERTIES;IGNORE_SUBTYPES;"
        xy_tolerance = "0.001 METERS"
        m_tolerance = 0
        z_tolerance = 0
        attribute_tolerance = "Shape_Length 0.001"
        omit_field = "#"
 
        # Process: FeatureCompare
        compare_result = arcpy.FeatureCompare_management(base_features, test_features, sort_field, compare_type, ignore_option, xy_tolerance, m_tolerance, z_tolerance, attribute_tolerance, omit_field)

        return compare_result.getOutput(0)

    except Exception, e:
        arcpy.AddError(e.message);    

#拷贝单个要素类对象，不在数据集内的要素类  
def CopyFeatureClasses(src_db,tar_db,num,prefix):  
  
    try:  
        #设置工作空间  
        arcpy.env.workspace = src_db  
  
        wk2 = tar_db  
  
        #遍历 feature classes  
  
        for fc in arcpy.ListFeatureClasses():             
  
            if arcpy.Exists(fc)==False:
                continue

            desc = arcpy.Describe(fc) 

            if desc.name.startswith(prefix.upper())==False:
                 continue 
  
            arcpy.AddMessage("读取要素类: {0}".format(fc)) 

            new_data=desc.name[num:]

            tar_fc=wk2 + os.sep + new_data 
  
            if arcpy.Exists(tar_fc)==False:  

                arcpy.Copy_management(fc, tar_fc)  
  
                arcpy.AddMessage("成功备份要素类:{0}".format(new_data)) 
  
            else:
                #对于已经存在的要素 先进行要素比较
                if CompareFeatureClass(fc,tar_fc)==False:

                    arcpy.Copy_management(fc, tar_fc)

                    arcpy.AddMessage("成功备份要素类:{0}".format(new_data))

                else:
                    arcpy.AddMessage("要素类 {0} 已经在目标数据库中存在且没有更新,将被忽略!".format(new_data))
  
        #Clear memory  
  
        del fc  
  
    except Exception as e:  
        arcpy.AddError(e.message);  

#拷贝数据集对象  
def CopyDatasets(src_db,tar_db,num,prefix):  
  
    try:  
  
        #设置工作空间  
  
        arcpy.env.workspace = src_db  
  
        wk2 = tar_db  
  
        datasetList = arcpy.ListDatasets() 
  
        #遍历datasets  
  
        for dataset in datasetList:             
  
            if arcpy.Exists(dataset)==False:
                continue

            desc = arcpy.Describe(dataset)

            if desc.name.startswith(prefix.upper())==False:
                 continue   
  
            arcpy.AddMessage("读取数据集: {0}".format(dataset))

            new_data=desc.name[num:]

            tar_dataset=wk2 + os.sep + new_data 
  
            if arcpy.Exists(tar_dataset)==False: 
  
                arcpy.Copy_management(dataset, tar_dataset)  
  
                arcpy.AddMessage("成功备份数据集: {0}".format(new_data)) 
  
            else:
                arcpy.Delete_management(tar_dataset)

                arcpy.Copy_management(dataset, tar_dataset)  
  
                arcpy.AddMessage("成功备份数据集: {0}".format(new_data))
  
                arcpy.AddMessage("数据集 {0} 已经在目标数据库中存在,将被忽略!".format(new_data)) 
  
        #Clear memory  
  
        del dataset  
  
    except Exception as e:  
  
        arcpy.AddError(e.message); 

#拷贝普通属性表  
def CopyTables(src_db,tar_db,num,prefix):  
  
    try:  
  
        #设置工作空间  
        arcpy.env.workspace = src_db  
  
        wk2 = tar_db  
  
        #遍历tables 
  
        for table in arcpy.ListTables():  
  
            if arcpy.Exists(table)==False:
                continue

            desc = arcpy.Describe(table) 

            if desc.name.startswith(prefix.upper())==False:
                 continue  
  
            arcpy.AddMessage("读取SDE表: {0}".format(table))

            new_data=desc.name[num:]  

            tar_table=wk2 + os.sep + new_data
  
            if arcpy.Exists(tar_table)==False:  
  
                arcpy.Copy_management(table, tar_table)  
  
                arcpy.AddMessage("成功备份SDE表".format(new_data))  
  
            else:  
                arcpy.Delete_management(tar_table)

                arcpy.Copy_management(table, tar_table)  
  
                arcpy.AddMessage("成功备份SDE表".format(new_data))  
  
                arcpy.AddMessage("SDE表 {0} 已经在目标数据库中存在,将被忽略!".format(new_data))  
  
        #Clear memory  
  
        del table  
  
    except Exception as e:  
  
        arcpy.AddError(e.message);  


if __name__== "__main__":

    TIME_FORMAT="%Y%m%d_%H%M%S"

    work_path = r"C:\TEMP\AGS"
    env.overwriteOutput = True

    if os.path.exists(work_path):
        arcpy.AddMessage("work_path exsits")
    else:
        os.makedirs(work_path)
    
    # 接收输入参数 #
    source_sde_settings=arcpy.GetParameterAsText(0).split(",")
    target_sde_settings=arcpy.GetParameterAsText(1).split(",")
    # mdb 文件目录
    mdb_dir_path=arcpy.GetParameterAsText(2)
    
    # 设置源数据库和目标数据库的ArcSDE连接文件位置 #
    source_sde_path=work_path+os.sep+"source.sde"
    target_sde_path=work_path+os.sep+"target.sde"
    
    # 如果不存在.sde 则新建#
    if arcpy.Exists(source_sde_path)==False:
        CreateSdeConnection(work_path,"source.sde",source_sde_settings[0],source_sde_settings[1],source_sde_settings[2])
    if arcpy.Exists(target_sde_path)==False:
        CreateSdeConnection(work_path,"target.sde",target_sde_settings[0],target_sde_settings[1],target_sde_settings[2])

    arcpy.AddMessage("源数据库:{0},连接参数:{1}".format(source_sde_path,source_sde_settings[0]))
    arcpy.AddMessage("目标数据库:{0},连接参数:{1}".format(target_sde_path,target_sde_settings[0]))

    start_num=len(source_sde_settings[1])+1

    # 压缩源数据库
    arcpy.AddMessage("压缩源数据库...");
    arcpy.Compress_management(source_sde_path);

    if len(mdb_dir_path)>0:

        # 创建此次备份的mdb文件
        if os.path.exists(mdb_dir_path)==False:
            os.makedirs(mdb_dir_path)

        file_name=time.strftime(TIME_FORMAT,time.localtime())+".mdb"
        arcpy.CreatePersonalGDB_management(mdb_dir_path,file_name)

        arcpy.AddMessage("开始备份数据至mdb数据库...")

        CopyFeatureClasses(source_sde_path,mdb_dir_path+os.sep+file_name,start_num,source_sde_settings[1])        

    # CopyFeatureClasses(source_sde_path,target_sde_path,start_num,source_sde_settings[1])

    #CopyDatasets(source_sde_path,target_sde_path,start_num,source_sde_settings[1])

    #CopyTables(source_sde_path,target_sde_path,start_num,source_sde_settings[1])

    arcpy.AddMessage("备份操作完成!")