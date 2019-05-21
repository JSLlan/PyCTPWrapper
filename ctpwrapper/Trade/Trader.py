#-*- coding : utf-8 -*-
# coding: utf-8
from ctp.futures import ApiStruct, TraderApi
import threading
import json
import copy


class Trader(TraderApi):

    TIMEOUT = 30

    __RequestID = 0
    __isLogined = False

    def __init__(self):
        self.requestid = ''
        self.broker_id = ''
        self.investor_id = ''
        self.user_id = ''
        self.passwd = ''
        # self.current_trade = ''

    def Connect(self, frontAddr):
        """ connect to front server """
        self.SubscribePrivateTopic(1)
        self.SubscribePublicTopic(1)
        self.RegisterFront(frontAddr)
        self.Init()
        self.__rsp_Connect = dict(event=threading.Event())
        self.__rsp_Connect['event'].clear()
        return 0 if self.__rsp_Connect['event'].wait(self.TIMEOUT) else -4

    def OnFrontConnected(self):
        """ the function will be executed after connection before login """
        self.__rsp_Connect['event'].set()

    def UserLogin(self, broker_id, investor_id, passwd):
        """user login"""
        reqUserLogin = ApiStruct.ReqUserLogin(BrokerID=broker_id, UserID=investor_id, Password=passwd)
        self.__rsp_Login = dict(results=dict(ErrorID = '', ErrorMsg = '', Content = []),
                                event=threading.Event(),
                                RequestID=self.__IncRequestID())
        ret = self.ReqUserLogin(reqUserLogin, self.__rsp_Login['RequestID'])
        if ret == 0:
            self.__rsp_Login['event'].clear()
            if self.__rsp_Login['event'].wait(self.TIMEOUT):
                self.__isLogined = True
                self.__Password = passwd
                return self.__rsp_Login['results']
            else:
                return -4
        return ret

    def OnRspUserLogin(self, RspUserLogin, RspInfo, RequestID, IsLast):
        """ response user login """
        if RequestID == self.__rsp_Login['RequestID'] and IsLast:
            if RspInfo is not None:
                self.__rsp_Login['results'].update(ErrorID = RspInfo.ErrorID)
                self.__rsp_Login['results'].update(ErrorMsg = RspInfo.ErrorMsg)
            if RspUserLogin is not None:
                print(RspUserLogin)
                updatedContent = self.__rsp_Login['results'].get('Content')
                updatedContent.append(RspUserLogin)
                self.__rsp_Login['results'].update(Content=updatedContent)
            if IsLast:
                self.__rsp_Login['event'].set()

    def QryTrade(self, brokerID, investorID):
        """query today's trade records"""

        reqQryTrade = ApiStruct.QryTrade(BrokerID=brokerID, InvestorID=investorID)
        self.__rsp_QryTrade = dict(results=dict(ErrorID = '', ErrorMsg = '', Content = []),
                                   RequestID=self.__IncRequestID(),
                                   event=threading.Event())
        ret = self.ReqQryTrade(reqQryTrade, self.__rsp_QryTrade['RequestID'])

        if ret == 0:
            self.__rsp_QryTrade['event'].clear()
            if self.__rsp_QryTrade['event'].wait(self.TIMEOUT):
                return self.__rsp_QryTrade['results']
            else:
                return -4
        return ret

    def OnRspQryTrade(self, rspTrade, RspInfo, RequestID, IsLast):
        """response of query today's trade records"""
        trade = copy.deepcopy(rspTrade)
        if RequestID == self.__rsp_QryTrade['RequestID']:
            if RspInfo is not None:
                self.__rsp_QryTrade['results'].update(ErrorID = RspInfo.ErrorID)
                self.__rsp_QryTrade['results'].update(ErrorMsg = RspInfo.ErrorMsg)
            if trade is not None:
                self.__rsp_QryTrade['results'].get('Content').append(trade)
            if IsLast:
                self.__rsp_QryTrade['event'].set()

    def trade_to_dict(self, Trade):
        result = {
            'broker_id': Trade.BrokerID,
            'investor_id': Trade.InvestorID,
            'instrument_id': Trade.InstrumentID,
            'order_ref': Trade.OrderRef,
            'user_id': Trade.UserID,
            'exchange': Trade.ExchangeID,
            'trade_id': Trade.TradeID,
            'direction': Trade.Direction,
            'order_sys_id': Trade.OrderSysID,
            'ParticipantID': Trade.ParticipantID,
            'client_id': Trade.ClientID,
            'trading_role': Trade.TradingRole,
            'exchange_ins_id': Trade.ExchangeInstID,
            'offset_flag': Trade.OffsetFlag,
            'hedge_flag': Trade.HedgeFlag,
            'price': Trade.Price,
            'volume': Trade.Volume,
            'trade_date': Trade.TradeDate,
            'trade_time': Trade.TradeTime,
            'trade_type': Trade.TradeType,
            'price_source': Trade.PriceSource,
            'oder_local_id': Trade.OrderLocalID,
            'clearing_part_id': Trade.ClearingPartID,
            'business_unit': Trade.BusinessUnit,
            'sequence_no': Trade.SequenceNo,
            'trading_day': Trade.TradingDay,
            'settlement_id': Trade.SettlementID,
            'broker_order_seq': Trade.BrokerOrderSeq,
            'trade_source': Trade.TradeSource
        }
        return result

    def QryExchange(self, ExchangeID=b''):
        """ query exchange """
        QryExchangeField = ApiStruct.Exchange(ExchangeID=ExchangeID)
        self.__rsp_QryExchange = dict(results=dict(ErrorID = '', ErrorMsg = '', Content = []),
                                      RequestID=self.__IncRequestID(),
                                      event=threading.Event())
        ret = self.ReqQryExchange(QryExchangeField, self.__rsp_QryExchange['RequestID'])
        if ret == 0:
            self.__rsp_QryExchange['event'].clear()
            if self.__rsp_QryExchange['event'].wait(self.TIMEOUT):
                return self.__rsp_QryExchange['results']
            else:
                return -4
        return ret

    def OnRspQryExchange(self, Exchange, RspInfo, RequestID, IsLast):
        """ response of query exchange """
        exchange = copy.deepcopy(Exchange)
        if RequestID == self.__rsp_QryExchange['RequestID']:
            if RspInfo is not None:
                self.__rsp_QryExchange['results'].update(ErrorID = RspInfo.ErrorID)
                self.__rsp_QryExchange['results'].update(ErrorMsg = RspInfo.ErrorMsg)
            if exchange is not None:
                self.__rsp_QryExchange['results'].get('Content').append(exchange)
            if IsLast:
                self.__rsp_QryExchange['event'].set()

    def UserLogout(self):
        """ request logout """
        reqUserLogout = ApiStruct.UserLogout(BrokerID=self.broker_id, UserID=self.user_id)
        self.__rsp_Logout = dict(results=dict(ErrorID = '', ErrorMsg = '', Content = []),
                                 RequestID=self.__IncRequestID(),
                                 event=threading.Event())
        ret = self.ReqUserLogout(reqUserLogout, self.__rsp_Logout['RequestID'])
        if ret == 0:
            self.__rsp_Logout['event'].clear()
            if self.__rsp_Logout['event'].wait(self.TIMEOUT):
                self.__isLogined = False
                return self.__rsp_Logout['results']
            else:
                return -4
        return ret

    def OnRspUserLogout(self, RspUserLogout, RspInfo, RequestID, IsLast):
        """ response of user logout """
        if RequestID == self.__rsp_Logout['RequestID'] and IsLast:
            if RspInfo is not None:
                if RspInfo is not None:
                    self.__rsp_Logout['results'].update(ErrorID=RspInfo.ErrorID)
                    self.__rsp_Logout['results'].update(ErrorMsg=RspInfo.ErrorMsg)
                if RspUserLogout is not None:
                    updatedContent = self.__rsp_Logout['results'].get('Content')
                    updatedContent.append(RspUserLogout)
                    self.__rsp_Logout['results'].update(Content=updatedContent)
                if IsLast:
                    self.__rsp_Logout['event'].set()

    def __IncRequestID(self):
        """ auto-increment request ID """
        self.__RequestID += 1
        return self.__RequestID

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

    def OnRtnDepthMarketData(self, depth_market_data):
        print ("Depth Market Data Return: ")
        print depth_market_data.BidPrice1,depth_market_data.BidVolume1,depth_market_data.AskPrice1,depth_market_data.AskVolume1,depth_market_data.LastPrice,depth_market_data.Volume,depth_market_data.UpdateTime,depth_market_data.UpdateMillisec,depth_market_data.InstrumentID

    def OnRspQryInvestor(self, pInvestor, pRspInfo, nRequestID, bIsLast):
        print("Query Investor Return: ")
        print(pInvestor, pRspInfo)

    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        print("Return OnRspSettlementInfoConfirm: ")
        print(pSettlementInfoConfirm, pRspInfo)