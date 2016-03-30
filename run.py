#!/usr/bin/python
#-*- coding:utf-8 -*-

__author__ = 'Francics'

from AnalysisConfigure import AnalysisConfigure
import os,os.path
import re
from codecs import open

WORKPATH=r'H:\myPythonModule\DataAnalysis'
INPUTFILEPATH=r'G:\1.公司\6.数据统计\收集数据\Tlog\\'
OUTFILEPATH=r'G:\1.公司\6.数据统计\分析数据\Tlog_xlsx\\'

def DelFileLine(filename,bgnline,endline):
   '''
   parament:
      filename
      bgnline  int  待删除文件的开始行数
      endline  int  待删除文件的结束行数
   '''
   if not isinstance(bgnline,int):
      raise TypeError('bgnline must be int')

   if not isinstance(endline,int):
      raise TypeError('endline must be int')

   try:
      with open(filename,'rb') as f:
         lines = f.readlines()
   except FileNotFoundError :
      print('文件:[%s]不存在' % filename)
      raise

   del lines[bgnline:endline]
   open(filename,'wb').writelines(lines)

if __name__ == "__main__":
   FILENAME='交易分析.xlsx'
   if os.path.exists(OUTFILEPATH+FILENAME):
      os.remove(OUTFILEPATH+FILENAME)
   for filename in os.listdir(INPUTFILEPATH):
      print("filename:[%s]" % filename)
      m = re.search("T[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}_[0-9]{2}_[0-9]{2}.log",filename)
      if m == None:
         continue

      try:
         aly = AnalysisConfigure()
         aly.Run(INPUTFILEPATH+m.group(), OUTFILEPATH+FILENAME, 0)
      except UnicodeDecodeError as e:
         del aly
         DelFileLine(INPUTFILEPATH+m.group(),1,31)
         aly = AnalysisConfigure()
         aly.Run(INPUTFILEPATH+m.group(),OUTFILEPATH+FILENAME,0)
      else:
         del aly
