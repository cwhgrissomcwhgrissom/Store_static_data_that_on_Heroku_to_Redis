# Heroku儲存靜態變數的方法: Flask+Redis+Heroku+line-bot
1. 申請Redis帳號, 免費帳後有30M的空間可以使用, 然後建立一個database</BR>, 用來儲存Heroku會用到的資料
2. app.py: 加入連線到Redis的程式碼
```
# redis資料庫連線資訊配置到Flask
app.config['SESSION_REDIS'] = redis.Redis(host='host', port='6397', password='password')
# 設定Redis的對象, 以便調用方法
redis_client = app.config['SESSION_REDIS']
```
3. 當在line-bot輸入"@", 將資料 `9527` 存入全域變數 `g.stk_num` and `Redis` `redis_client.set('words', g.stk_num)`
4. 再次於line-bot輸入"p", 將資料印出來, 確認所儲存得資料是否存在?
5. 由Heroku logs結果可以發現 `g.stk_num`在dyno結束後就被清掉了, 而Redis的內容並不會因為dyno結束而被清掉
