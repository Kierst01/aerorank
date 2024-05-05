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

def get_bounding_box(user_latitude, user_longitude, search_distance):
    """Given a users latitude, longitude, and desired search distance, returns a rectangular lat/lon bounding box surrounding the user
    
    params:
    user_latitude: float
        The users latitude
    user_longitude: float
        The users longitude
    search_distance: int
        The users desired search distance
        
    returns:
    max_latitude: float
        Maximum latitude of the bounding box
    max_longitude: float
        Maximum longitude of the bounding box
    min_latitude: float
        Minimum latitude of the bounding box
    min_longitude: float
        Minimum longitude of the bounding box
        """
    user_cartesian = (coord_to_cartesian(user_latitude, user_longitude))

    max_x, max_y = user_cartesian[0] + search_distance, user_cartesian[1] + search_distance
    min_x, min_y = user_cartesian[0] - search_distance, user_cartesian[1] - search_distance

    max_coords = cartesian_to_coord(max_x, max_y)
    min_coords = cartesian_to_coord(min_x, min_y)


    return (max_coords[0], max_coords[1], min_coords[0], min_coords[1])




