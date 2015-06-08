import numpy as np
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import math
import sys
import fileinput
from datetime import datetime

bx = 0
by = 0
bt = 1706
time_gran = 2
filename='/lfs/local/0/sameepb/xdata/nyc/bucket_agg/bucket_combined2_pickup.csv'

def main():
	bmap = {}
	for i in xrange(368 * 24 / time_gran):
		if (((i - bt) % (7 * 24 / time_gran)) == 0):
			bmap[i] = 0
	with open(filename) as nycf:
		for line in nycf:
			line = line[:-1]
			line_arr = line.split(',')
			bucket_x = int(line_arr[0])
			bucket_y = int(line_arr[1])
			bucket_time = int(line_arr[2])
			if ((bucket_x == bx) and (bucket_y == by)):
				if (bmap.has_key(bucket_time)):
					bmap[bucket_time] = float(line_arr[4]) / float(line_arr[7])
	volume_vec = []
	for key in sorted(bmap.keys()):
		volume_vec.append(bmap.get(key))

	plt.figure(1)
	plt.plot(volume_vec)
	plt.title('time')
	plt.savefig("%d_%d_%d_time.png" % (bx,by,bt))
	plt.close()
					

main()
