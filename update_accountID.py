# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 12:41:17 2018

@author: Administrator
"""

import pymysql 
import pandas as pd 

conn = pymysql.connect(host = 'rm-uf6w8oxsxgs5q8d2ho.mysql.rds.aliyuncs.com', 
                       user = 'yixue_crm' ,
                       password = 'Hello@2017', 
                       db = 'ecustomer',
                       charset='utf8')

cursor = conn.cursor()

sql_st_id_null ='''
select  DISTINCT `student name` student_name
from yixue_crm_db.yejibiao 
where accountid is null 
'''

st_id_null = pd.read_sql(sql_st_id_null,conn)


for item in st_id_null['student_name']:
#for item in ['唐安妮']:
    sql_find_st_id = '''select a.accountid
                     from ecustomer.ec_account a
                     where a.accountname = '%s'
                 '''%(item)
    cursor.execute(sql_find_st_id)
    st_id = cursor.fetchone()
    if st_id is not None :
#        print (st_id[0])
        sql_update_st_id = '''
                            update  yixue_crm_db.yejibiao
                            set accountid = '%d'
                            where `student name` = '%s'
                            '''%(st_id[0] , item)

        try:
            cursor.execute(sql_update_st_id)
        except Exception as e :
            pass
        print (st_id[0] , item)