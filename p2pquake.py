import sys

sys.path.append('/Users/okazaki/.pyenv/versions/3.8.5/lib/python3.8/site-packages')


import datetime
import requests
import json
import schedule
from time import sleep
import chromedriver_binary
from selenium import webdriver
import time




# payload:検索条件
limit = 1
# 最大震度の下限。10(震度1)、20(震度2)、30(震度3)、40(震度4)、45(震度5弱)、50(震度5強)、55(震度6弱)、60(震度6強)、70(震度7)。
min_scale = 30


def earthquake_execute():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    print(now)
    seconds_ago = now - datetime.timedelta(seconds=30)
    base_time = seconds_ago.strftime('%Y/%m/%d %H:%M:%S')
    print(base_time)




    # 地震情報：概要抽出
    print(1)
    url = "https://api.p2pquake.net/v2/jma/quake"
    payload = {"limit":limit, "min_scale":min_scale}
    r = requests.get(url, params=payload)
    data = json.loads(r.text)
    print(2)

    # 地震情報：詳細抽出
    info_url = url + '/' + data[0]['id']
    print(3)
    info_r = requests.get(info_url)
    print(4)
    info_data = json.loads(info_r.text)
    print(5)
    # 地震発生時間
    quake_time = info_data['earthquake']['time']
    print(6)
    #quake_time = "2023/11/03 20:45:59"

    if quake_time>base_time:
        # 発生場所
        name = info_data['earthquake']['hypocenter']['name']
        #最大震度
        maxscale = info_data['earthquake']['maxScale']
        #マグニチュード
        magnitude = info_data['earthquake']['hypocenter']['magnitude']

        #quake_time="2022/04/25 19:13:00"


        # 震度判定
        if maxscale < 10:
            intensity = '１未満'
        elif maxscale < 11:
            intensity = '１'
        elif maxscale < 21:
            intensity = '２'
        elif maxscale < 31:
            intensity = '３'
        elif maxscale < 41:
            intensity = '４'
        elif maxscale < 46:
            intensity = '５弱'
        elif maxscale < 51:
            intensity = '５強'
        elif maxscale < 56:
            intensity = '６弱'
        elif maxscale < 61:
            intensity = '６強'
        elif maxscale < 71:
            intensity = '７'


        # （min_scale）以上に該当する都道府県を出力　
        region = []

        for i in info_data['points']:
            if i['scale'] >= min_scale:
                region.append(i['pref'])

        # 重複する都道府県を１つに処理
        region = list(dict.fromkeys(region))
        str_region = "\n".join(region)

        # def send_message():

    
        headers = {
            'Authorization': 'Bearer YourLineNotifyToken',
        }

        messagefile="緊急地震速報"+"======================="+"地震発生時間:\n"+str(quake_time)+"\n震源地:"+name+"\n予想最大震度 :"+intensity+"\nマグニチュード:"+str(magnitude)
        
        files = {
            'message': (None,messagefile)
            

        }

        requests.post('https://notify-api.line.me/api/notify', headers=headers, files=files)

        # def send_picture():
        driver = webdriver.Chrome()
        driver.get("http://www.kmoni.bosai.go.jp")
        time.sleep(1)
        driver.set_window_size(500,900)
        #driver.get("https://typhoon.yahoo.co.jp/weather/jp/earthquake/kyoshin/")
        driver.save_screenshot("aaa.png")
        #driver.save_screenshot("")
        headers = {
            'Authorization': 'Bearer YourLineNotifyToken',
        }

        image = 'aaa.png'
        files = {
            'message': (None, '震源地情報'),
            'imageFile': open(image, 'rb')
            #'stickerPackageId': 1, #ステッカーパッケージIDを入力 
            #'stickerId': 13, #ステッカーIDを入力 
        }

        requests.post('https://notify-api.line.me/api/notify', headers=headers, files=files)

    else:
        print("Nothing")

    # if quake_time>base_time:
    #     print("地震が発生しました")
    #     send_message()
    #     send_picture()
    # else:
    #     print("何もないよ")
    #     send_message()
    #     send_picture()


# earthquake_execute()

while True:
    earthquake_execute()

