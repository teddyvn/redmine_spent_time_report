# Redmine Spent Time Report For Last Month
# Author: Nguyen Huu Phuoc (phuoc{dot}h{dot}nguyen{at}gmail{dot}com)
# It requires redmine.conf file
# Create: 2019-08-08
from redminelib import Redmine
from datetime import date
import datetime
import calendar
import configparser
config = configparser.ConfigParser()
config.readfp(open(r'redmine.conf'))
url = config.get('Redmine', 'url')
key = config.get('Redmine', 'key')
members = config.get('Redmine', 'members')
now = datetime.datetime.now()
m = now.month - 1
y = now.year
if m == 0:
    m = 12
    y = y - 1
monthrange = calendar.monthrange(y,m)
fromdate = date(y,m,1)
todate = date(y,m,monthrange[1])
uids = members.split(",")
pidList = dict()
uidList = dict()
timeList = dict()
redmine = Redmine(url,key=key)
for user in uids:
    offset = 0
    cont = True
    while cont:
        time_entries = redmine.time_entry.filter(offset=offset,limit=100,user_id=int(user),from_date=fromdate,to_date=todate)
        if len(time_entries) < 100:
            #got whole, break while loop
            cont = False
        else:
            #get next page
            offset += 100
        for time_entry in time_entries:
            pid = time_entry.project.id
            uid = time_entry.user.id
            h = time_entry.hours
            if pid not in pidList:
                pidList[pid] = time_entry.project.name
            if uid not in uidList:
                uidList[uid] =  time_entry.user.name
            if uid in timeList:
                ps = timeList[uid]
                if pid in ps:
                    t = ps[pid]
                    ps[pid] = t + h
                else:
                    ps[pid] = h    
            else:
                ps = dict()
                ps[pid] = h
            timeList[uid] = ps            
#write in CSV format
for user in timeList:
    ps = timeList[user]
    for project in ps:
        print(uidList[user]+","+pidList[project]+","+str(ps[project]))