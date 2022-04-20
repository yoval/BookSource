# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 20:37:02 2022

@author: fuwen
"""

import pandas as pd


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
for yuan in YuanList:
    yuan_df1= pd.read_json(yuan)
    yuan_df = pd.concat([yuan_df,yuan_df1])

bookUrlPatternList = [] #书籍Url正则
exploreUrlList = [] #发现
loginUrlList = [] #登录
searchUrlList = [] #搜索
sourceCommentList = [] #备注
bookSourceGroupList = [] #书籍分组
bookSourceUrlList = [] #书源 
for row in yuan_df.itertuples():
    bookSourceUrl = row.bookSourceUrl
    exploreUrl = row.exploreUrl
    loginUrl = row.loginUrl
    searchUrl = row.searchUrl
    bookUrlPattern = row.bookUrlPattern
    sourceComment = row.sourceComment
    pass