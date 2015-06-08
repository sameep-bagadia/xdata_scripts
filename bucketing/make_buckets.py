import numpy as np
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import math
import sys
import fileinput
from datetime import datetime

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
location_type="dropoff"
time_gran = 2

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
OUTPUT_TIME_FORMAT = "%Y-%m-%d"

BUCKET_DIST = 50 # in miles

class Direction:
    north = 1
    south = 2
    east = 3
    west = 4

def dist(lat1, lon1, lat2, lon2):
  lat1 *= math.pi / 180
  lat2 *= math.pi / 180
  lon1 *= math.pi / 180
  lon2 *= math.pi / 180
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  a = pow(math.sin(dlat/2), 2) + math.cos(lat1) * math.cos(lat2) * pow(math.sin(dlon/2), 2) 
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
  d = RADIUS_EARTH * c
  return d


# Change in longitude
def GetDX(coord1, coord2=(CENTER_LONG, CENTER_LAT)):
    """Coordinates should be tuples consisting of floats, of the form (longitude, latitude)."""
    (lon1, lat1) = coord1
    (lon2, lat2) = coord2
    # Keep latitude fixed to get horizontal distance distance
    distance = dist(lat1, lon1, lat1, lon2)
    if lon1 > lon2:
        direction = Direction.east
    else:
        direction = Direction.west
    return (distance, direction)

def GetDY(coord1, coord2=(CENTER_LONG, CENTER_LAT)):
    """Coordinates should be tuples consisting of floats, of the form (longitude, latitude)."""
    (lon1, lat1) = coord1
    (lon2, lat2) = coord2
    # Keep latitude fixed to get horizontal distance distance
    distance = dist(lat1, lon1, lat2, lon1)
    if lat1 > lat2:
        direction = Direction.north
    else:
        direction = Direction.south
    return (distance, direction)

def GetBucket(coord1, coord2=(CENTER_LONG, CENTER_LAT)):
    (xdist, xdir) = GetDX(coord1, coord2)
    (ydist, ydir) = GetDY(coord1, coord2)
    bucketx = buckety = 0
    if xdist >= BUCKET_DIST or ydist >= BUCKET_DIST:
        bucketx = buckety = OUT_BOUNDS
        if (coord1[0] == 0 and coord1[1] == 0):
            bucketx = buckety = NO_COORDS
    else:
        if xdir == Direction.east:
            tempx = BUCKET_DIST + xdist
        else:
            tempx = BUCKET_DIST - xdist
        if ydir == Direction.north:
            tempy = BUCKET_DIST + ydist
        else:
            tempy = BUCKET_DIST - ydist
        bucketx = int(tempx*BUCKETS_PER_MILE)
        buckety = int(tempy*BUCKETS_PER_MILE)
    return (bucketx, buckety)

day_count = [0,0,31,59,90,120,151,181,212,243,273,304,334]

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

def main():
	ref_time = calc_sec("2013-01-01 00:00:00")
	for line in fileinput.input():
		line = line[:-1]
		line_arr = line.split(',')
		if (location_type == "pickup"):
			lon = float(line_arr[10])
			lat = float(line_arr[11])
			dt = line_arr[5]
		elif (location_type == "dropoff"):
			lon = float(line_arr[12])
			lat = float(line_arr[13])
			dt = line_arr[6]
		else:
			raise Exception("Not a proper location to bucket")
		loc_bucket = GetBucket((lon, lat))
		time_bucket = GetTimeBucket(dt)
		print "%d,%d,%d,%s" % (loc_bucket[0], loc_bucket[1], time_bucket, line)
	

main()







