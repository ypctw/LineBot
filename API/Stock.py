import requests
import pandas as pd
import yfinance as yf
import os
from dotenv import load_dotenv
import alpha_vantage
from datetime import date, timedelta
from pandas_datareader import data as pdr

class TaiwanStock():
    def __init__(self):
        self.__network = 'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch='

    def getJson(self, Stock, TSEoOTC='tse_'):
        """
        Stock : input Stock ID
        TSEorTOC : (TSE)在交易所掛牌通常稱上市 or (TOC)在櫃買中心掛牌通常稱上櫃
        """
        dictJson = {"name":"","當日最低":"0","當日最高":"0","當下價格":"0","昨日收盤價":"0","開盤":"0"}

        try:
            url = self.__network + 'tse_' + Stock + '.tw&json=1&delay=0'
            print(url)
            r = requests.get(url)
            datum = r.json()
            if len(datum['msgArray']) == 0:
                url = self.__network + 'otc_' + Stock + '.tw&json=1&delay=0'
                r = requests.get(url)
                datum = r.json()
            dictJson["當日最低"] = datum['msgArray'][0]['l']
            try:
                dictJson["name"] = datum['msgArray'][0]['nf']
            except:
                dictJson["name"] = datum['msgArray'][0]['n']
            dictJson["當日最高"] = datum['msgArray'][0]['h']
            dictJson["當下價格"] = datum['msgArray'][0]['z']
            dictJson["昨日收盤價"] = datum['msgArray'][0]['y']
            dictJson["開盤"] = datum['msgArray'][0]['o']
        except:
            dictJson = {"name":"網路逾時，請重新查找","當日最低":"-","當日最高":"-","當下價格":"-","昨日收盤價":"-","開盤":"-"}
        return dictJson

def LastDay():
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime('20%y%m%d')

class USAStock():
    def __init__(self):
        load_dotenv()
        alphavantage_APIKEY = os.getenv("alphavantage_APIKEY", None)
        self.__network_Prefix = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
        self.__network_Suffix = "&apikey=" + alphavantage_APIKEY
        self.__network_Prefix_Recent = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
        self.__network_Suffix_Recent = "&interval=5min&apikey=" + alphavantage_APIKEY
        self.INDEX = {"DJI":"DOW JONES","GSPC":"S&P 500","IXIC":"NASDAQ","NDX":"NASDAQ-100"}
    def getJson(self, Symbol):
        """
        Symbol : Stock Symbol
        NASDAQ => https://github.com/prediqtiv/alpha-vantage-cookbook/blob/master/data/NASDAQ.txt
        """
        dictJson = {"name":Symbol,"當日最低":"0","當日最高":"0","當下價格":"0","昨日收盤價":"0","開盤":"0"}
        if Symbol == "DJI" or Symbol == "GSPC" or Symbol == "IXIC" or Symbol == "NDX":
            datum = pdr.get_data_yahoo("^"+Symbol,CountDay(7), CountDay(0))
            index = 0
            dictJson["name"] = self.INDEX[Symbol]
            for i in reversed(datum["Adj Close"]):
                index += 1
                if index == 2:
                    dictJson["昨日收盤價"] = str(i)
                    break
            for i in reversed(datum['High']):
                dictJson["當日最高"] = str(i)
                break
            for i in reversed(datum['Low']):
                dictJson["當日最低"] = str(i)
                break
            for i in reversed(datum['Close']):
                dictJson["當下價格"] = str(i)
                break
            for i in reversed(datum['Open']):
                dictJson["開盤"] = str(i)
                break
            return dictJson
        url = self.__network_Prefix + Symbol + self.__network_Suffix
        url_recent = self.__network_Prefix_Recent + Symbol + self.__network_Suffix_Recent
#         try:
        r = requests.get(url)
        r_recent = requests.get(url_recent)
        datum = r.json()
        datum_recent = r_recent.json()
        try:
            dictJson["name"] = datum['Meta Data']['2. Symbol']
            index = 0
            for i in datum['Time Series (Daily)']:
                index += 1
                if index == 1:
                    dictJson["當日最低"] = datum['Time Series (Daily)'][i]['3. low']
                    dictJson["當日最高"] = datum['Time Series (Daily)'][i]['2. high']
                    dictJson["開盤"] = datum['Time Series (Daily)'][i]['1. open']
                if index == 2:
                    dictJson["昨日收盤價"] = datum['Time Series (Daily)'][i]['4. close']
                    break
            for i in datum_recent['Time Series (5min)']:
                dictJson["當下價格"] = datum_recent['Time Series (5min)'][i]['4. close']
                break
        except:
            dictJson = {"name":"網路逾時，請重新查找","當日最低":"-","當日最高":"-","當下價格":"-","昨日收盤價":"-","開盤":"-"}
        return dictJson


class CryptoStock():
    def __init__(self):
        self.__network_Prefix = "https://api.coinbase.com/v2/exchange-rates?currency="
    def getJson(self, crypto):
        dictJson = {"crypto":crypto,"USDC":0,"TWD":0}
        url = self.__network_Prefix + crypto
        try:
            r = requests.request("GET",url)
            datum = r.json()
            dictJson['USDC'] = datum['data']['rates']['USDC']
            dictJson['TWD'] = datum['data']['rates']['TWD']
        except:
            dictJson = {"crypto":None,"USDC":0,"TWD":0}
        return dictJson


def CountDay(count):
    day = date.today() - timedelta(days=count)
    return day.strftime("20%y-%m-%d")




#
# a = CryptoStock()
# datum = a.getJson('ETH')
# print(datum)
