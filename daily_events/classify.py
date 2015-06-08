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
0 : date 
1 : time 
2 : latitude 
3 : longitude 
4 : percent change in metric 
5 : metric value 
6 : avg metric value in past 4 weeks 
7 : sd of metric value in past 4 weeks 
8 : volume of trips 
9 : volume of trips in last 4 weeks
10: bucketx 
11: buckety 
12: buckett
"""

def main():
	inputfilepath = sys.argv[1]
	inputfilename = sys.argv[2]
	outputpath = sys.argv[3]
	inputfile = inputfilepath + inputfilename
	fmap = {}
	with open(inputfile) as ipfile:
		for line in ipfile:
			line = line[:-1]
			line_arr = line.split('\t')
			date = line_arr[0]
			bx = int(line_arr[10])
			by = int(line_arr[11])
			# out of bounds
			if ((bx <= 0) or (by <= 0)):
				continue
			# discard buckets with not much activity
			if (float(line_arr[8]) + float(line_arr[9]) < 100):
				continue
			# discard events based on standard deviation
			if (abs(float(line_arr[5]) - float(line_arr[6])) < float(line_arr[7])):
				continue

			if (not fmap.has_key(date)):
				fmap[date] = open(outputpath + date + '_' + inputfilename,'w')
			fmap.get(date).write("%s\n" % (line))

main()













