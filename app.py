from flask import Flask, request, abort
from multiprocessing.dummy import Pool
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests 

app = Flask(__name__)
line_bot_api = LineBotApi('fSDjokoamI2lnlDZE8GJ2+PoZBn8DHsDba8zCtW57zR++3X+Iiy5jwtMQFB1oynrcHd3pU4g5S3IikMXzTmCkPueLieW/ilvst42POA6I6cyt/+z3u13OPxjof+Jq12l046ITxA2+sSMC95uRwEdHQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a3e92910d347b8dcda29a8bfaba8e3bc')
pools = Pool(2)

@app.route("/bot", methods=['POST'])
def bot():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    data = request.json
    print(data)
    print("USERID :"+ data['events'][0]['source']['userId'])
    print("Massage :"+ data['events'][0]['message']['text'])
    app.logger.info("Request body: " + body)
    
    massage = data['events'][0]['message']['text']
    if 'scan>' in massage:
        countrycode = massage.split('>')[1]
        print(countrycode)
        pools.apply_async(requests.get, ['http://13.251.22.242:8000/skyscanner/api/country/?country='+countrycode ])
        # r = requests.get('http://13.251.49.123:8000/skyscanner/api/country/?country='+countrycode)
        print("SENT")
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route("/warakorn", methods=['GET'])
def warakorn():

    countrycode ='it'
   
    print(countrycode)
    r = requests.get('http://127.0.0.1:8000/skyscanner/api/country/?country='+countrycode)
    print(r.text)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="ได้รับข้อมูลแล้วครับ ผมจะรีบหาข้อมูลแล้วส่งกลับไปครับ"))

if __name__ == "__main__":
    app.run()