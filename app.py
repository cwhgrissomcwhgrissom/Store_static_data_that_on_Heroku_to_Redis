
from flask import Flask,request,g
import module, random, linecache, json, datetime, time, os, redis
from flask_redis import FlaskRedis
from bs4 import BeautifulSoup
import pandas as pd
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app=Flask(__name__)

# redis資料庫連線
app.config['SESSION_REDIS'] = redis.Redis(host='redis-14274.c10.us-east-1-4.ec2.cloud.redislabs.com', port='14274', password='PCisrKZmMk7o7HTpsHBJM4mTAithO3LS')
# app.config['SESSION_REDIS'] = 'redis://:PCisrKZmMk7o7HTpsHBJM4mTAithO3LS@redis-14274.c10.us-east-1-4.ec2.cloud.redislabs.com:14274/1'

# 設定Redis的對象, 以便調用方法
redis_client = app.config['SESSION_REDIS']

# Line-bot的連接資訊
line_bot_api=LineBotApi('NbZxPNw17qV6p/aKwntgf8O26U4PTZVGWWuZ8aJkwruEhMynK7QamR+H5C4BOUJK1RV8HEzQob66m+vH+erdBAyivV4imkGU9dQzgCpase2amWlI4AQOZNACarJzCR31abnoJ9i6TUJ58fm9N6obAwdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('e781f715dc7c8311d81a2bb1269c4022')

# 增加全局变量g.stk_num
@app.before_request
def before_request():
    g.stk_num = ""

@app.route("/callback",methods=['GET','POST'])
def callback():
    signature=request.headers['X-Line-Signature']
    body=request.get_data(as_text=True)
    app.logger.info("Request body: "+body)
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    if '@' in event.message.text:
            # store data in global variables
            g.stk_num = module.get_stocknum(event.message.text)
            # store data in Redis
            redis_client.set('words', g.stk_num)
            print('***debug msg[Is the data in global variables?:]--------------------------------------------:'+g.stk_num)
            print('***debug msg[Is the data in Redis?:]--------------------------------------------:'+str(redis_client.get('words')))
    elif 'p' in event.message.text:
        # When event.message.text is not '@', print out g.stk_num to see if the data is missing
        stk_num_print()
    else: pass

# Define print function
def stk_num_print():
    for i in range(0,3):
        print('***debug msg[Checking. print global variables, s.stk_num:]--------------------------------------------:'+g.stk_num)
        print("***debug msg[Checking. print Redis, redis_client.get('words'):]--------------------------------------------:"+str(redis_client.get('words')))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)