from transitions import Machine
from linebot.models import ImageSendMessage, ImageCarouselColumn, URITemplateAction, MessageTemplateAction, TemplateSendMessage,ImageCarouselTemplate,FlexSendMessage
from API.Stock import TaiwanStock, USAStock, CryptoStock
from API.Flex_message import Flex_Message_Crypto, TW_Stock_Each
from API.SimpleMovingAverage import SimpleMovingAverage as SMA
import json
from utils import send_text_message, send_button_message_NoneURL, send_Multi_Image, send_Flex_message, CountDay,send_button_message_URL
class TocMachine(Machine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.TW_STOCK = TaiwanStock()
        self.US_STOCK = USAStock()
        self.CRYPTO_STOCK = CryptoStock()
    # State 1 #
    def is_going_to_Start(self, event):
        return True
    def is_going_to_Search(self, event):
        text = event.message.text
        return text.lower() == "查詢"
    def is_going_to_Crypto(self, event):
        text = event.message.text
        return text.lower() == "虛擬貨幣"
    def is_going_to_Crypto_Fetch(self, event):
        text = event.message.text
        return True
    def is_going_to_Return_Crypto(self, event):
        return event.message.text.lower() == "繼續搜尋"
    def is_going_to_Return_Start(self, event):
        return event.message.text.lower() == "探索" or event.message.text.lower() == "離開"
    def is_going_to_Stock(self, event):
        text = event.message.text
        return text.lower() == "股票" or text.lower() == "繼續查詢"
    def is_going_to_Stock_US(self, event):
        text = event.message.text
        return text.lower() == "美股"
    def  is_going_to_Stock_US_Index(self,event):
        return event.message.text == "美股指數"
    def  is_going_to_Stock_US_Individual(self,event):
        return event.message.text == "美國個別股"
    def is_going_to_Stock_US_Index_four(self,event):
        text = event.message.text
        print(text)
        return text == 'GSPC' or text == 'IXIC' or text == 'NDX' or text == 'DJI'

    def is_going_to_Stock_US_Fetch(self,event):
        return True
    def is_going_to_Stock_TW(self, event):
        text = event.message.text
        return text.lower() == "台股"
    def is_going_to_Stock_TW_Fetch(self, event):
        if event.message.text != 'More':
            return True
        return False
    def is_going_to_Stock_TW_Fetch_2_End(self, event):
        return event.message.text.lower() == "離開"
    def is_going_to_TodayHigh(self, event):
        text = event.message.text
        return text.lower() == "平均線"

    def on_enter_Start(self, event):
        print("I'm entering Search")
        actions=[
            MessageTemplateAction(label='今日股市',text='查詢'),
            MessageTemplateAction(label='近期股市分析',text='股票分析')]
        send_button_message_NoneURL(
            reply_token = event.reply_token,
            title='請問需要甚麼服務',
            text='選擇功能',
            btn = actions,
            )
    def on_enter_Search(self, event):
        reply_token = event.reply_token
        actions=[
            MessageTemplateAction(label='Crypto',text='虛擬貨幣'),
            MessageTemplateAction(label='Stock',text='股票')]
        send_button_message_NoneURL(
            reply_token = event.reply_token,
            title='請選擇幣別',
            text='虛擬貨幣(Crypto Currency)\n股票(Stock)',
            btn = actions,)

    def on_enter_Crypto(self, event):
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template = ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/bVKzgFV.png',
                        action=MessageTemplateAction(label='BTC',text='BTC'),),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/UOqQuCW.png',
                        action=MessageTemplateAction(label='BAT',text='BAT'),),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/H54bizg.png',
                        action=MessageTemplateAction(label='ETH',text='ETH'),),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/qRIxXS7.png',
                        action=MessageTemplateAction(label='BNB',text='BNB'),),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/z2uYzbT.png',
                        action=MessageTemplateAction(label='BTC Cash',text='BCH'),),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/my1xVPD.png',
                        action=MessageTemplateAction(label='Dogecoin',text='DOGE'),),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/KHX1Rae.png',
                        action=MessageTemplateAction(label='SHIB',text='SHIB'),),
                    ]
                )
            )
        send_Multi_Image(reply_token = event.reply_token,message = message)
    def on_enter_Crypto_Fetch(self, event):
        datum = self.CRYPTO_STOCK.getJson(event.message.text)
        reply_token = event.reply_token
        send_Flex_message(event.reply_token,Flex_Message_Crypto(event.message.text, datum))

    def on_enter_Stock(self, event):
        reply_token = event.reply_token
        actions=[
            MessageTemplateAction(label='台灣股市',text='台股'),
            MessageTemplateAction(label='美國股市',text='美股')]
        send_button_message_NoneURL(
            reply_token = event.reply_token,
            title='請選擇',
            text='台灣股市/美國股市',
            btn = actions,)
    def on_enter_Stock_US(self, event):
        reply_token = event.reply_token
        actions=[
            MessageTemplateAction(label='美股指數',text='美股指數'),
            MessageTemplateAction(label='個別股票',text='美國個別股')]
        send_button_message_NoneURL(
            reply_token = event.reply_token,
            title='請問需要甚麼服務',
            text='選擇功能',
            btn = actions,
            )
    def on_enter_Stock_US_Index(self, event):
        message = json.load(open('Flex/US_Stock.json','r',encoding='utf-8'))
        send_Flex_message(event.reply_token,message)
    def on_enter_Stock_US_Individual(self,event):
        message = json.load(open('Flex/US_Stock_Individual.json','r',encoding='utf-8'))
        send_Flex_message(event.reply_token,message)


    def on_enter_Stock_US_Fetch(self, event):
        datum = self.US_STOCK.getJson(event.message.text)
        send_Flex_message(event.reply_token,TW_Stock_Each(url="https://i.imgur.com/RQMpQyo.png",datum=datum))

    def on_enter_Stock_US_Index_four(self,event):
        datum = self.US_STOCK.getJson(event.message.text)
        send_Flex_message(event.reply_token,TW_Stock_Each(url="https://i.imgur.com/RQMpQyo.png",datum=datum))
    def on_enter_Stock_TW(self, event):
        message = json.load(open('Flex/TW_Stock.json','r',encoding='utf-8'))
        send_Flex_message(event.reply_token,message)

    def on_enter_Stock_TW_Fetch(self,event):
        datum = self.TW_STOCK.getJson(event.message.text)
        send_Flex_message(event.reply_token,TW_Stock_Each(url="https://i.imgur.com/e7yvQGQ.png",datum=datum))


    def is_going_to_SMA(self,event):
        return event.message.text.lower() == "股票分析"

    def on_enter_SMA(self,event):
        message = json.load(open('Flex/TW_SAM.json','r',encoding='utf-8'))
        send_Flex_message(event.reply_token,message)

    def is_going_to_SMA_S(self,event):
        return event.message.text.lower() == "台股短線"

    def on_enter_SMA_S(self,event):
        message = json.load(open('Flex/TW_Stock.json','r',encoding='utf-8'))
        send_Flex_message(event.reply_token,message)

    def is_going_to_SMA_M(self,event):
        return event.message.text.lower() == "台股中線"
    def on_enter_SMA_M(self,event):
        message = json.load(open('Flex/TW_Stock.json','r',encoding='utf-8'))
        send_Flex_message(event.reply_token,message)

    def is_going_to_SMA_L(self,event):
        return  event.message.text.lower() == "台股長線"
    def on_enter_SMA_L(self,event):
        message = json.load(open('Flex/TW_Stock.json','r',encoding='utf-8'))
        send_Flex_message(event.reply_token,message)


    def is_going_to_SMA_S_US(self,event):
        return event.message.text.lower() == "美股短線"

    def on_enter_SMA_S_US(self,event):
        message = json.load(open('Flex/US_Stock_Individual.json','r',encoding='utf-8'))
        send_Flex_message(event.reply_token,message)

    def is_going_to_SMA_M_US(self,event):
        return event.message.text.lower() == "美股中線"
    def on_enter_SMA_M_US(self,event):
        message = json.load(open('Flex/US_Stock_Individual.json','r',encoding='utf-8'))
        send_Flex_message(event.reply_token,message)

    def is_going_to_SMA_L_US(self,event):
        return  event.message.text.lower() == "美股長線"
    def on_enter_SMA_L_US(self,event):
        message = json.load(open('Flex/US_Stock_Individual.json','r',encoding='utf-8'))
        send_Flex_message(event.reply_token,message)

    def is_going_to_S_Stock(self,event):
        if self.TW_STOCK.getJson(event.message.text)["當日最高"] == "-":
            return False
        self.sma = SMA(stock=event.message.text+".TW",stype="short",start=CountDay(60),end=CountDay(0))
        return True
    def on_enter_S_Stock(self,event):
        url = self.sma.upload_url()
        message = ImageSendMessage(original_content_url=url,preview_image_url=url)
        send_Multi_Image(event.reply_token,message)

    def is_going_to_M_Stock(self,event):
        if self.TW_STOCK.getJson(event.message.text)["當日最高"] == "-":
            return False
        self.sma = SMA(stock=event.message.text+".TW",stype="medium",start=CountDay(240),end=CountDay(0))
        return True
    def on_enter_M_Stock(self,event):
        url = self.sma.upload_url()
        message = ImageSendMessage(original_content_url=url,preview_image_url=url)
        send_Multi_Image(event.reply_token,message)
    def is_going_to_L_Stock(self,event):
        if self.TW_STOCK.getJson(event.message.text)["當日最高"] == "-":
            return False
        self.sma = SMA(stock=event.message.text+".TW",stype="long",start=CountDay(480),end=CountDay(0))
        return True
    def on_enter_L_Stock(self,event):
        url = self.sma.upload_url()
        message = ImageSendMessage(original_content_url=url,preview_image_url=url)
        send_Multi_Image(event.reply_token,message)


    def is_going_to_S_Stock_US(self,event):
        if self.US_STOCK.getJson(event.message.text)["當日最高"] == "-":
            return False
        self.sma = SMA(stock=event.message.text,stype="short",start=CountDay(60),end=CountDay(0))
        return True

    def on_enter_S_Stock_US(self,event):
        url = self.sma.upload_url()
        message = ImageSendMessage(original_content_url=url,preview_image_url=url)
        send_Multi_Image(event.reply_token,message)

    def is_going_to_M_Stock_US(self,event):
        if self.US_STOCK.getJson(event.message.text)["當日最高"] == "-":
            return False
        self.sma = SMA(stock=event.message.text,stype="medium",start=CountDay(240),end=CountDay(0))
        return True

    def on_enter_M_Stock_US(self,event):
        url = self.sma.upload_url()
        message = ImageSendMessage(original_content_url=url,preview_image_url=url)
        send_Multi_Image(event.reply_token,message)


    def is_going_to_L_Stock_US(self,event):
        if self.US_STOCK.getJson(event.message.text)["當日最高"] == "-":
            return False
        self.sma = SMA(stock=event.message.text,stype="long",start=CountDay(480),end=CountDay(0))
        return True

    def on_enter_L_Stock_US(self,event):
        url = self.sma.upload_url()
        message = ImageSendMessage(original_content_url=url,preview_image_url=url)
        send_Multi_Image(event.reply_token,message)

    def is_going_to_Restart_SMA(self,event):
        return event.message.text.lower() != "股票分析" and event.message.text.lower() != "進階"

#     def is_going_to_Stock_Analysis(self,event):
#         return event.message.text.lower() == "進階"
#
#     def on_enter_Stock_Analysis(self,event):
#         url = self.sma.upload_url()
#         message = ImageSendMessage(original_content_url=url,preview_image_url=url)
#         send_Multi_Image(event.reply_token,message)

