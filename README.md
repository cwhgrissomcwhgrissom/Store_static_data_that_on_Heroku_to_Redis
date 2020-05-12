# Heroku儲存靜態變數的方法: Flask+Redis+Heroku+line-bot
1. 申請Redis帳號, 免費帳後有30M的空間可以使用, 然後建立一個database</BR>
2. app.py:
```
# redis資料庫連線
app.config['SESSION_REDIS'] = redis.Redis(host='host', port='6397', password='password')
# 設定Redis的對象, 以便調用方法
redis_client = app.config['SESSION_REDIS']
```
3. 資料 `9527` 存入全域變數 `g.stk_num` and `Redis` `redis_client.set('words', g.stk_num)`
```
if '@' in event.message.text:
            # store data in global variables
            g.stk_num = module.get_stocknum(event.message.text)
            # store data in Redis
            redis_client.set('words', g.stk_num)
            print('***debug msg[Is the data in global variables?:]--------------------:'+g.stk_num)
            print('***debug msg[Is the data in Redis?:]--------------------:'+str(redis_client.get('words')))
```
4. 然後再將其印出來確認所儲存得資料是否存在?
```
def stk_num_print():
    for i in range(0,3):
        print('***debug msg[Checking. print global variables, s.stk_num:]--------------------:'+g.stk_num)
        print("***debug msg[Checking. print Redis, redis_client.get('words'):]--------------------:"+str(redis_client.get('words')))
```
5. 由Heroku logs結果可以發現 `g.stk_num`在dyno結束後就被清掉了, 而Redis的內容並不會因為dyno結束而被清掉
```
2020-05-12T06:33:53.362201+00:00 app[web.1]: ***debug msg[Is the data in global variables?:]---------------------:9527
2020-05-12T06:33:53.363186+00:00 app[web.1]: ***debug msg[Is the data in Redis?:]---------------------:b'9527'
2020-05-12T06:33:53.365420+00:00 app[web.1]: 10.113.192.240 - - [12/May/2020:14:33:53 +0800] "POST /callback HTTP/1.1" 200 2 "-" "LineBotWebhook/1.0"
2020-05-12T06:33:53.370531+00:00 heroku[router]: at=info method=POST path="/callback" host=gspace.herokuapp.com request_id=4490fb5a-1f1c-4eec-94ff-20fab045b88e fwd="147.92.150.194" dyno=web.1 connect=0ms service=89ms status=200 bytes=161 protocol=https
2020-05-12T06:33:58.642992+00:00 app[web.1]: ***debug msg[Checking. print global variables, s.stk_num:]---------------------:
2020-05-12T06:33:58.747110+00:00 app[web.1]: ***debug msg[Checking. print Redis, redis_client.get('words'):]-------------------:b'9527'
2020-05-12T06:33:58.747225+00:00 app[web.1]: ***debug msg[Checking. print global variables, s.stk_num:]---------------------:
2020-05-12T06:33:58.749831+00:00 app[web.1]: ***debug msg[Checking. print Redis, redis_client.get('words'):]-------------------:b'9527'
2020-05-12T06:33:58.749915+00:00 app[web.1]: ***debug msg[Checking. print global variables, s.stk_num:]---------------------:
2020-05-12T06:33:58.774237+00:00 app[web.1]: ***debug msg[Checking. print Redis, redis_client.get('words'):]-------------------:b'9527'
2020-05-12T06:33:58.776288+00:00 app[web.1]: 10.69.244.94 - - [12/May/2020:14:33:58 +0800] "POST /callback HTTP/1.1" 200 2 "-" "LineBotWebhook/1.0"
2020-05-12T06:33:58.776369+00:00 heroku[router]: at=info method=POST path="/callback" host=gspace.herokuapp.com request_id=ab7d1a08-7d33-4d84-bfa2-a36510196c09 fwd="147.92.150.194" dyno=web.1 connect=1ms service=140ms status=200 bytes=161 protocol=https
```
