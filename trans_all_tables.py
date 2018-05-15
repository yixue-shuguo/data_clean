# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 17:08:44 2018

@author: Administrator
"""

import pymysql 
import pandas as pd 

conn = pymysql.connect(host = 'rm-uf6w8oxsxgs5q8d2hrw.mysql.rds.aliyuncs.com', 
                       user = 'yixue_crm' ,
                       password = 'gToce0owVt7vhvaqpqplkwdf', 
                       db = 'xadmin_db',
                       charset='utf8')

cursor = conn.cursor()

conn_crm = pymysql.connect(host = '101.132.162.160', 
                           port = 3316,
                           user = 'online' ,
                           password = 'Hello2017', 
                           db = 'xadmin_db',
                           charset='utf8')

cursor_crm = conn_crm.cursor()

all_tables = ''' show tables '''

cursor_crm.execute(all_tables)

all_tables_list = cursor_crm.fetchall()

#for table in all_tables_list:
for table in (('t_app_user'),):
    print (table)
    sql = '''
            select * 
            from %s ''' %(table)
    data = pd.read_sql_query(sql ,conn_crm)
    