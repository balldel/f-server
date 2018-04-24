from flask import Flask, request, abort
from linebot import (
LineBotApi, WebhookHandler
)
from linebot.exceptions import (
InvalidSignatureError
)
from linebot.models import (
MessageEvent, TextMessage, TextSendMessage,
)

import requests 

app = Flask(__name__)
line_bot_api = LineBotApi('fSDjokoamI2lnlDZE8GJ2+PoZBn8DHsDba8zCtW57zR++3X+Iiy5jwtMQFB1oynrcHd3pU4g5S3IikMXzTmCkPueLieW/ilvst42POA6I6cyt/+z3u13OPxjof+Jq12l046ITxA2+sSMC95uRwEdHQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a3e92910d347b8dcda29a8bfaba8e3bc')

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
        r = requests.get('http://52.76.34.87:8000/skyscanner/api/country/?country='+countrycode)
        print(r.text)
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
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.type))

if __name__ == "__main__":
    app.run()