#!/usr/bin/env python
import sys
from datetime import datetime
import requests
import logging

logging.basicConfig(level=logging.DEBUG, filename='/tmp/zabbix_bearychat.log', mode='a')
to = sys.argv[1]
subject = sys.argv[2]
message = sys.argv[3]
logging.info(subject)
url = "https://hook.bearychat.com/=bw70H/incoming/{}".format(to)

subject_list = subject.split('=')
alert_type = subject_list[0]
title = subject_list[1]

if 'Resolved' == alert_type:
    emoji = ':heavy_check_mark: '
    color = '#00ff00'
    start_time = subject_list[2]
    end_time = subject_list[3]
    duration_time = datetime.strptime(end_time, '%Y.%m.%d %H:%M:%S') - datetime.strptime(start_time, '%Y.%m.%d %H:%M:%S')
    duration_time = duration_time.total_seconds()
    message = message.replace('placeholder', str(int(duration_time)/60)+'m '+str(int(duration_time)%60)+'s')

elif 'Problem' == alert_type:
    emoji=':x: '
    color='#ff0000'
else:
    emoji=':green_heart: '
    color='#ffe599'

attachments = {"title": title, "text": message, "color": color }
post={"text": alert_type, "attachments": [ attachments ]}

logging.info(post)

try:
    r = requests.post(url, json=post)
    logging.info(r)
except Exception, e:
    logging.error(e)

logging.info('######################################################')
