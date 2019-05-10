#-*- coding : utf-8 -*-
# coding: utf-8
"This is the main demo file"
from ctp.futures import ApiStruct, TraderApi
import time
import traceback
import sys
import threading


class MyTraderApi(TraderApi):
    TIMEOUT = 30

    __RequestID = 0
    __isLogined = False

    def __init__(self, broker_id,
                 investor_id, passwd, *args,**kwargs):
        self.requestid = 0
        self.broker_id =broker_id
        self.investor_id = investor_id
        self.passwd = passwd

    def __IncRequestID(self):
        """ 自增并返回请求ID """
        self.__RequestID += 1
        return self.__RequestID

    def __IncOrderRef(self):
        """ 递增报单引用 """
        OrderRef = bytes('%012d' % self.__OrderRef, 'GBK')
        self.__OrderRef += 1
        return OrderRef

    def OnRspError(self, info, RequestId, IsLast):
        print (" Error")
        self.isErrorRspInfo(info)

    def isErrorRspInfo(self, info):
        if info.ErrorID !=0:
            print ("ErrorID=", info.ErrorID, ", ErrorMsg=", info.ErrorMsg.decode("GBK"))
        return info.ErrorID != 0

    def OnFrontDisConnected(self, reason):
        print ("Front DisConnected:", reason)

    def OnHeartBeatWarning(self, time):
        print ("Heart Beat Warning", time)

    def OnFrontConnected(self):
        print ("Front Connected: ")
        self.user_login(self.broker_id, self.investor_id, self.passwd)

    def user_login(self, broker_id, investor_id, passwd):
        req = ApiStruct.ReqUserLogin(BrokerID=broker_id, UserID=investor_id, Password=passwd)

        self.requestid += 1
        self.ReqUserLogin(req, self.requestid)

    def OnRspUserLogin(self, RspUserLogin, RspInfo, rid, IsLast):
        """ 登录请求响应 """
        print("login response: ")
        print(RspUserLogin)
        print(RspInfo.ErrorMsg.decode("GBK"))
        reqQryTrade = ApiStruct.QryTrade(self.broker_id, self.investor_id)
        self.__rsp_QryTrade = dict(results=[], RequestID=self.__IncRequestID(), ErrorID=0,
                                   event=threading.Event())
        self.ReqQryTrade(reqQryTrade, self.__rsp_QryTrade['RequestID'])

    def OnRtnDepthMarketData(self, depth_market_data):
        print ("Depth Market Data Return: ")
        print depth_market_data.BidPrice1,depth_market_data.BidVolume1,depth_market_data.AskPrice1,depth_market_data.AskVolume1,depth_market_data.LastPrice,depth_market_data.Volume,depth_market_data.UpdateTime,depth_market_data.UpdateMillisec,depth_market_data.InstrumentID

    def OnRspQryInvestor(self, pInvestor, pRspInfo, nRequestID, bIsLast):
        print("Query Investor Return: ")
        print(pInvestor, pRspInfo)

    def OnRspQryTrade(self, pTrade, pRspInfo, nRequestID, bIsLast):
        print("Query Trade Return: ")
        print(pTrade)

    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        print("Return OnRspSettlementInfoConfirm: ")
        print(pSettlementInfoConfirm, pRspInfo)


def main():
    # user = MyTraderApi(broker_id="9999",investor_id="089303",passwd="198759")
    user = MyTraderApi(broker_id="0001",investor_id="00119",passwd="130652")

    user.Create("trader")
    # user.RegisterFront("tcp://180.168.146.187:10001")
    user.RegisterFront("tcp://58.32.236.39:21205")

    user.SubscribePrivateTopic(2) # only accept contents after login
    user.SubscribePublicTopic(1) # accept contents since last disconnect
    user.Init()


    user.Join()
    # print(len(MyTraderApi.staticvariable))


if __name__=="__main__":
    main()
