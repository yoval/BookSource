# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 11:55:42 2022

@author: fuwen
"""

#import requests,json
import pandas as pd


def replaceFomat(text: str, word: str, n: int,reverse=False):
    '''对文本中的指定单词进行格式化的替换/替回
    Params:
    ---
    text
        要替换的文本
    word
        目标单词
    n
        目标单词的序号
    reverse
        是否进行替回
    Return:
    ---
    new_text
        替换后的文本
    '''
    # 构造【中间变量】
    new_text = text[ : ]
    fmt = "<{}>".format(n)
    # 替换
    if reverse is False:
        new_text = new_text.replace(word, fmt)  # 格式化替换
        return new_text
    # 替回
    elif reverse is True:
        new_text = new_text.replace(fmt, word)  # 去格式化替换
        return new_text
    # 要求非法，引发异常
    else:
        raise TypeError
def replaceMulti(text: str, olds: list, news: list):
    '''一次替换多组字符串
    Params:
    ---
    text
        要替换的文本
    olds
        旧字符串列表
    news
        新字符串列表
    Return:
    ---
    new_text: str
        替换后的文本
    '''
    if len(olds) != len(news):
        raise IndexError
    else:
        new_text = text[ : ]
        # 格式化替换
        i = 0  # 单词计数器
        for word in olds:
            i += 1
            new_text = replaceFomat(new_text, word, i)
        # 去格式化替回
        i = 0  # 归零
        for word in news:
            i += 1
            new_text = replaceFomat(new_text, word, i,True)
        # 返回替换好的文本
        return new_text
#源Url
bookSourceUrl = 'https://shuyuan.mgz6.cc/'
def yuan(bookSourceUrl):
    if bookSourceUrl[-1]=='/':
        bookSourceUrl=bookSourceUrl[:-1]
    if bookSourceUrl[-1]=='/':
        bookSourceUrl=bookSourceUrl[:-1]
    return bookSourceUrl
#网站名称
bookSourceName = '飞卢小说(分类最全)'
def Name(bookSourceName):
    bookSourceName = bookSourceName.split('(')[0] 
    bookSourceName = bookSourceName.split('（')[0] 
    return bookSourceName
    
#特殊字符
olds = ['Ⓢ',' ','②','🔸','①','③','⑮','④','⑧','⑨','⑪','📜','💰', '🌾', '💫', '💰', '🔞', '💡',  '🐳', '✐', '🧾' ,'📒' ,'☆' ,'🈲' ,'📖', '❎', '☘️','📗','📙',
        '🍩','🎉','🏷','🌸','🍅','🎊','👍','🎈','🔥','📚','📰','💜','📥','💗','🔰','👿']
news = ['' for i in olds]

url = 'https://shuyuan.mgz6.cc/shuyuan/a3231337446afe1ea5179b02737a8980.json'
data = pd.read_json(url)
#删除 源注释Comment
data['bookSourceComment'] = ''
#删除bookSourceUrl 签名
data['bookSourceUrl'] =[ i.split('#')[0] for i in data['bookSourceUrl']]
#书源名替换
data['bookSourceName'] = [replaceMulti(i, olds, news) for i in data['bookSourceName'] ]
data['bookSourceName'] = [Name(i) for i in data['bookSourceName']]
#修改分组
bookSourceList = []
for bookSource in data['bookSourceGroup'] :
    if bookSource =='':
        bookSource = '一般书源'
    bookSourceList.append(bookSource)
data['bookSourceGroup']  = bookSourceList
#源URL
data['bookSourceUrl'] =[yuan(i) for i in data['bookSourceUrl']]
#删除源Url相同数值
data = data.drop_duplicates('bookSourceUrl',keep='first')
#源Url重新排序
data.sort_values("bookSourceName",inplace=True)
#保存
data.to_json('bookSource.json',orient='records',force_ascii=False,lines=False,indent=4)


