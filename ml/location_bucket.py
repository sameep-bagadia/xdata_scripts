import numpy as np
from math import radians, cos, sin, asin, sqrt
import math
import sys
import fileinput
from datetime import datetime

# Center of the grid
CENTER_LONG = -74.00 #-73.9954898
CENTER_LAT = 40.72 #40.7214947
# Size of each bucket in the grid
LON_DELTA = 0.01
LAT_DELTA = 0.01
BUCKET_RADIUS = 100 # how many buckets to the right and left of the center
"""
LON_DELTA = 0.02
LAT_DELTA = 0.02
BUCKET_RADIUS = 50 # how many buckets to the right and left of the center
"""
# Bottom Right corner of the generated grid
BR_LONG = CENTER_LONG - LON_DELTA * BUCKET_RADIUS
BR_LAT = CENTER_LAT - LAT_DELTA * BUCKET_RADIUS
OUT_BOUNDS = -1
NO_COORDS = -2
MIN_BUCKET = 0
MAX_BUCKET = 2 * BUCKET_RADIUS

# Used in deprecated GetLongLat function
RADIUS_EARTH = 3959 # in miles
OUT_BOUNDS = -1
NO_COORDS = -2
BUCKETS_PER_MILE = 20
BUCKET_DIST = 50 # in miles


class Direction:
    north = 1
    south = 2
    east = 3
    west = 4

def DEPRECATED_GetLongLat(bucket_x, bucket_y, coord2=(CENTER_LONG, CENTER_LAT)):
    """Given the buckets returned by GetBucket, and a set of coordinates,
    returns the original longitude and latitude; the further the bucket is
    from the center, the more likely there will be rounding error in the
    returned longitude and latitude.

    Input:
        bucket_x: the longitude bucket
        bucket_y: the latitude bucket
        coord2: a tuple consisting of the (longitude, latitude)
    Output:
      a tuple, (longitude, latitude)
    """
    middle_bucket = BUCKET_DIST * BUCKETS_PER_MILE
    # Get direction from the center point
    dist_x = bucket_x/float(BUCKETS_PER_MILE)
    dist_y = bucket_y/float(BUCKETS_PER_MILE)
    direction = [0, 0]
    if dist_x > BUCKET_DIST:
        dist_x -= BUCKET_DIST
        direction[0] = Direction.east
    else:
        dist_x = BUCKET_DIST - dist_x
        direction[0] = Direction.west
    if dist_y > BUCKET_DIST:
        dist_y -= BUCKET_DIST
        direction[1] = Direction.north
    else:
        dist_y = BUCKET_DIST - dist_y
        direction[1] = Direction.south
    # Get longitude
    (lon2, lat2) = coord2
    lat2 *= math.pi / 180
    lon2 *= math.pi / 180
    c = dist_x/float(RADIUS_EARTH)
    b = math.tan(c/2)
    a = pow(b, 2)/(1 + pow(b,2))
    deltaLon =  2 * math.asin(math.sqrt(a / (pow(math.cos(lat2), 2))))
    if direction[0] == Direction.east:
        lon1 = lon2 + deltaLon
        lon1 /= (math.pi * 1/180)
    else:
        lon1 = lon2 - deltaLon
        lon1 /= (math.pi * 1/180)
    # Calculate latitude
    c = dist_y/float(RADIUS_EARTH)
    b = math.tan(c/2)
    a = pow(b, 2)/(1 + pow(b,2))
    deltaLat =  2 * math.sqrt(a)
    if direction[1] == Direction.north:
        lat1 = lat2 + deltaLat
        lat1 /= (math.pi * 1/180)
    else:
        lat1 = lat2 - deltaLat
        lat1 /= (math.pi * 1/180)
    return (lon1, lat1)

def GetLongLat(bucket_x, bucket_y, coord2=(BR_LONG, BR_LAT)):
    """Same as above function, just uses deltas in longitude/latitude
    rather than the haversine distance to do conversion to and from buckets."""
    lon = (0.5 + bucket_x)*LON_DELTA + BR_LONG
    lat = (0.5 + bucket_y)*LAT_DELTA + BR_LAT
    return (lon, lat)



def dist(lat1, lon1, lat2, lon2):
    """Uses haversine distance to compute the distance between two coordinates."""
    lat1 *= math.pi / 180
    lat2 *= math.pi / 180
    lon1 *= math.pi / 180
    lon2 *= math.pi / 180
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = pow(math.sin(dlat/2), 2) + math.cos(lat1) * math.cos(lat2) * pow(math.sin(dlon/2), 2) 
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
    d = RADIUS_EARTH * c
    return d


# Change in longitude
def GetDX(coord1, coord2=(CENTER_LONG, CENTER_LAT)):
    """Coordinates should be tuples consisting of floats, of the form (longitude, latitude)."""
    (lon1, lat1) = coord1
    (lon2, lat2) = coord2
    # Keep latitude fixed to get horizontal distance distance
    distance = dist(lat1, lon1, lat1, lon2)
    if lon1 > lon2:
        direction = Direction.east
    else:
        direction = Direction.west
    return (distance, direction)

def GetDY(coord1, coord2=(CENTER_LONG, CENTER_LAT)):
    """Coordinates should be tuples consisting of floats, of the form (longitude, latitude)."""
    (lon1, lat1) = coord1
    (lon2, lat2) = coord2
    # Keep latitude fixed to get horizontal distance distance
    distance = dist(lat1, lon1, lat2, lon1)
    if lat1 > lat2:
        direction = Direction.north
    else:
        direction = Direction.south
    return (distance, direction)

def DEPRECATED_GetBucket(coord1, coord2=(CENTER_LONG, CENTER_LAT)):
    """Given two pairs of coordiantes, gets the buckets for coord1 based on
    its distance from coord2. Uses haversine distance. Returns a tuple consisting
    of the longitude bucket, followed by the latitude bucket (bucket_x, bucket_y)."""
    (xdist, xdir) = GetDX(coord1, coord2)
    (ydist, ydir) = GetDY(coord1, coord2)
    bucketx = buckety = 0
    if xdist >= BUCKET_DIST or ydist >= BUCKET_DIST:
        bucketx = buckety = OUT_BOUNDS
        if (coord1[0] == 0 and coord1[1] == 0):
            bucketx = buckety = NO_COORDS
    else:
        if xdir == Direction.east:
            tempx = BUCKET_DIST + xdist
        else:
            tempx = BUCKET_DIST - xdist
        if ydir == Direction.north:
            tempy = BUCKET_DIST + ydist
        else:
            tempy = BUCKET_DIST - ydist
        bucketx = int(tempx*BUCKETS_PER_MILE)
        buckety = int(tempy*BUCKETS_PER_MILE)
    return (bucketx, buckety)

def GetBucket(coord1, coord2=(BR_LONG, BR_LAT)):
    """Same as above, but uses the latitude and longitude (rather than
    haversine distance) to calculate the buckets. """
    bucketx = buckety = 0
    if (coord1[0] == 0 and coord1[1] == 0): # This was an invalid coordinate in the original dataset
        bucketx = buckety = NO_COORDS
    else:
        bucketx = int((coord1[0]-coord2[0])/LON_DELTA)
        buckety = int((coord1[1]-coord2[1])/LAT_DELTA)
        if bucketx < MIN_BUCKET or bucketx > MAX_BUCKET or buckety < MIN_BUCKET or buckety > MAX_BUCKET:
            bucketx = buckety = OUT_BOUNDS
    return (bucketx, buckety)
