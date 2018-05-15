# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 18:38:08 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:21:11 2018

@author: Administrator
"""

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

sql_channel_null ='''
select DISTINCT  y.accountid 
from yixue_crm_db.yejibiao y 
where 1=1
# and DATE_FORMAT(y.billing_date,'%Y') = 2018
and 
(
y.cellphone is null 
or y.cellphone = ''
)
'''

channel_null = pd.read_sql(sql_channel_null,conn)



for item in channel_null['accountid']:
#for item in ['陈启樾']:
    print (item)
    sql_find_id = '''
                     select 
                     fs.cellphone
                     from t_formal_student fs 
                     where fs.id = '%s'
                     limit 1  
                '''%(item)
    
    cursor_crm.execute(sql_find_id)
    account_id_raw = cursor_crm.fetchall()
    print (account_id_raw)
    
    
    if len(account_id_raw) != 0:
        account_id = account_id_raw[0][0]
        print (account_id)
    
        sql_update_st_id = '''
                      update yejibiao 
                      set cellphone ='%s'
                      where accountid  = '%s'
                      
                      '''%(account_id,item)


        cursor.execute(sql_update_st_id)
        cursor.execute('commit')
    else :
        pass
   