# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 15:59:47 2018

@author: Administrator
"""

import pymysql 
import yagmail 
import pandas as pd 
import datetime

conn = pymysql.connect(host = 'rm-uf6w8oxsxgs5q8d2hrw.mysql.rds.aliyuncs.com', 
                       user = 'yixue_crm' ,
                       password = 'gToce0owVt7vhvaqpqplkwdf', 
                       db = 'yixue_crm_db',
                       charset='utf8')

cursor = conn.cursor()

mkt_sql = '''
select 
channel_id '渠道ID',
tsc.cn_name '渠道名称',
sum(leads) '导入leads',
sum(appoit_num)  '预约' ,
sum(attend_num )  '出席' ,
concat(round(sum(attend_num)*100/sum(appoit_num),0),'%') '出席率', 
sum(order_num) '转化',
sum(order_amount) '金额'
from 
(
select 
id AS channel_id,
sum(leads) as leads,
0 as appoit_num,
0 as attend_num,
0 AS order_num ,
0 AS order_amount
from yixue_crm_db.mkt_leads WHERE
DATE_FORMAT(`upload date` ,'%Y%m')= '201803'
 group by id,channel

union all
SELECT
tf.channel_id as channel_id,
  0 as leads,
	count(distinct s.id) appoit_num,
	sum(if(s.student_attendance_status = 'yes' ,1,0)) attend_num,
	0 AS order_num ,
	0 AS order_amount
FROM
xadmin_db.t_course_lesson AS s 
left join xadmin_db.t_student tf
on s.student_id = tf.id
WHERE
	s.ctype = 'audition'
AND s.delete_time IS NULL
and	FROM_UNIXTIME(s.start_time,'%Y%m')  = '201803'
GROUP BY
tf.channel_id

	union all
SELECT
p.channel_id as channel_id,
	0 as leads,
	0 as appoit_num,
	0 as attend_num,
	count( distinct IF ( p.payment_types = '新生', accountid, NULL ) ) AS order_num,
	sum( IF ( p.payment_types = '新生' , p.contract_amount, 0 ) ) AS order_amount
FROM
	yixue_crm_db.yejibiao AS p 
WHERE
	DATE_FORMAT(billing_date,'%Y%m' )= '201803'
GROUP BY
p.channel_id
	)r
left join xadmin_db.t_sys_channel tsc
on r.channel_id = tsc.id
group by r.channel_id
order by sum(order_amount) desc
'''
now = datetime.datetime.now().strftime("%Y%m%d %H%M%S") 
mkt_info = pd.read_sql(mkt_sql,conn)
file = 'MTK_info_%s.xlsx'%(now)
mkt_info.to_excel(file,index = False)


#链接邮箱服务器
yag = yagmail.SMTP( user="shujubu@171xue.com", password="yixue123", host='mail.171xue.com')

# 邮箱正文
contents = ['MKT渠道信息,更新日期 %s'%(now)]

# 发送邮件
#yag.send('cici.cai@171xue.com', 'MKT渠道信息', contents,[file])

yag.send('mashuguo@171xue.com', 'MKT渠道信息', contents,[file])



