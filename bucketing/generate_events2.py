import numpy as np
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import math
import sys
import fileinput
from datetime import datetime

"""
0 : total distance
1 : total time
2 : total speed
3 : total #passengers
4 : trip counts
"""
space_gran = 10
time_gran = 2
bmap = {}
lookback = 4

CENTER_LONG = -73.9954898
CENTER_LAT = 40.7214947
RADIUS_EARTH = 3959 # in miles
OUT_BOUNDS = -1
NO_COORDS = -2
BUCKETS_PER_MILE = 20
PICKUP_LONG = 0
PICKUP_LAT = 1
DROPOFF_LONG = 2
DROPOFF_LAT = 3
PICKUP_TIME = 4
DROPOFF_TIME = 5

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
OUTPUT_TIME_FORMAT = "%Y-%m-%d"

BUCKET_DIST = 50 # in miles

class Direction:
    north = 1
    south = 2
    east = 3
    west = 4

def GetLongLat(bucket_x, bucket_y, coord2=(CENTER_LONG, CENTER_LAT)):
    middle_bucket = BUCKET_DIST * BUCKETS_PER_MILE
    # Get direction from the center point
    dist_x = bucket_x/float(BUCKETS_PER_MILE)
    dist_y = bucket_y/float(BUCKETS_PER_MILE)
    direction = [0, 0]
    if dist_x > BUCKET_DIST:
        dist_x -= BUCKET_DIST
        direction[0] = Direction.east
    else:
        dist_x = BUCKET_DIST - dist_x
        direction[0] = Direction.west
    if dist_y > BUCKET_DIST:
        dist_y -= BUCKET_DIST
        direction[1] = Direction.north
    else:
        dist_y = BUCKET_DIST - dist_y
        direction[1] = Direction.south
    # Get longitude
    (lon2, lat2) = coord2
    lat2 *= math.pi / 180
    lon2 *= math.pi / 180
    c = dist_x/RADIUS_EARTH
    b = math.tan(c/2)
    a = pow(b, 2)/(1 + pow(b,2))
    deltaLon =  2 * math.asin(math.sqrt(a / (pow(math.cos(lat2), 2))))
    if direction[0] == Direction.east:
        lon1 = lon2 + deltaLon
        lon1 /= (math.pi * 1/180)
    else:
        lon1 = lon2 - deltaLon
        lon1 /= (math.pi * 1/180)
    # Calculate latitude
    c = dist_y/RADIUS_EARTH
    b = math.tan(c/2)
    a = pow(b, 2)/(1 + pow(b,2))
    deltaLat =  2 * math.sqrt(a)
    if direction[1] == Direction.north:
        lat1 = lat2 + deltaLat
        lat1 /= (math.pi * 1/180)
    else:
        lat1 = lat2 - deltaLat
        lat1 /= (math.pi * 1/180)
    return (lon1, lat1)

def insert(bx, by, bt, line_arr):
	key = "%d,%d,%d" % (bx,by,bt)
	if (not bmap.has_key(key)):
		bmap[key] = np.zeros(5)
	val = bmap.get(key)
	val[0] += float(line_arr[3])
	val[1] += float(line_arr[4])
	val[2] += float(line_arr[5])
	val[3] += float(line_arr[6])
	val[4] += int(line_arr[7])
	bmap[key] = val

day_count = [0,0,31,59,90,120,151,181,212,243,273,304,334,365]
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

