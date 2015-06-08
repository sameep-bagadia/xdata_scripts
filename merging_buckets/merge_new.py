# merge buckets
# first read in buckets and add a node in the graph if a node for that bucket doesn't already exist. Then form edges among the nodes. Then find connected cmponents
# merged events output : outf
# merged events output by listing all the buckets : outf_all

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
from location_bucket import *
from time_bucket import *


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
		nbx = bx + 1
		nby = by + 1
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
	(date, time) = GetDateTime(bts)
	duration = (bte - bts + 1) * time_gran
	return (lon, lat, date, time, duration, magnitude)


def main():
	# call read_buckets for each classifier output
	read_buckets('/lfs/madmax/0/sameepb/xdata/ml_output_new/concerts_pred3.tsv')
	read_buckets('/lfs/madmax/0/sameepb/xdata/ml_output_new/se_pred3.tsv')
	outf = open('/lfs/madmax/0/sameepb/xdata/ml_output_new/merged_events3.tsv', 'w')
	outf_all = open('/lfs/madmax/0/sameepb/xdata/ml_output_new/merged_events_buckets3.tsv', 'w')
	construct_edges()
	print G.GetNodes(), G.GetEdges()
	Components = snap.TCnComV()
	snap.GetWccs(G, Components)
	print len(Components)
	"""
	lon \t lat \t date \t time \t #buckets
	"""
	for cmp in Components:
		for node_id in cmp:
			bucket_arr = reverse_node_map[node_id].split(",")
			bx = int(bucket_arr[0])
			by = int(bucket_arr[1])
			bt = int(bucket_arr[2])
			(blon, blat) = GetLongLat(bx,by)
			(bdate, btime) = GetDateTime(bt)
			outf_all.write('%f,%f,%s,%s\t' % (blat, blon, bdate, btime))
		outf_all.write('\n')
		(lon, lat, date, time, duration, magnitude) = GetBucketAgg(cmp)
		outf.write('%f\t%f\t%s\t%s\t%d\t%d\n' % (lat, lon, date, time, duration, magnitude))
		#print cmp.Len()

main()

