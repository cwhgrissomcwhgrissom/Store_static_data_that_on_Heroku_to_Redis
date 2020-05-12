# Heroku儲存靜態變數的方法: Flask+Redis+Heroku+line-bot
申請Redis帳號, 免費帳後有30M的空間可以使用, 然後建立一個database</BR>
app.py:
```
# redis資料庫連線
app.config['SESSION_REDIS'] = redis.Redis(host='host', port='6397', password='password')
# app.config['SESSION_REDIS'] = 'redis://:password@host:port/db'
# 設定Redis的對象, 以便調用方法
redis_client = app.config['SESSION_REDIS']
```
同始將變數存入全域變數 `g.stk_num` and `Redis` `redis_client.set('words', g.stk_num)`, 
然後再將其印出來確認所儲存得資料是否存在?
由列印結果可以發現 `g.stk_num`在dyno結束後就被清掉了, 而Redis的內容並不會因為dyno結束而被清掉
