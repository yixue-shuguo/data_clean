 # -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 12:41:17 2018

@author: Administrator
"""

import pymysql 
import pandas as pd 

conn = pymysql.connect(host = 'rm-uf6w8oxsxgs5q8d2hrw.mysql.rds.aliyuncs.com', 
                       user = 'yixue_crm' ,
                       password = 'gToce0owVt7vhvaqpqplkwdf', 
                       db = 'yixue_crm_db',
                       charset='utf8')

cursor = conn.cursor()

conn_crm = pymysql.connect(host = 'rm-uf63p0667k98h8trnyo.mysql.rds.aliyuncs.com', 
#                           port = 3316,
                           user = 'yixue_crm' ,
                           password = 'gToce0owVt7vhvaqpqplkwdf', 
                           db = 'xadmin_db',
                           charset='utf8')

cursor_crm = conn_crm.cursor()

sql_st_id_null ='''
select  DISTINCT st_name student_name
from yixue_crm_db.yejibiao 
where accountid is null 
or accountid = '' 
'''

st_id_null = pd.read_sql(sql_st_id_null,conn)





for item in st_id_null['student_name']:
#for item in ['陈启樾']:
    print (item)
    sql_find_id = '''
                select id
                from t_formal_student fs 
                where fs.sname ='%s'
                limit 1 
                '''%(item)
    
    cursor_crm.execute(sql_find_id)
    account_id_raw = cursor_crm.fetchall()
    if len(account_id_raw) != 0:
        account_id = account_id_raw[0][0]
        print (account_id)
    
        sql_update_st_id = '''
                      update yejibiao 
                      set accountid =%d
                      where st_name = '%s'
                      and(
                      accountid is null
                      or accountid = '' )
                      
                      '''%(account_id,item)


        cursor.execute(sql_update_st_id)
        cursor.execute('commit')
    else :
        pass
   