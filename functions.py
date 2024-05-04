import math

def coord_to_cartesian(latitude, longitude):
    """This function will approximately convert a latitude and longitude value to a point on the cartesian coordinate system
    
    params:
    latitude: float
        The latitude value
    longitude: float 
        The longitude value

    returns:
    x_dist: float
        The approximate distance from the origin in cartesian coordinates
    y_dist: float
        The approximate distance form the origin in cartesian coordinates
    """
    x_dist = 110.574 * latitude
    y_dist = 111.320 * math.cos(latitude * (2 * math.pi / 360)) * longitude

    return (x_dist, y_dist)