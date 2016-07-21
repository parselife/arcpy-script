# Name: del_overdue_mdb.py
# Description: 删除过期的mdb备份文件
# Author: alex

# -*- coding:utf-8 -*-
import os,time
import arcpy
from arcpy import env
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

# 两个时间之间的间隔天数
# 时间数据必须都是localtime格式
def DaysDiff(start_time,end_time):
	try:
		s_year=start_time.tm_year
		e_year=end_time.tm_year

		s_yday=start_time.tm_yday
		e_yday=end_time.tm_yday

		diff_year=e_year-s_year
		diff_day=e_yday-s_yday

		return abs(diff_day)+abs(diff_year)*365
		
	except Exception, e:
		arcpy.AddError(e.message);
	

if __name__== "__main__":

	# 设置备份文件目录
	work_path=arcpy.GetParameterAsText(0)

	# 设置超期天数
	days_overdue=int(arcpy.GetParameterAsText(1))

	if os.path.exists(work_path)==False:
		arcpy.AddError("指定目录{0}不存在".format(work_path));

	i=0
	for f in os.listdir(work_path):
		f_mtime=time.localtime(os.path.getmtime(work_path+os.sep+f))
		arcpy.AddMessage("文件{0} 生成时间 {1}".format(f,time.strftime("%Y-%m-%d %H:%M:%S",f_mtime)))
		if DaysDiff(f_mtime,time.localtime())>=days_overdue:
			arcpy.AddMessage("文件 {0} 已经超过设定的天数期限 {1},即将删除...".format(f,days_overdue))
			try:
				arcpy.Delete_management(f)
				arcpy.AddMessage("文件 {0} 删除成功!".format(f))
				i=i+1
			except Exception, e:
				arcpy.AddError(e.message)

	arcpy.AddMessage("本次共删除 {0} 个过期文件.".format(i))