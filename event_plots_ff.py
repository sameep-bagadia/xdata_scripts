import numpy as np
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    #r = 6371  Radius of earth in kilometers. Use 3956 for miles
    r = 3956
    return c * r

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


day_count = [0,0,31,59,90,120,151,181,212,243,273,304,334,365]
def get_day(date, month, year):
	return day_count[month + ((year - 2013)*12)] + date - 1

def main():

	weekdays_count = [53,53,53,53,52,52,52]
	num_days = 368
	
	trip_lengths = np.zeros(num_days)
	trip_times = np.zeros(num_days)
	trip_speed = np.zeros(num_days)
	passenger_counts = np.zeros(num_days)
	trip_counts = np.zeros(num_days)

	agg_trip_lengths = np.zeros(7)
	agg_trip_times = np.zeros(7)
	agg_trip_speed = np.zeros(7)
	agg_passenger_counts = np.zeros(7)
	agg_trip_counts = np.zeros(7)

	event_lat = 40.7590615
	event_lon = -73.969231
	'''
	event_date = 21
	event_month = 5
	event_year = 2013
	event_day = get_day(event_date, event_month, event_year)
	'''
	# iterate through all data to fill these arrays
	total_trips = 0
	trips_considered = 0
	with open('filelist_nyc.txt') as f:
		for filename in f:
			filename = filename[:-1]
			print filename
			filepath = '/dfs/scratch0/dataset/xdata/SummerCamp2015/nyc_taxi_trip/' + filename
			with open(filepath) as nycf:
				for line in nycf:
					line = line[:-1]
					#print line
					line_arr = line.split(',')
					if (not (is_number(line_arr[12]) and is_number(line_arr[13]))):
						continue
					drop_lat = float(line_arr[13])
					drop_lon = float(line_arr[12])
					total_trips += 1
					#print haversine(drop_lon, drop_lat, event_lon, event_lat)
					if (haversine(drop_lon, drop_lat, event_lon, event_lat) < 1):
						date_time_drop = line_arr[6]
						passenger_count = float(line_arr[7])
						trip_time = float(line_arr[8])
						if (trip_time == 0):
							#print line
							continue
						trips_considered += 1
						trip_length = float(line_arr[9])
						trip_date_arr = date_time_drop.split(' ')[0].split('-')
						trip_year = int(trip_date_arr[0])
						trip_month = int(trip_date_arr[1])
						trip_date = int(trip_date_arr[2])
						trip_day = get_day(trip_date, trip_month, trip_year)
						trip_lengths[trip_day] += trip_length
						trip_times[trip_day] += trip_time
						trip_speed[trip_day] += trip_length / trip_time
						passenger_counts[trip_day] += passenger_count
						trip_counts[trip_day] += 1
						weekday_no = trip_day % 7
						agg_trip_lengths[weekday_no] += trip_length
						agg_trip_times[weekday_no] += trip_time
						agg_trip_speed[weekday_no] += trip_length / trip_time
						agg_passenger_counts[weekday_no] += passenger_count
						agg_trip_counts[weekday_no] += 1

	# postprocessing of the data collected
	trip_lengths = trip_lengths / trip_counts
	trip_times = trip_times / trip_counts
	trip_speed = trip_speed / trip_counts
	passenger_counts = passenger_counts / trip_counts

	agg_trip_lengths = agg_trip_lengths / agg_trip_counts
	agg_trip_times = agg_trip_times / agg_trip_counts
	agg_trip_speed = agg_trip_speed / agg_trip_counts
	agg_passenger_counts = agg_passenger_counts / agg_trip_counts

	perday_trip_counts = agg_trip_counts / weekdays_count

	pc_trip_lengths = np.zeros(num_days)
	pc_trip_times = np.zeros(num_days)
	pc_trip_speed = np.zeros(num_days)
	pc_passenger_counts = np.zeros(num_days)
	pc_trip_counts = np.zeros(num_days)
	for i in xrange(num_days):
		pc_trip_lengths[i] = (trip_lengths[i] - agg_trip_lengths[i%7])*100.0 / agg_trip_lengths[i%7]
		pc_trip_times[i] = (trip_times[i] - agg_trip_times[i%7])*100.0 / agg_trip_times[i%7]
		pc_trip_speed[i] = (trip_speed[i] - agg_trip_speed[i%7])*100.0 / agg_trip_speed[i%7]
		pc_passenger_counts[i] = (passenger_counts[i] - agg_passenger_counts[i%7])*100.0 / agg_passenger_counts[i%7]
		pc_trip_counts[i] = (trip_counts[i] - perday_trip_counts[i%7])*100.0 / perday_trip_counts[i%7]

	wow_trip_lengths = np.zeros(num_days)
	wow_trip_times = np.zeros(num_days)
	wow_trip_speed = np.zeros(num_days)
	wow_passenger_counts = np.zeros(num_days)
	wow_trip_counts = np.zeros(num_days)
	for i in range(7,num_days):
		wow_trip_lengths[i] = (trip_lengths[i] - trip_lengths[i-7]) * 100.0 / trip_lengths[i-7]
		wow_trip_times[i] = (trip_times[i] - trip_times[i-7]) * 100.0 / trip_times[i-7]
		wow_trip_speed[i] = (trip_speed[i] - trip_speed[i-7]) * 100.0 / trip_speed[i-7]
		wow_passenger_counts[i] = (passenger_counts[i] - passenger_counts[i-7]) * 100.0 / passenger_counts[i-7]
		wow_trip_counts[i] = (trip_counts[i] - trip_counts[i-7]) * 100.0 / trip_counts[i-7]

	# plots
	plt.figure(1)
	plt.plot(pc_trip_lengths)
	plt.title('Percent change in Trip lengths')
	plt.savefig('plots/plots-ff/plot1.png')
	plt.close()

	plt.figure(2)
	plt.plot(pc_trip_times)
	plt.title('Percent change in Trip times')
	plt.savefig('plots/plots-ff/plot2.png')
	plt.close()

	plt.figure(3)
	plt.plot(pc_trip_speed)
	plt.title('Percent change in Trip speed')
	plt.savefig('plots/plots-ff/plot3.png')
	plt.close()

	plt.figure(4)
	plt.plot(pc_passenger_counts)
	plt.title('Percent change in Passenger Counts')
	plt.savefig('plots/plots-ff/plot4.png')
	plt.close()

	plt.figure(5)
	plt.plot(pc_trip_counts)
	plt.title('Percent change in Trip counts')
	plt.savefig('plots/plots-ff/plot5.png')
	plt.close()

	plt.figure(6)
	plt.plot(trip_counts)
	plt.title('Trip counts')
	plt.savefig('plots/plots-ff/plot6.png')
	plt.close()

	plt.figure(7)
	plt.plot(trip_lengths)
	plt.title('Trip lengths')
	plt.savefig('plots/plots-ff/plot7.png')
	plt.close()

	plt.figure(8)
	plt.plot(trip_times)
	plt.title('Trip times')
	plt.savefig('plots/plots-ff/plot8.png')
	plt.close()

	plt.figure(9)
	plt.plot(trip_speed)
	plt.title('Trip speed')
	plt.savefig('plots/plots-ff/plot9.png')
	plt.close()

	plt.figure(10)
	plt.plot(passenger_counts)
	plt.title('Passenger Counts')
	plt.savefig('plots/plots-ff/plot10.png')
	plt.close()

	plt.figure(11)
	plt.plot(wow_trip_lengths)
	plt.title('wow change in Trip lengths')
	plt.savefig('plots/plots-ff/plot11.png')
	plt.close()

	plt.figure(12)
	plt.plot(wow_trip_times)
	plt.title('wow change in Trip times')
	plt.savefig('plots/plots-ff/plot12.png')
	plt.close()

	plt.figure(13)
	plt.plot(wow_trip_speed)
	plt.title('wow change in Trip speed')
	plt.savefig('plots/plots-ff/plot13.png')
	plt.close()

	plt.figure(14)
	plt.plot(wow_passenger_counts)
	plt.title('wow change in Passenger Counts')
	plt.savefig('plots/plots-ff/plot14.png')
	plt.close()

	plt.figure(15)
	plt.plot(wow_trip_counts)
	plt.title('wow change in Trip counts')
	plt.savefig('plots/plots-ff/plot15.png')
	plt.close()

	print total_trips, trips_considered

main()







