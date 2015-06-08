day_count = [0,0,31,59,90,120,151,181,212,212,242,273,301,334]
def get_day(date, month, year):
	return day_count[month + ((year - 2013)*12)] + date - 1

print get_day(21,5,2013)
print get_day(5,12,2013)
print get_day(25,3,2013)
print get_day(10,2,2013)
