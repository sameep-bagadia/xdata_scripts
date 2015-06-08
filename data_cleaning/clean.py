import fileinput

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

day_count = [0,0,31,59,90,120,151,181,212,243,273,304,334]

def calc_sec(stamp):
	stamp_arr = stamp.split(' ')
	date_arr = stamp_arr[0].split('-')
	time_arr = stamp_arr[1].split(':')
	time_days = (int(date_arr[0]) - 2013) * 365
	time_days += day_count[int(date_arr[1])]
	time_days += int(date_arr[2])
	time_hours = time_days * 24
	time_hours += int(time_arr[0])
	time_min = time_hours * 60
	time_min += int(time_arr[1])
	time_sec = time_min * 60
	time_sec += int(time_arr[2])
	return time_sec
	

def is_consistent(stamp1, stamp2, trip_time):
	time1 = calc_sec(stamp1)
	time2 = calc_sec(stamp2)
	if (time2 < time1):
		return False
	calc_time = time2 - time1
	if ((float(abs(calc_time - trip_time)) * 2.0 /float(calc_time + trip_time)) < 0.1):
		return True
	if (abs(calc_time - trip_time) <= 100):
		return True
	return False

def speed(dist, time_sec):
	time_hour = float(time_sec) / 3600.0
	return dist/time_hour

def interchanged(lon, lat):
	return ((float(lon) > 0) and (float(lat) < 0))

def main():
	count = 0
	for line in fileinput.input():
		line = line[:-1]
		line_arr = line.split(',')
		# check if latitues and longitudes are numbers
		if (not (is_number(line_arr[10]) and is_number(line_arr[11]) and is_number(line_arr[12]) and is_number(line_arr[13]))):
			continue
		#check if latitudes and longitudes are not 0
		if (float(line_arr[10]) * float(line_arr[11]) * float(line_arr[12]) * float(line_arr[13]) == 0):
			continue
		
		trip_time = int(line_arr[8])
		# check trip time > 0
		if (trip_time == 0):
			continue
		# check trip time matches with date and time stamps
		if (not is_consistent(line_arr[5], line_arr[6], trip_time)):
			continue
		# check reasonable speed
		trip_dist = float(line_arr[9])
		if (speed(trip_dist, trip_time) > 75):
			continue
		# check if latitude and longitudes are interchanged
		lon1 = line_arr[10]
		lat1 = line_arr[11]
		lon2 = line_arr[12]
		lat2 = line_arr[13]
		changed = False
		if (interchanged(lon1, lat1)):
			line_arr[10] = lat1
			line_arr[11] = lon1
			changed = True
		if (interchanged(lon2, lat2)):
			line_arr[12] = lat2
			line_arr[13] = lon2
			changed = True
		if (changed):
			count += 1
			line = line_arr[0]
			for i in range(1,14):
				line = line + "," + line_arr[i]
		# looks okay. so print the line
		#print line
	print count
		
main()







