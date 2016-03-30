#!/usr/bin/python
#-*- coding:utf-8 -*-

__author__ = 'Francics'

from ParseFile import ParseFile
import os.path
import re
import codecs

#def ParseFileForTlog(ParseFile):
class ParseFileForTlog():
   def __init__(self):
      ##super(ParseFile,self).__init__()
      self.__f = None
      self.__filename = None
   
   def Open(self,filename,encode='GBK'):
      if not isinstance(filename,str):
         raise TypeError('filename must be str')
      
      if not os.path.exists(filename):
         raise IOError('file: %s not exist' % filename)
      
      self.__f = codecs.open(filename,'r',encoding = encode)
      self.__filename = filename
   
   def Readline(self):
      line = self.__f.readline()
      mcompile = re.split(' *',line)
      
      if '交易日期:' in mcompile:
         return [mcompile[2]]
      
      if len(mcompile) != 9 and '失败' not in mcompile:
         if mcompile == ['']:
            raise EOFError('Read file:[%s] End' % self.__filename)
         return None
      
      ##重构list.使元素满足9个
      if '失败' in mcompile:
         mcompile.insert(5,'None')
         
      return mcompile
   
   def Close(self):
      if self.__f:
         self.__f.close()
         self.__f = None
   
   def get_filename(self):
      return self.__filename
   
   def isOpen(self):
      return True if self.__f else False
         
   
   
      