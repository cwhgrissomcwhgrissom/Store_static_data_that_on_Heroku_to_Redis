import requests , json , datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
import time

def movie():
    target_url = 'https://movies.yahoo.com.tw/'
    res = requests.get(target_url)
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.select('div.movielist_info h2 a')
    content = ""
    count = 0
    for i in data:
        if count < 8:
            title = i.text
            link =  i['href']
            content += '{}\n{}\n'.format(title, link)
            count = count + 1
    #print(content)
    return content

def nowtime():
    datetime_dt = datetime.datetime.today()# 獲得當地時間
    context = datetime_dt.strftime("%Y/%m/%d %H:%M:%S")  # 格式化日期
    return context


def get_stocknum(datastr):
    msg = datastr
    msg2 = []
    num = len(msg)
    for n in range(0, num):
        if msg[n] == '@':
            for n1 in range(1,num):
                msg2.append(msg[n1])  
    msg2 = ''.join(msg2)
    msg2 = str(msg2)
    return msg2

def meizitu():

    pagenums = 5 # 用來決定爬的頁數
    pageflag = 0
    pic_url = []
    while(1):
        if pageflag == 0:
            base_url = 'https://www.2717.com/tag/320.html'
            r = requests.get(base_url)
            soup = BeautifulSoup(r.content,'lxml')
            #print(soup)
            soup = soup.find_all('img')
            #print(soup)
            for n in soup:
                n = n['src']
                pic_url.append(n)
                #print(n)
            pageflag = 1
            #break
            #pass
        else:
            #print('[debug msg]_Im here~~~!!')
            for pagenum in range(2,pagenums):
                base_url = 'https://www.2717.com/tag/320_'+ str(pagenum) +'.html'
                #print(base_url)
                r = requests.get(base_url)
                soup = BeautifulSoup(r.content,'lxml')
                #print(soup)
                soup = soup.find_all('img')
                #print(soup)
                for n in soup:
                    n = n['src']
                    pic_url.append(n)
                    #print(n)
            #print('------------------------------------------------------------------------------------')
            #print(pic_url)
            break
    pic_url = random.choice(pic_url)        
    return pic_url