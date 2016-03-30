#!/usr/bin/ptyhon
#-*- coding:utf-8 -*-

__author__ = 'Francics'

INFILETYPE = {0:'Tlog',1:'Nmon',2:'EveryCheck'}
OUTFILETYPE = {0:'volume',1:'txnid',2:'sysrscday',3:'sysrsctotal'}

###OUT_BUSINESS_SEQNO 与 OUT_BUSENESS_NAME 在顺序上是对应关系
OUT_BUSINESS_SEQNO = ('adpk','adts','call','draf','feb0','ipay','msgt','smng')
OUT_BUSENESS_NAME = ('批扣交易','柜面','呼叫中心','电票交易','短信发送交易','网上银行','电话银行','秘钥同步')