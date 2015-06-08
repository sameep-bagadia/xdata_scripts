# This file takes in 'inputfile' (concert or special events data) and generates labels for buckets corresponding to the file 'bucketsfile' and stores the labels in 'labelsfile'

import numpy as np
#import matplotlib
#matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
#import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import math
import sys
import fileinput
from datetime import datetime
from location_bucket import *
from time_bucket import *

lmap = {}
def insert(bx, by, bt):
	key = "%d,%d,%d" % (bx,by,bt)
	if (not lmap.has_key(key)):
		lmap[key] = 1

def main():
	inputfile = 'special_events.csv'
	#inputfile = 'concerts2.txt'
	#skip_lines = 0
  
  # read the 'inputfile' and store the buckets to be marked as events in the dict.
	with open(inputfile) as ipf:
		for line in ipf:
			#if (skip_lines > 0):
			#	print line
			#	skip_lines = skip_lines - 1
			#	continue
			line = line[:-1]
			#print line
			#print "nothing"
			line_arr_all = line.split(',')
			for id in xrange(len(line_arr_all) / 13):
				line_arr = line_arr_all[id*13:(id+1)*13]
				#print ",".join(line_arr)
				lat = float(line_arr[11])
				lon = float(line_arr[12])
				(bx, by) = GetBucket((lon, lat))
				bts = GetTimeBucket_data(line_arr[7])
				bte = GetTimeBucket_data(line_arr[8])
        
				# if longer than 48 hours, then skip it. else we add consider the surrounding buckets as events too.
				if ((bte - bts) > (48 / time_gran)):
					continue
					"""
					for i in range(-1,2):
						for j in xrange(-1,2):
							for k in range(bts, bte+1):
								if during_day(k):
									insert(bx + i, by + j, k)
					"""
				else:
					for i in range(-1,2):
						for j in xrange(-1,2):
							for k in range(bts, bte+1):
								insert(bx + i, by + j, k)

  # go through each bucket in the 'bucketsfile' and mark it 1 or 0 depending on whether it is present in the dict or not.
	print len(lmap.keys())
	bucketsfile = '/dfs/scratch0/sameepb/xdata/ml_data_new/bucket1.csv'
	#labelsfile = open('/dfs/scratch0/sameepb/xdata/ml_data_new/labels_concerts3.txt', 'w')
	labelsfile = open('/dfs/scratch0/sameepb/xdata/ml_data_new/labels_se3.txt', 'w')
	count1 = 0
	with open(bucketsfile) as bf:
		for line in bf:
			key = line[:-1]
			if (lmap.has_key(key)):
				labelsfile.write('1\n')
				count1 += 1
			else:
				labelsfile.write('0\n')

	print count1
	
main()










