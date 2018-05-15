# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 13:36:45 2018

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
select distinct y.channel
from yixue_crm_db.mkt_leads y 
where 1=1
# and DATE_FORMAT(y.billing_date,'%Y') = 2018
and 
(
y.id is null 
or y.id =''
)
'''

channel_null = pd.read_sql(sql_channel_null,conn)





for item in channel_null['channel']:
#for item in ['陈启樾']:
    print (item)
    sql_find_id = '''
                     select 
                     fs.id
                     from t_sys_channel fs 
                     where fs.cn_name = '%s'
                     limit 1  
                '''%(item)
    
    cursor_crm.execute(sql_find_id)
    account_id_raw = cursor_crm.fetchall()
    print (account_id_raw)
    
    
    if len(account_id_raw) != 0:
        account_id = account_id_raw[0][0]
        print (account_id)
    
        sql_update_st_id = '''
                      update yixue_crm_db.mkt_leads
                      set id ='%s'
                      where channel  = '%s'
                      
                      '''%(account_id,item)


        cursor.execute(sql_update_st_id)
        cursor.execute('commit')
    else :
        pass
   