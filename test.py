import requests
import time
import telegram

bot = telegram.Bot(token='1291913473:AAF1cPee5-ipb0YPgLFQLo07eelSW2I29-Y')

url = "https://api.upbit.com/v1/market/all"

querystring = {"isDetails":"false"}

response = requests.request("GET", url, params=querystring)

res_json = response.json()

coin_name = []
coin_list = []
coin_old_price = []
coin_new_price = []

for i in res_json:
    coinlist_str = i["market"]
    coinName_str = i["korean_name"]
    coinlist_str = str(coinlist_str)
    coinName_str = str(coinName_str)

    if "KRW" in coinlist_str:
        coin_list.append(coinlist_str)
        coin_name.append(i['korean_name'])

for i in res_json:
    coin_name.append(i['korean_name'])    

url = "https://api.upbit.com/v1/trades/ticks"

for i in coin_list:
    querystring = {"market":i,"count":"1"}
    each_coin_price = requests.request("GET", url, params=querystring)
    each_coin_price_json = each_coin_price.json()
    # print(each_coin_price_json)
    coin_old_price.append(each_coin_price_json[0]['trade_price'])

while(1):
    start = time.time()
    for i in coin_list:
        querystring = {"market":i,"count":"1"}
        each_coin_price = requests.request("GET", url, params=querystring)
        coin_new_price_json = each_coin_price.json()
        # print(coin_new_price_json)
        coin_new_price.append(coin_new_price_json[0]["trade_price"])

    for i in range(0,len(coin_old_price)):
        if coin_new_price[i] >= coin_old_price[i] * 1.05:
            text_str = str(coin_name[i]) + " is growing Up!!"
            bot.send_message(chat_id=1244447272, text=text_str)

    coin_old_price = coin_new_price
    coin_new_price = []
    print("Excute time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간