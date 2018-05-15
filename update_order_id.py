# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:48:54 2018

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

order_id_null ='''
select a.* , b.id 
from 
(
select a.accountid ,DATE_FORMAT(a.billing_date,'%Y%m%d') order_date,a.contract_amount  
from yejibiao a
where a.order_id is null 
and a.billing_date is not null 
and a.contract_amount is not null 
)a 
join 
(
select s.id s_id,t.id, t.income/100 income, FROM_UNIXTIME(t.add_time , '%Y%m%d') order_date
from xadmin_db.t_formal_student s 
left join xadmin_db.t_order t 
on t.student_id = s.id 
left join xadmin_db.t_order_detail d
on t.id = d.order_id 
where s.delete_time is null 
and t.delete_time is null 
and t.income >= 10000
and d.delete_time is null 
and d.course_id is not null 
)b 
on a.accountid = b.s_id
and a.order_date = b.order_date 
and a.contract_amount = b.income

'''


order_id_null ='''
select a.accountid ,FROM_UNIXTIME(a.order_date,'%Y%m%d') order_date,a.contract_amount,b.id
from 
(
select a.accountid ,unix_timestamp(a.billing_date) order_date,a.contract_amount  
from yejibiao a
where a.order_id is null 
and a.billing_date is not null 
and a.contract_amount is not null 
)a 
join 
(
select s.id s_id,t.id, t.income/100 income, t.add_time order_date
from xadmin_db.t_formal_student s 
left join xadmin_db.t_order t 
on t.student_id = s.id 
left join xadmin_db.t_order_detail d
on t.id = d.order_id 
where s.delete_time is null 
and t.delete_time is null 
and t.income >= 10000
and d.delete_time is null 
and d.course_id is not null 
)b 
on a.accountid = b.s_id
and a.contract_amount = b.income
and a.order_date BETWEEN b.order_date-259200 and b.order_date+259200


'''


order_id_null_result = pd.read_sql(order_id_null,conn)






for item in order_id_null_result.values:
#for item in ['陈启樾']:
    print (item)

    sql_update_st_id = '''
                      update yejibiao a
                      set order_id ='%s'
                      where accountid  = '%s'
                      and DATE_FORMAT(a.billing_date,'%%Y%%m%%d') = '%s'
                      and contract_amount = %s
                      
                      '''%(item[3],item[0],item[1],item[2])




    cursor.execute(sql_update_st_id)
    cursor.execute('commit')

   