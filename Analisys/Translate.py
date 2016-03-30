#!/usr/bin/python
#-*- coding:utf-8 -*-

__author__ = 'Francics'

'''
主要功能用于分析交易情况类
'''

class Translate():

    __slots__ = ('__volume','__business','__txnid','__transdate')
   
    def __init__(self):
        self.__volume = 0
        self.__business  = {}
        self.__txnid = {}
        self.__transdate = '1990-01-01'
      
    def _TranslatorTime(self,stime):
        '''
        将stime转换证int型.其中stime格式为hhmmss
        '''
        if not isinstance(stime,str):
            raise TypeError('stime must be str')
        return (int)(stime[0:2])*3600 + (int)(stime[2:4])*60 + (int)(stime[4:6])
     
    def AddVolume(self,businessName,txnid,bgntm,endtm,result):
        paras = {'businessName':businessName,'txnid':txnid,
              'bgntm':bgntm,'endtm':endtm,'result':result}
      
        for key,value in paras.items():
            if not isinstance(value,str):
                raise TypeError('argument %s type must be str' % key)

        self.__volume += 1
      
        if businessName in self.__business:
            self.__business[businessName] += 1
        else:
            self.__business[businessName] = 1
      
        if not txnid in self.__txnid:
            self.__txnid[txnid] = []
      
        self.__txnid[txnid].append((bgntm,endtm,result))
      
      
    def SetTransDate(self,mdate):
        if not isinstance(mdate, str):
            raise TypeError("mdate must be str")
      
        if len(mdate) == 8:
            self.__transdate = mdate[0:4]+"-"+mdate[4:6]+"-"+mdate[6:8]
        elif len(mdate) == 10:
            self.__transdate = mdate
        else:
            raise TypeError("mdate数据长度只能为8或10")
      
    def GetTransDate(self):
        return self.__transdate
      
    def GetTotalVolume(self):
        return self.__volume
   
    def GetBusinessVolume(self,businessName):
        return self.__business[businessName]
   
    def GetTxnidVolume(self,txnid):
      
        if not txnid in self.__txnid:
            raise KeyError('不存在相应交易代号TXNID:%s' % txnid )
        return len(self.__txnid[txnid])
       
    def GetAllTxnid(self):
        return self.__txnid
   
    def TxnAvgTime(self,txnid,iWhere=0):
        '''
        用于统计交易代号中不小于指定条件iWhere时间差的交易平均时差
        返回：
            tuple(平均时间,数量)
        '''
      
        if not txnid in self.__txnid:
            raise KeyError('不存在相应交易代号TXNID:%s' % txnid )
      
        if not isinstance(iWhere,int):
            raise TypeError("iWhere must be int")
      
        total_diff_time = 0
        iNumber = 0
        iOverNum = 0
        for trans in self.__txnid[txnid]:
            if trans[1] == 'None':
                continue
            difftime = self._TranslatorTime(trans[1]) - self._TranslatorTime(trans[0])
         
            if difftime >= iWhere:
                total_diff_time += difftime
                iOverNum += 1
            iNumber += 1

        return (round( (total_diff_time/iNumber) , 2), iOverNum)
   
   
    def TxnFailNum(self,txnid):
        '''
        交易失败笔数
        '''
        if not txnid in self.__txnid:
            raise KeyError('不存在相应交易代号TXNID:%s' % txnid )
         
        Num = 0
        for trans in self.__txnid[txnid]:
            if trans[2] != '成功':
                Num += 1
      
        return Num
   
    def TxnFailPer(self,txnid):
        '''
        交易的失败率
        '''
        return round(self.TxnFailNum(txnid)/len(self.__txnid[txnid])*100, 2)
   
    def OverTimePer(self,txnid,iWhere):
        '''
        根据指定的iWhere计算超时率
        :param txnid: 交易编号
        :param iWhere: 超时时间
        :return: float
        '''
        return round(self.TxnAvgTime(txnid,iWhere)[1]/len(self.__txnid[txnid])*100, 2)