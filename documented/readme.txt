Run the scripts in the order as shown below. None of the scripts take any arguments. To change files read into or written to by the script one needs to change the filename in the corresponding script. Look into individual scripts for more comments

1. generate_data_new1.py : Takes in data given by Sheila and creates a new data file and buckets list corresponding to each data point in the data file
2. generate_labels_new1 : Generates labels for each of the buckets in buckets list files. (Will need to run this twice (once each for concerts and special events)
3. rf_new1.py, rf_new2.py : Train classifiers uing data generated so far and predict labels for the buckets
4. merge_new.py : Merge the events using connected components approach.

time_bucket.py and location_bucket.py contain functions for converting back and forth from bucket ids to values.