def main():
	with open('/lfs/local/0/sameepb/xdata/nyc/bucket_agg/bucket_combined2.csv') as nycf:
		for line in nycf:
			line = line[:-1]
			line_arr = line.split(',')
			bucket_x = int(line_arr[0])
			bucket_y = int(line_arr[1])
			bucket_time = int(line_arr[2])
			insert(bucket_x, bucket_y, bucket_time, line_arr)

	filepath = '/lfs/local/0/sameepb/xdata/nyc/events2/'
	fdist = open(filepath + 'pc_dist.csv','w')
	ftime = open(filepath + 'pc_time.csv','w')
	fspeed = open(filepath + 'pc_speed.csv','w')
	fpc = open(filepath + 'pc_pc.csv','w')
	fcnt = open(filepath + 'pc_cnt.csv','w')
	for key in bmap.keys():
		val = bmap.get(key)
		#if (val[4] >= 5000):
		if (True):
			b_arr = key.split(',')
			bx = int(b_arr[0])
			by = int(b_arr[1])
			bt = int(b_arr[2])
			if (bt <= (lookback * 7 * 24 / time_gran)):
				continue
			event_trip_time = val[1]/val[4]
			event_trip_dist = val[0]/val[4]
			event_trip_speed = val[2]/val[4]
			event_pass_cnt = val[3]/val[4]
			event_trip_cnt = val[4]
			past_trip_time = 0.0
			past_trip_dist = 0.0
			past_trip_speed = 0.0
			past_pass_cnt = 0.0
			past_trip_cnt = 0.0
			past_trip_time_sq = 0.0
			past_trip_dist_sq = 0.0
			past_trip_speed_sq = 0.0
			past_pass_cnt_sq = 0.0
			past_trip_cnt_sq = 0.0
			for i in range(1,lookback+1):
				ibt = bt - (i*7*24/time_gran)
				ikey = "%d,%d,%d" % (bx, by, ibt)
				if (bmap.has_key(ikey)):
					ival = bmap.get(ikey)
					past_trip_dist += ival[0]
					past_trip_time += ival[1]
					past_trip_speed += ival[2]
					past_pass_cnt += ival[3]
					past_trip_cnt += ival[4]
					past_trip_dist_sq += ival[0]*ival[0]
					past_trip_time_sq += ival[1]*ival[1]
					past_trip_speed_sq += ival[2]*ival[2]
					past_pass_cnt_sq += ival[3]*ival[3]
					past_trip_cnt_sq += ival[4]*ival[4]
			if (past_trip_cnt <= 10):
				#print "no past data!"
				# not enough data
				# handle this case
				continue
			past_trip_dist = past_trip_dist / past_trip_cnt
			past_trip_time = past_trip_time / past_trip_cnt
			past_trip_speed = past_trip_speed / past_trip_cnt
			past_pass_cnt = past_pass_cnt / past_trip_cnt
			past_trip_cnt = past_trip_cnt / lookback

			past_trip_dist_sq = past_trip_dist_sq / past_trip_cnt
			past_trip_time_sq = past_trip_time_sq / past_trip_cnt
			past_trip_speed_sq = past_trip_speed_sq / past_trip_cnt
			past_pass_cnt_sq = past_pass_cnt_sq / past_trip_cnt
			past_trip_cnt_sq = past_trip_cnt_sq / lookback

			dist_var = past_trip_dist_sq - (past_trip_dist * past_trip_dist)
			time_var = past_trip_time_sq - (past_trip_time * past_trip_time)
			speed_var = past_trip_speed_sq - (past_trip_speed * past_trip_speed)
			pc_var = past_pass_cnt_sq - (past_pass_cnt * past_pass_cnt)
			cnt_var = past_trip_cnt_sq - (past_trip_cnt * past_trip_cnt)

			pc_dist = (event_trip_dist - past_trip_dist) * 100.0 / past_trip_dist
			pc_time = (event_trip_time - past_trip_time) * 100.0 / past_trip_time
			pc_speed = (event_trip_speed - past_trip_speed) * 100.0 / past_trip_speed
			pc_pc = (event_pass_cnt - past_pass_cnt) * 100.0 / past_pass_cnt
			pc_cnt = (event_trip_cnt - past_trip_cnt) * 100.0 / past_trip_cnt

			(lon, lat) = GetLongLat(bx, by)
			(date, time) = GetDateTime(bt)

			'''
			date \t time \t latitude \t longitude \t percent change in metric \t metric value \t avg metric value in past 4 weeks \t sd of metric value in past 4 weeks \t volume of trips \t volume of trips in last 4 weeks \t bucketx \t buckety \t buckett
			'''
			fdist.write("%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%f\t%d\t%d\t%d\n" % (date, time, lat, lon, pc_dist, event_trip_dist, past_trip_dist, math.sqrt(dist_var), event_trip_cnt, past_trip_cnt, bx, by, bt))
			ftime.write("%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%f\t%d\t%d\t%d\n" % (date, time, lat, lon, pc_time, event_trip_time, past_trip_time, math.sqrt(time_var), event_trip_cnt, past_trip_cnt, bx, by, bt))
			fspeed.write("%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%f\t%d\t%d\t%d\n" % (date, time, lat, lon, pc_speed, event_trip_speed, past_trip_speed, math.sqrt(speed_var), event_trip_cnt, past_trip_cnt, bx, by, bt))
			fpc.write("%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%f\t%d\t%d\t%d\n" % (date, time, lat, lon, pc_pc, event_pass_cnt, past_pass_cnt, math.sqrt(pc_var), event_trip_cnt, past_trip_cnt, bx, by, bt))
			fcnt.write("%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%f\t%d\t%d\t%d\n" % (date, time, lat, lon, pc_cnt, event_trip_cnt, past_trip_cnt, math.sqrt(cnt_var), event_trip_cnt, past_trip_cnt, bx, by, bt))
			
		

main()



