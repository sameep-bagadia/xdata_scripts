# Functions relating to time bucket.
# eg usage:	bt = GetTimeBucket("2013-01-01 00:00:00")
# eg usage:	(date, time) = GetDateTime(5)
# time_gran : number of hours between consecutive buckets
# lookback : number of weeks in past to compare from


import numpy as np
from math import radians, cos, sin, asin, sqrt
import math
import sys
import fileinput
from datetime import datetime

#time_gran = 4
time_gran = 2 # number of hours between consecutive buckets
lookback = 4.0 # number of weeks in past to compare from
day_count = [0,0,31,59,90,120,151,181,212,243,273,304,334,365]

def calc_sec(stamp):
	stamp_arr = stamp.split(' ')
	date_arr = stamp_arr[0].split('-')
	time_arr = stamp_arr[1].split(':')
	time_days = (int(date_arr[0]) - 2013) * 365
	time_days += day_count[int(date_arr[1])]
	time_days += int(date_arr[2])
	time_hours = time_days * 24
	time_hours += int(time_arr[0])
	time_min = time_hours * 60
	time_min += int(time_arr[1])
	time_sec = time_min * 60
	time_sec += int(time_arr[2])
	return time_sec

ref_time = calc_sec("2013-01-01 00:00:00")

def GetTimeBucket(dt):
	ev_time = calc_sec(dt)
	diff = ev_time - ref_time
	bucket = int(diff / (time_gran*60*60))  #time_gran hours interval
	return bucket

def GetDateTime(bt):
	days = int((bt * time_gran) / 24)
	hour = (bt * time_gran) % 24
	if (days >= 365):
		date = "2014-01-%d" % (days-365+1)
	else:
		month = 1
		while(day_count[month] <= days):
			month += 1
		month -= 1
		day = days - day_count[month] + 1
		date = "2013-%02d-%02d" % (month, day)
	time = "%02d:00:00" % (hour)
	return (date, time)

# 8am to 10pm
def during_day(bt):
	days = int((bt * time_gran) / 24)
	hour = (bt * time_gran) % 24
	if ((hour >= 8) and (hour <= 22)):
		return True
	else:
		return False


def calc_sec_data(stamp):
	stamp_arr = stamp.split(' ')
	date_arr = stamp_arr[0].split('/')
	time_arr = stamp_arr[1].split(':')
	time_days = (int(date_arr[2]) - 13) * 365
	time_days += day_count[int(date_arr[0])]
	time_days += int(date_arr[1])
	time_hours = time_days * 24
	time_hours += int(time_arr[0])
	time_min = time_hours * 60
	time_min += int(time_arr[1])
	time_sec = time_min * 60
	#time_sec += int(time_arr[2])
	return time_sec

ref_time_data = calc_sec_data("1/1/13 00:00")

def GetTimeBucket_data(dt):
	ev_time = calc_sec_data(dt)
	diff = ev_time - ref_time_data
	bucket = int(diff / (time_gran*60*60))  #time_gran hours interval
	return bucket
