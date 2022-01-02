import json
def Flex_Message_Crypto(Crypto, datum):
    message = json.load(open('Flex/Crypto.json','r',encoding='utf-8'))
    if Crypto == 'BTC':
        message['hero']['url'] = 'https://i.imgur.com/bVKzgFV.png'
        message['hero']['action']['uri'] = 'https://www.coinbase.com/price/bitcoin'
        message['body']['contents'][0]['text'] = "BitCoin(BTC)"
        message['body']['contents'][1]['contents'][0]['contents'][1]['text'] = datum['USDC']
        message['body']['contents'][1]['contents'][1]['contents'][1]['text'] = datum['TWD']
    elif Crypto == 'BAT':
        message['hero']['url'] = 'https://i.imgur.com/UOqQuCW.png'
        message['hero']['action']['uri'] = 'https://www.coinbase.com/price/basic-attention-token'
        message['body']['contents'][0]['text'] = "Basic Attention Token"
        message['body']['contents'][1]['contents'][0]['contents'][1]['text'] = datum['USDC']
        message['body']['contents'][1]['contents'][1]['contents'][1]['text'] = datum['TWD']
    elif Crypto == 'ETH':
        message['hero']['url'] = 'https://i.imgur.com/H54bizg.png'
        message['hero']['action']['uri'] = 'https://www.coinbase.com/price/ethereum'
        message['body']['contents'][0]['text'] = "Ethereum(ETH)"
        message['body']['contents'][1]['contents'][0]['contents'][1]['text'] = datum['USDC']
        message['body']['contents'][1]['contents'][1]['contents'][1]['text'] = datum['TWD']
    elif Crypto == 'BNB':
        message['hero']['url'] = 'https://i.imgur.com/qRIxXS7.png'
        message['hero']['action']['uri'] = 'https://www.coinbase.com/price/binance-coin'
        message['body']['contents'][0]['text'] = "Binance Coin(BNB)"
        message['body']['contents'][1]['contents'][0]['contents'][1]['text'] = datum['USDC']
        message['body']['contents'][1]['contents'][1]['contents'][1]['text'] = datum['TWD']
    elif Crypto == 'BCH':
        message['hero']['url'] = 'https://i.imgur.com/z2uYzbT.png'
        message['hero']['action']['uri'] = 'https://www.coinbase.com/price/bitcoin-cash'
        message['body']['contents'][0]['text'] = "Bitcoin Cash(BCH)"
        message['body']['contents'][1]['contents'][0]['contents'][1]['text'] = datum['USDC']
        message['body']['contents'][1]['contents'][1]['contents'][1]['text'] = datum['TWD']
    elif Crypto == 'DOGE':
        message['hero']['url'] = 'https://i.imgur.com/my1xVPD.png'
        message['hero']['action']['uri'] = 'https://www.coinbase.com/price/dogecoin'
        message['body']['contents'][0]['text'] = "Dogecoin(DOGE)"
        message['body']['contents'][1]['contents'][0]['contents'][1]['text'] = datum['USDC']
        message['body']['contents'][1]['contents'][1]['contents'][1]['text'] = datum['TWD']
    elif Crypto == 'SHIB':
        message['hero']['url'] = 'https://i.imgur.com/KHX1Rae.png'
        message['hero']['action']['uri'] = 'https://www.coinbase.com/price/shiba-inu'
        message['body']['contents'][0]['text'] = "SHIBA INU(SHIB)"
        message['body']['contents'][1]['contents'][0]['contents'][1]['text'] = datum['USDC']
        message['body']['contents'][1]['contents'][1]['contents'][1]['text'] = datum['TWD']
    return message

def TW_Stock_Each(url,datum):
    message = json.load(open('Flex/TW_Stock_each.json','r',encoding='utf-8'))
    message['hero']['url'] = url
    message['body']['contents'][0]['text'] = datum['name']
    message['body']['contents'][1]['text'] = str(round(float(datum['昨日收盤價']),4))
    if not datum["name"] == "網路逾時，請重新查找":
        count = float(datum['當下價格']) - float(datum['昨日收盤價'])
        count = round(count,3)
        if count < 0:
            message['body']['contents'][2]['color'] = '#008000'
            message['body']['contents'][2]['text'] = str(count)
        elif count > 0:
            message['body']['contents'][2]['color'] = '#f00000'
            message['body']['contents'][2]['text'] = "+" + str(count)
        else:
            message['body']['contents'][2]['color'] = '#808080'
            message['body']['contents'][2]['text'] = "+" + str(count)
        count = round((count / float(datum['昨日收盤價'])*100),2)
        message['body']['contents'][2]['text'] =  message['body']['contents'][2]['text'] + " (" + str(abs(count)) + "%)"
    else:
        message['body']['contents'][2]['color'] = '#808080'
        message['body']['contents'][2]['text'] = '-'
    message['body']['contents'][3]['contents'][0]['contents'][1]['text'] = str(round(float(datum['開盤']),4))
    message['body']['contents'][3]['contents'][1]['contents'][1]['text'] = str(round(float(datum['當日最低']),4))
    message['body']['contents'][3]['contents'][2]['contents'][1]['text'] = str(round(float(datum['當日最高']),4))
    message['body']['contents'][3]['contents'][3]['contents'][1]['text'] = str(round(float(datum['昨日收盤價']),4))
    return message