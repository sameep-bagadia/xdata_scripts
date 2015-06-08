import snap
import numpy as np
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import math
import sys
import fileinput
from datetime import datetime

space_gran = 10
time_gran = 2
lookback = 4.0

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


G = snap.TUNGraph.New()

node_map = {}
reverse_node_map = {}


def insert(key):
	if (not node_map.has_key(key)):
		val = G.GetNodes()
		node_map[key] = val
		G.AddNode(val)
		reverse_node_map[val] = key

def read_buckets(infile):
	with open(infile) as nycf:
		for line in nycf:
			line = line[:-1]
			line_arr = line.split('\t')
			label = int(line_arr[0])
			if (label == 1):
				bx = int(line_arr[6])
				by = int(line_arr[5])
				bt = int(line_arr[7])
				key = "%d,%d,%d" % (bx, by,bt)
				insert(key)

def add_edge(key1, key2):
	if (node_map.has_key(key1) and node_map.has_key(key2)):
		node1 = node_map[key1]
		node2 = node_map[key2]
		G.AddEdge(node1, node2)

def construct_edges():
	for key in node_map.keys():
		key_arr = key.split(',')
		bx = int(key_arr[0])
		by = int(key_arr[1])
		bt = int(key_arr[2])
		nbx = bx + space_gran
		nby = by + space_gran
		nbt = bt + 1
		add_edge(key, "%d,%d,%d" % (nbx, by, bt))
		add_edge(key, "%d,%d,%d" % (bx, nby, bt))
		add_edge(key, "%d,%d,%d" % (bx, by, nbt))

def GetBucketAgg(cmp):
	bx = 0
	by = 0
	bts = float('Inf')
	bte = -1
	magnitude = len(cmp)
	for node_id in cmp:
		bucket_arr = reverse_node_map[node_id].split(",")
		bx = bx + int(bucket_arr[0])
		by = by + int(bucket_arr[1])
		bt = int(bucket_arr[2])
		if (bt < bts):
			bts = bt
		if (bt > bte):
			bte = bt
	bx = bx / magnitude
	by = by / magnitude
	(lon, lat) = GetLongLat(bx, by)
	(date, time) = GetDateTime(bts-1) # -1 since bucket denotes the centre time of duration
	duration = (bte - bts + 2) * time_gran
	return (lon, lat, date, time, duration, magnitude)


def main():
	#read_buckets('/lfs/madmax/0/sameepb/xdata/ml_output2/concerts_pred.tsv')
	read_buckets('/lfs/madmax/0/sameepb/xdata/ml_output2/se_pred.tsv')
	outf = open('/lfs/madmax/0/sameepb/xdata/ml_output2/merged_events_se.tsv', 'w')
	construct_edges()
	print G.GetEdges(), G.GetNodes()
	Components = snap.TCnComV()
	snap.GetWccs(G, Components)
	print len(Components)
	"""
	lon \t lat \t date \t time \t #buckets
	"""
	for cmp in Components:
		(lon, lat, date, time, duration, magnitude) = GetBucketAgg(cmp)
		outf.write('%.10f\t%.10f\t%s\t%s\t%d\t%d\n' % (lat, lon, date, time, duration, magnitude))
		#print cmp.Len()

main()

