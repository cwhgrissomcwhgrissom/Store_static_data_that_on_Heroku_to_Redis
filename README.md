"# Heroku儲存變數的方法: Flask+Redis+Heroku+line-bot" 
同始將變數存入全域變數 `g.stk_num` and `Redis` `redis_client.set('words', g.stk_num)`, 
然後再將其印出來確認所儲存得資料是否存在
由列印結果可以發現 `g.stk_num`在dyno結束後就被清掉了, 而Redis的內容並不會因為dyno結束而被清掉
