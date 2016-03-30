#!/usr/bin/python
#-*- coding:utf-8 -*-

__author__ = 'Francics'

## from ParseFile import ParseFile
import os.path
from openpyxl import load_workbook

class ParseFileForNmon():
    def __init__(self):
        ##super(ParseFile,self).__init__()
        self.__workbook = None
        self.__filename = None
        self.__worksheet = None
   
    def Open(self,filename,encode='GBK'):
        if not isinstance(filename,str):
            raise TypeError('filename must be str')
      
        if not os.path.exists(filename):
            raise IOError('file: %s not exist' % filename)
      
        self.__workbook = load_workbook(filename, read_only=True)
        self.__filename = filename

    def Close(self):
        if self.__workbook:
            self.__workbook = None
            self.__filename = None
            self.__workbook = None
   
    def Readline(self):
        '''
        迭代单元格,利用生成器简化读取
        :return:generator
        '''
        if self.__worksheet:
            raise  ValueError("you need select a worksheet")
        for row in self.__worksheet.rows:
            yield [x.value for x in row]

   
    def isOpen(self):
        return True if self.__workbook else False
   
    def get_filename(self):
        return self.__filename

    def get_sheet(self,sheetname):
        try:
            self.__worksheet=self.__workbook[sheetname]
        except KeyError :
            raise KeyError('file:[%s] not exist sheet[%s]' %(self.__filename,sheetname) )
   