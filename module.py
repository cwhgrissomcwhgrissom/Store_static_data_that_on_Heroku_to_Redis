import requests , json , datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
import time

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
