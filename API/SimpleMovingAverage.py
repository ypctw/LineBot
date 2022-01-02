from pandas_datareader import data as pdr
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator
import mplfinance as mpf
from dotenv import load_dotenv
import os
import pyimgur

class SimpleMovingAverage():
    def __init__(self,   stock="AAPL",
                         stype='short',
                         start="2021-07-01",
                         end="2021-12-31"
                        ):
        load_dotenv()
        if stock =='t00.TW':
            stock = "^TWII"
        self.Imgur_Client_ID = os.getenv("Imgur_Client_ID", None)
        self.__start = start
        self.__end  =  end
        self.__stock_name = stock
        self.__stock = self.fetchJson(stock)
        mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
        self.__s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
        self.__stype = stype


    def fetchJson(self,stock):
        return pdr.get_data_yahoo(stock, self.__start, self.__end)

    def DataFrame_Index(self):
         self.__stock.index =  self.__stock.index.strftime("%Y-%m-%d")

    def stock(self):
        return self.__stock
    def stock_name(self):
        return self.__stock_name
    def Image(self):
        if self.__stype == 'short':
            self.min,self.max = 5,10
            kwargs = dict(type='candle', mav=(5,10), volume=True, figratio=(500,300), figscale=1, title=self.__stock_name + " Short", style=self.__s,savefig="./Image/SMA.png")
        elif self.__stype == 'medium':
            self.min,self.max = 20,60
            kwargs = dict(type='candle', mav=(20,60), volume=True, figratio=(500,300), figscale=1, title=self.__stock_name + " Medium", style=self.__s,savefig="./Image/SMA.png")
        elif self.__stype == 'long':
            self.min,self.max = 120,240
            kwargs = dict(type='candle', mav=(120,240), volume=True, figratio=(500,300), figscale=1, title=self.__stock_name + " Long", style=self.__s,savefig="./Image/SMA.png")
        mpf.plot(self.__stock, **kwargs)
    def upload_url(self):
        self.Image()
        im = pyimgur.Imgur(self.Imgur_Client_ID)
        uploaded_image = im.upload_image("./Image/SMA.png", title= self.__stype + "SMA")
        return uploaded_image.link

#     def Analysis(self):
#         self.SMA = SMA()
#         self.Min_Array = self.SMA(self.min)
#         self.Max_Array = np.array(self.SMA(self.max)
#
#
#
# class SMA():
#     def __init__(self, stock):
#         self.__Stock_dict = stock.to_dict()
#     def MA_Index(self,index):
#         MD = {}
#         queue = []
#         for date in self.__Stock_dict['Adj Close']:
#             if len(queue) == index:
#                 MD[date] = (sum(queue) / len(queue))
#                 queue.pop(0)
#             queue.append(self.__Stock_dict['Adj Close'][date])
#         return MD
#
# # a = SimpleMovingAverage(stype='medium')
# print(a.upload_url())
