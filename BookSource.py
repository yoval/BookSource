# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 11:55:42 2022

@author: fuwen
"""

import requests,re
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
bookSourceUrl = 'https://www.bixiabook.com/'
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
#检测网站标题
def Title(bookSourceUrl):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'}
    try:
        resp = requests.get(bookSourceUrl,headers=headers,timeout=10)
        resp.encoding = resp.apparent_encoding 
        html = resp.text
        title = re.findall('<title>(.*?)</title>', html)[0]
    except:
        title = '未链接成功'
    with open('website.md','a',encoding='utf-8') as f:
        f.write('| %s    | %s    |\n'%(title,bookSourceUrl))
    return title
#Markdown初始化
def md():
    with open('website.md','a',encoding='utf-8') as f:
        f.write('| 标题    | 网址    |'+'\n'+' | ---- | ---- | '+'\n')
md()
#特殊字符
olds = ['Ⓢ',' ','②','🔸','①','③','⑮','④','⑧','⑨pp','⑪','📜','💰', '🌾', '💫', '💰', '🔞', '💡',  '🐳', '✐', '🧾' ,'📒' ,'☆' ,'🈲' ,'📖', '❎', '☘️','📗','📙',
        '🍩','🎉','🏷','🌸','🍅','🎊','👍','🎈','🔥','📚','📰','💜','📥','💗','🔰','👿']
news = ['' for i in olds]

url = 'https://fuwenyue.coding.net/p/yuedu/d/BookSource/git/raw/master/bookSource.json'
data = pd.read_json(url)
'''
YuanList = [
    'https://fuwenyue.coding.net/p/yuedu/d/BookSource/git/raw/master/bookSource.json',
    'https://shuyuan.mgz6.cc/shuyuan/424e79df768f2fb936e65bed1967b07f.json',
    'http://www.yckceo1.com/d/zUPa9',
    'http://www.yckceo1.com/d/Tq61A',
    'http://www.yckceo1.com/d/XctAY',
    'http://www.yckceo1.com/d/9Jdd8',
    'http://www.yckceo1.com/d/K7DJr',
    'http://www.yckceo1.com/d/u7kQh',
    'http://www.yckceo1.com/d/3GpXX',
    
    ]

yuan_df = pd.DataFrame()
for oneyuan in YuanList:
    yuan_df1= pd.read_json(oneyuan)
    yuan_df = pd.concat([yuan_df,yuan_df1])

data = yuan_df
del yuan_df
print('全部书源读取成功')
'''
rows = data.shape[0]
print('检测到%s条数据'%rows)
#源注释Comment
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

#删除搜索链接为空的源
for row in data.itertuples():
    searchUrl = row.searchUrl
    if type(searchUrl) == float:
        data.drop(row.Index, inplace=True)
#精简源
bookUrlPatternList = [] #书籍Url正则
exploreUrlList = [] #发现
loginUrlList = [] #登录
searchUrlList = [] #搜索
sourceCommentList = [] #备注
bookSourceGroupList = [] #书籍分组
bookSourceUrlList = []
for row in data.itertuples():
    bookSourceGroup = row.bookSourceGroup
    bookSourceUrl = row.bookSourceUrl
    bookUrlPattern = row.bookUrlPattern
    try:
        bookUrlPattern = bookUrlPattern.replace(bookSourceUrl,'')
    except:
        bookUrlPattern = ''
    bookUrlPatternList.append(bookUrlPattern)
    loginUrl = row.loginUrl
    try:
        loginUrl = loginUrl.replace(bookSourceUrl,'')
    except:
        loginUrl = ''
    loginUrlList.append(loginUrl)
    searchUrl = row.searchUrl
    if '<js>' in searchUrl:
        pass
    else:
        try:
            searchUrl = searchUrl.replace(bookSourceUrl,'')
        except:
            searchUrl = ''
    if 'https' in searchUrl:
        bookSourceGroup = '搜索可精简'
        bookSourceGroup = ''
    else:
        bookSourceGroup = ''
    bookSourceGroupList.append(bookSourceGroup)
    searchUrlList.append(searchUrl)
    exploreUrl = row.exploreUrl
    try:
        exploreUrl = exploreUrl.replace(bookSourceUrl,'')
    except:
        exploreUrl = ''
    exploreUrlList.append(exploreUrl)

data['bookUrlPattern'] = bookUrlPatternList
data['exploreUrl'] = exploreUrlList
data['searchUrl'] = searchUrlList
data['loginUrl'] = loginUrlList
data['bookSourceGroup'] = bookSourceGroupList
#删除源Url相同数值
bookSourceUrlList = []
for row in data.itertuples():
    bookSourceUrl = row.bookSourceUrl
    print(bookSourceUrl)
    if bookSourceUrl in bookSourceUrlList or bookSourceUrl.replace('http','https') in bookSourceUrlList or bookSourceUrl.replace('http','https') in bookSourceUrlList:
        data.drop(row.Index, inplace=True)
        print('重复值，删除')
    else:
        bookSourceUrlList.append(bookSourceUrl)
        try: #删除相应时间大于10秒
            resp = requests.get(bookSourceUrl,timeout=10)
        except:
            data.drop(row.Index, inplace=True)
            print('响应时间长，删除')
#保存
data.to_json('bookSource.json',orient='records',force_ascii=False,lines=False,indent=4)
#s = [Title(bookSourceUrl) for bookSourceUrl in data['bookSourceUrl']]
