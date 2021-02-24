import math
import random

class RandomCoord:
  def __init__(self, lng, lat):
    self.lng = lng
    self.lat = lat

  def randomize_coords(self):
    #Earth’s radius, sphere
    R=6378137

    # offsets in meters
    dn = random.randint(5,25)
    de = random.randint(5,25)

    #Coordinate offsets in radians
    dLat = dn/R
    dLng = de/(R*math.cos(math.pi*self.lat/180))

    #OffsetPosition, decimal degrees
    latO = self.lat + dLat * 180/math.pi
    lngO = self.lng + dLng * 180/math.pi

    self.lng=lngO
    self.lat=latO
    return self
