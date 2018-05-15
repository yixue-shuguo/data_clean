# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:58:14 2018

@author: Administrator
"""

import pymysql 
import pandas as pd 

conn = pymysql.connect(host = 'rm-uf6w8oxsxgs5q8d2ho.mysql.rds.aliyuncs.com', 
                       user = 'yixue_crm' ,
                       password = 'Hello@2017', 
                       db = 'yixue_crm_db',
                       charset='utf8')


phone_sql  = 'select id from t1'
cursor = conn.cursor()
phone  = pd.read_sql(phone_sql,conn)

L = []

for item in phone :
    shiting = '''
    select 