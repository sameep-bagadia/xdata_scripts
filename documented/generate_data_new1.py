# This script takes in data from 'data_input' file and writes the same data to 'dataf' after filtering those buckets which are in the first four (lookback) weeks. We only keep those buckets for which we have the entire previous data of 4 (lookback) weeks. We also convert the date and time to time bucket bt.

# Also it creates a new file 'bucketf' where each lines is (bx,by,bt) and the same line nummber in 'dataf' and 'bucketf' correspond to same bucket. 'bucketf' is used to generate labels for the data.


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

def main():
	#dataf = open('/dfs/scratch0/sameepb/xdata/ml_data/data2.tsv', 'w')
  data_input = '/dfs/scratch0/ramasshe/xdata/output/full_no_overlap_4hr_1mi.tsv'
	outfilepath = '/dfs/scratch0/sameepb/xdata/ml_data_new/'
	dataf = open(outfilepath + 'data2.csv', 'w')
	bucketf = open(outfilepath + 'bucket2.csv', 'w')
	with open(data_input) as nycf:
		for line in nycf:
			line = line[:-1]
			line_arr = line.split('\t')
			by = int(line_arr[0])
			bx = int(line_arr[1])
			bt = GetTimeBucket(line_arr[2] + ' ' + line_arr[3])
      # skip those data points which are in the first 'lookback' number of weeks
      # time gran is the number of hours between consecutive time buckets
			if (bt <= (lookback * 7 * 24 / time_gran)):
				continue
			dataf.write('%s,%s,%d' % (by, bx, bt)) #by, bx, bt
			for i in xrange(4, len(line_arr)):
				dataf.write(',%s' % (line_arr[i]))
			dataf.write('\n')
			bucketf.write("%d,%d,%d\n" % (bx, by, bt))
		

main()



