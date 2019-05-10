#-*- coding : utf-8 -*-
# coding: utf-8
from Trade.Trader import Trader
import time


def main():

    # define a trader object
    trader = Trader()
    trader.broker_id = "0001"
    trader.user_id = "00119"
    trader.investor_id = "00119"
    trader.passwd = "130652"
    trader.Create("trader")

    # trader object can perform several actions
    print('action-connect to front',
          trader.Connect('tcp://58.32.236.39:21205'))

    print('action-user login',
          trader.UserLogin(trader.broker_id, trader.investor_id, trader.passwd))

    time.sleep(1.0)
    print('action-query trade',
          trader.QryTrade(trader.broker_id, trader.investor_id))

    time.sleep(1.0)
    print('action-query exchange',
          trader.QryExchange())

    time.sleep(1.0)
    print('action-logout',
          trader.UserLogout())


if __name__ == "__main__":
    main()