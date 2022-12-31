# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 01:43:18 2023

@author: Administrator
"""
from tld import get_tld
import requests
import pandas as pd

url = 'https://shuyuan.mgz6.cc/shuyuan/b6e606af3c02f364aeeb594d99fd580d.json'


def ChangebookSourceUrl(bookSourceUrl):
    if bookSourceUrl == '':
        bookSourceUrl=''
    elif bookSourceUrl[-1] == '/':
        try:
            res = get_tld(bookSourceUrl, as_object=True)
            bookSourceUrl = res.parsed_url.scheme + '://' + res.parsed_url.netloc
        except:
            bookSourceUrl = ''
    else:
        bookSourceUrl = ''
    bookSourceUrl = bookSourceUrl.split('#')[0]
    bookSourceUrl = bookSourceUrl.split('-By')[0]
    if 'http' not in bookSourceUrl:
        bookSourceUrl = 'http://' + bookSourceUrl
    if 'https' not in bookSourceUrl:
        bookSourceUrl = bookSourceUrl.replace('http','https')
    return bookSourceUrl

def CheckbookSourceUrl(bookSourceUrl):
    try:
        requests.get(bookSourceUrl)
    except:
        bookSourceUrl=''
    return bookSourceUrl



data = pd.read_json(url)
rows = data.shape[0]
print('共检测到%s条数据'%rows)
#按书源链接排序
data['bookSourceUrl'] = data['bookSourceUrl'].map(ChangebookSourceUrl)
#data['bookSourceUrl'] = data['bookSourceUrl'].map(CheckbookSourceUrl)
data.sort_values(by='bookSourceUrl',ascending=True,inplace = True)
data.drop_duplicates(subset=['bookSourceUrl'],keep='first',inplace=True)
data['bookSourceComment'] = ''
data.to_json('myBookSource.json',orient='records',force_ascii=False,lines=False,indent=4)


