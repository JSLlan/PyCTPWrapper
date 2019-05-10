#-*- coding : utf-8 -*-
# coding: utf-8
from Trade.Trader import Trader
import time


def main():

    # define a trader object
    trader = Trader()
    trader.broker_id = ""
    trader.user_id = ""
    trader.investor_id = ""
    trader.passwd = ""
    trader.Create("trader")

    # trader object can perform several actions
    print('action-connect to front',
          trader.Connect(''))

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