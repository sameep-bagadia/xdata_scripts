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

def main():
	bmap = {}
	with open('filelist_nyc.txt') as f:
		for filename in f:
			filename = filename[:-1]
			print filename
			path_pickup = '/lfs/local/0/sameepb/xdata/nyc/pickup_buckets2/'
			path_dropoff = '/lfs/local/0/sameepb/xdata/nyc/dropoff_buckets2/'
			filepaths = [path_pickup + filename]
			for filepath in filepaths:
				with open(filepath) as nycf:
					for line in nycf:
						line = line[:-1]
						#print line
						line_arr = line.split(',')
						trip_time = float(line_arr[11])
						trip_dist = float(line_arr[12])
						trip_speed = trip_dist / trip_time
						pass_cnt = float(line_arr[10])
						key = "%s,%s,%s" % (line_arr[0], line_arr[1], line_arr[2])
						if (not bmap.has_key(key)):
							bmap[key] = np.zeros(5)
						val = bmap.get(key)
						val[0] += trip_dist
						val[1] += trip_time
						val[2] += trip_speed
						val[3] += pass_cnt
						val[4] += 1
						bmap[key] = val
	outfile = '/lfs/local/0/sameepb/xdata/nyc/bucket_agg/bucket_agg2_pickup.csv'
	with open(outfile, "w") as outF:
		for key in bmap.keys():
			val = bmap.get(key)
			outF.write("%s,%f,%f,%f,%f,%d\n" % (key, val[0], val[1], val[2], val[3], val[4]))
							

	
main()
