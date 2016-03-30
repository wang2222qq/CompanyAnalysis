#!/usr/bin/python
#-*- coding:utf-8 -*-

__author__ = 'Francics'

'''
进行流程调度
'''

from ParseFile.ParseFileForNmon import ParseFileForNmon
from ParseFile.ParseFileForTlog import ParseFileForTlog
from WriteFile.WriteFile import WriteFile
from Analisys.Translate import Translate
from Config.Config import OUT_BUSINESS_SEQNO,OUT_BUSENESS_NAME,INFILETYPE

import os,logging
from myfunc import mylog

WORKPATH=r'H:\myPythonModule\DataAnalysis'


class AnalysisConfigure():

    def __init__(self):
        self.__parsefile = None
        self.__writefile = WriteFile()
        self.__translate = Translate()

    def __GetParseFile(self,filetype):
        '''
        将输入filetype转换对应的解析类
        :param filetype:
        :return:
        '''
        if INFILETYPE.get(filetype,'') == 'Tlog':
            self.__parsefile = ParseFileForTlog()
        elif INFILETYPE.get(filetype,'') == 'Nmon':
            self.__parsefile = ParseFileForNmon()
        else:
            raise TypeError("filetype no this option[%s]" % filetype )

    def __Parse(self,filename):
        '''
        逐行解析文件。生成器
        :param filename:
        :return:
        '''

        self.__parsefile.Open(filename)
        i=0
        while True:
            try:
                if isinstance(self.__parsefile, ParseFileForNmon):
                    pass
                elif isinstance(self.__parsefile, ParseFileForTlog):
                    line = self.__parsefile.Readline()
                    if line == None:
                        continue
                    if len(line) == 1:
                        self.__translate.SetTransDate(line[0])
                    elif line:
                        t = line[2:-2:1]
                        self.__translate.AddVolume(*t)
                i=i+1
            except EOFError as e:
                self.__parsefile.Close()
                break
            except TypeError as e:
                print("错误发生在解析文件的第%d行" % i)
                print(e)
                raise

    def __TlogWriteFile(self,outfilename):
        """

        :type self: object
        """
        self.__writefile.Open(outfilename)
        #####工作簿:交易汇总情况
        self.__writefile.setSheet("交易汇总情况")

        firstLine = ["交易日期","交易总量"]
        firstLine.extend(OUT_BUSENESS_NAME)

        curRow=len(self.__writefile.rows[0])
        if curRow == 0:
            self.__writefile.WriteLine(1,firstLine)

        curRow=len(self.__writefile.rows)
        lLine = [self.__translate.GetTransDate(),self.__translate.GetTotalVolume()]
        for mType in OUT_BUSINESS_SEQNO:
            try:
                volume = self.__translate.GetBusinessVolume(mType)
            except KeyError as e:
                volume = 0

            lLine.append(volume)
        self.__writefile.WriteLine(curRow+1,lLine)

        #####工作簿:交易分类
        firstLine = ["交易代号","交易平均时间(s)",
                     "失败笔数","失败率(%)","超时笔数(20s)","超时率(%)","交易总量"]

        self.__writefile.setSheet("%s交易分类情况" % self.__translate.GetTransDate())

        curRow=len(self.__writefile.rows[0])
        if curRow == 0:
            self.__writefile.WriteLine(1,firstLine)

        for txnid in self.__translate.GetAllTxnid().keys():
            lLine = [txnid,
                     self.__translate.TxnAvgTime(txnid)[0],
                     self.__translate.TxnFailNum(txnid),
                     self.__translate.TxnFailPer(txnid),
                     self.__translate.TxnAvgTime(txnid,20)[1],
                     self.__translate.OverTimePer(txnid,20),
                     self.__translate.GetTxnidVolume(txnid)
                     ]
            curRow=len(self.__writefile.rows)
            self.__writefile.WriteLine(curRow+1, lLine)

        ##写入到磁盘中
        self.__writefile.Save()
        self.__writefile.Close()

    def __NmonWriteFile(self,outfilename):
        '''
        通过SysResourc类重构输出
        :param outfilename: 输出文件绝对路径
        :return:
        '''
        self.__writefile.Open(outfilename)
        self.__writefile.setSheet()
    @mylog.log
    def Run(self,infilename,outfilename,filetype):
        self.__GetParseFile(filetype)
        ###读取文件到内存中
        self.__Parse(infilename)
        ### 根据filetype选择元数据类 重组数据
        if INFILETYPE.get(filetype,'') == 'Tlog':
            self.__TlogWriteFile(outfilename)
        elif INFILETYPE.get(filetype,'') == 'Nmon':
            pass
        elif INFILETYPE.get(filetype,'') == 'EveryCheck':
            pass

        self.__parsefile.Close()

if __name__ == '__main__':
   aly = AnalysisConfigure()
   aly.Run(WORKPATH+r'\eg\T2016-02-06-00_10_19.log',WORKPATH+r'\test.xlsx',0)