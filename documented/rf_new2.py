# Train the random forest classifier on 'data_file' using labels from 'y1' (special events data). Use the trained classifier to predict events and store the predicted events in file 'outf_out'

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

from sklearn import linear_model
from sklearn import cross_validation
from sklearn import ensemble
from sklearn import preprocessing

lookback = 4.0

def main():
  data_file = '/lfs/madmax/0/sameepb/xdata/ml_data_new/data3.csv'
	X_orig = np.genfromtxt(data_file, delimiter=',')
	X = X_orig[:,3:X_orig.shape[1]]
	y0 = np.genfromtxt('/lfs/madmax/0/sameepb/xdata/ml_data_new/labels_concerts3.txt', delimiter=',')
	y1 = np.genfromtxt('/lfs/madmax/0/sameepb/xdata/ml_data_new/labels_se3.txt', delimiter=',')

	outf_inp = open('/lfs/madmax/0/sameepb/xdata/ml_output_new/se_train3.tsv', 'w')
	outf_out = open('/lfs/madmax/0/sameepb/xdata/ml_output_new/se_pred3.tsv', 'w')
	#outform = open('/lfs/madmax/0/sameepb/xdata/ml_output_new/concerts_buckets.csv', 'w')

	X_train = X
	y_train = y1
	X_test = X
	y_test = y0
	#print "total ones = %d" % (sum(y))
	m = X.shape[0]
	for i in xrange(m):
		if(not np.all(np.isfinite(X[i,:]))):
			print i
			print X[i,:]
			break
	#n = Data.shape[1] - 2
	#X = Data[:,1:n+1]
	#y = Data[:,n+1:n+2]
	#X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=0)
	
	#y_train.shape = (y_train.shape[0], )
	#y_test.shape = (y_test.shape[0], )
	#for d in range(10,15):
	print X.shape
	print y1.shape

	#print y_train.shape
	#print y_test.shape
	for d in range(45,46):
		print "d = %d" % (d)
		rand_for = ensemble.RandomForestClassifier(max_depth=d, n_jobs = 40, class_weight='auto')
		#rand_for = ensemble.RandomForestClassifier(n_jobs = 40, class_weight='auto')
		rand_for.fit(X_train,y_train)

		train_accuracy = rand_for.score(X_train, y_train)
		test_accuracy = rand_for.score(X_test, y_test)

		y_test_pr = rand_for.predict(X_test)
		count11 = sum(y_test*y_test_pr)
		count10 = sum(y_test*(1-y_test_pr))
		count01 = sum((1-y_test)*y_test_pr)
		count00 = sum((1-y_test)*(1-y_test_pr))

		print "count00 = %d \t count01 = %d \t count10 = %d \t count11 = %d" % (count00, count01, count10, count11)
		precision = float(count11) / float(sum(y_test_pr))
		recall = float(count11) / float(sum(y_test))

		print "precision = %f" % (precision)
		print "recall = %f" % (recall)

		count11 = sum(y_train*y_test_pr)
		count10 = sum(y_train*(1-y_test_pr))
		count01 = sum((1-y_train)*y_test_pr)
		count00 = sum((1-y_train)*(1-y_test_pr))

		precision = float(count11) / float(sum(y_test_pr))
		recall = float(count11) / float(sum(y_train))

		print "precision = %f" % (precision)
		print "recall = %f" % (recall)
	
		print "Train accuracy = %f" % (train_accuracy)
		print "Test accuracy = %f" % (test_accuracy)

		return
		
		y_prob = rand_for.predict_proba(X)
		y_pred = rand_for.predict(X)
		""" output classes
		label \t lat \t lon \t date \t time \t by \t bx \t bt \t probability
		"""
		""" training classes
		label \t lat \t lon \t date \t time \t by \t bx \t bt 
		"""
		for i in xrange(m):
			by = X_orig[i,0]
			bx = X_orig[i,1]
			bt = X_orig[i,2]
			(lon, lat) = GetLongLat(bx, by)
			(date, time) = GetDateTime(bt)
			outf_inp.write('%d\t%f\t%f\t%s\t%s\t%d\t%d\t%d\n' % (y_train[i], lat, lon, date, time, by, bx, bt))
			outf_out.write('%d\t%f\t%f\t%s\t%s\t%d\t%d\t%d\t%f\n' % (y_pred[i], lat, lon, date, time, by, bx, bt, y_prob[i,1]))
		
	
	
main()
