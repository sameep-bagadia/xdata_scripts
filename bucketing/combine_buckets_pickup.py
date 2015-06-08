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

def main():
	with open('/lfs/local/0/sameepb/xdata/nyc/bucket_agg/bucket_agg2_pickup.csv') as nycf:
		for line in nycf:
			line = line[:-1]
			line_arr = line.split(',')
			bucket_x = int(line_arr[0])
			bucket_y = int(line_arr[1])
			bucket_time = int(line_arr[2])
			nbx = int(bucket_x / space_gran) * space_gran
			nby = int(bucket_y / space_gran) * space_gran
			#nbt = int(bucket_time / time_gran) * time_gran
			nbt = bucket_time
			for i in xrange(2):
				for j in xrange(2):
					for k in xrange(2):
						insert(nbx + i*space_gran, nby + j*space_gran, nbt + k, line_arr)
	outfile = '/lfs/local/0/sameepb/xdata/nyc/bucket_agg/bucket_combined2_pickup.csv'
	counts = []
	with open(outfile, "w") as outF:
		for key in bmap.keys():
			val = bmap.get(key)
			outF.write("%s,%f,%f,%f,%f,%d\n" % (key, val[0], val[1], val[2], val[3], val[4]))
			counts.append(val[4])

	# plot histogram
	plt.hist(counts, 200)
	plt.yscale('log')
	plt.savefig('plot.png')
	plt.close()
			
			

main()









