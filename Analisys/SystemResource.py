#!/usr/bin/python
#-*- coding:utf-8 -*-

__author__ = 'Francics'

'''
主要功能用于保存单日系统资情况
'''

class SystemResource():
   
    __slots__ = ('__cpu',"__io","__stime","__index",'SRCTYP')
   
    def __init__(self):
        self.__cpu = []
        self.__io = []
        self.__stime = []
        self.__index = 0
        self.SRCTYP = ('cpu','io')
      
    def AddSysRsc(self,stime,cpu,io):
        self.__cpu.append(cpu)
        self.__io.append(io)
        self.__stime.append(stime)
   
    def __iter__(self):
        self.__index = 0
        return self
   
    def __next__(self):
        i = self.__index
        if self.__index >= len(self.__stime):
            raise StopIteration
        else:
            self.__index += 1
        return self.__stime[i],self.__cpu[i],self.__io[i]
   
    def __getitem__(self,i):
        return self.__stime[i],self.__cpu[i],self.__io[i]
      
    def RscAvg(self,systyp):
        if systyp not in SRCTYP:
            raise TypeError("systyp must in %" % SRCTYP)
      
        if systyp == 'cpu':
            cpuall = 0
            for cpu in self.__cpu:
                cpuall += cpu
         
            return round(cpuall/len(self.__cpu), 2)
        elif systyp == 'io':
            ioall = 0
            for io in self.__io:
                ioall += io
            
            return round(ioall/len(self.__io), 2)
  
    def Max(self,systyp):
        if systyp not in self.SRCTYP:
            raise TypeError("systyp must in %" % self.SRCTYP)
      
        if systyp == 'cpu':
            return max(self.__cpu)
        elif systyp == 'io':
            return max(self.__io)
   
    def Min(self,systyp):
        if systyp not in self.SRCTYP:
            raise TypeError("systyp must in %" % self.SRCTYP)
      
        if systyp == 'cpu':
            return min(self.__cpu)
        elif systyp == 'io':
            return min(self.__io)
   
if __name__ == "__main__":
   sysrsc = SystemResource()
   sysrsc.AddSysRsc('00:00:05',10.2,8141)
   sysrsc.AddSysRsc('00:01:00',20.1,8124)
   sysrsc.AddSysRsc('00:05:05',30.1,8123)
   
   print('Max(cpu):',sysrsc.Max('cpu'))
   print('Max(io):',sysrsc.Max('io'))
   
  