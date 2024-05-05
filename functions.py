import math

def coord_to_cartesian(latitude, longitude):
    """This function will approximately convert a latitude and longitude value to a point on a cartesian coordinate system in units of kilometers
    
    params:
    latitude: float
        The latitude value
    longitude: float 
        The longitude value

    returns:
    x_dist: float
        The approximate distance in kilometers from the origin in cartesian coordinates
    y_dist: float
        The approximate distance in kilometers from the origin in cartesian coordinates
    """
    x_dist = 110.574 * latitude
    y_dist = 111.320 * math.cos(latitude * (2 * math.pi / 360)) * longitude

    return (x_dist, y_dist)


def cartesian_to_coord(x_dist, y_dist):
    """This function will approximately convert from a cartesian coordinate system in units of kilometers to latitude and longitude
    
    params:
    x_dist: float
        The approximate distance from the origin in cartesian coordinates
    y_dist: float
        The approximate distance form the origin in cartesian coordinates

    returns:
    latitude: float
        The latitude value
    longitude: float 
        The longitude value
    """
    latitude = x_dist / 110.574
    longitude = y_dist / 111.320 / math.cos(latitude * (2 * math.pi / 360))

    return (latitude, longitude)
