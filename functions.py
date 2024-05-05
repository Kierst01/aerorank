import math
import utm

def get_bounding_box(user_latitude, user_longitude, search_distance_meters):
    """Given a users latitude, longitude, and desired search distance, returns a rectangular lat/lon bounding box surrounding the user
    
    params:
    user_latitude: float
        The users latitude
    user_longitude: float
        The users longitude
    search_distance: int
        The users desired search distance in meters
        
    returns:
    max_bbox_latitude: float
        Maximum latitude of the bounding box
    max_bbox_longitude: float
        Maximum longitude of the bounding box
    min_bbox_latitude: float
        Minimum latitude of the bounding box
    min_bbox_longitude: float
        Minimum longitude of the bounding box
        """
    
    user_utm_x, user_utm_y, zone_num, zone_letter = utm.from_latlon(user_latitude, user_longitude)

    utm_bbox_x_max = user_utm_x + search_distance_meters
    utm_bbox_y_max = user_utm_y + search_distance_meters
    utm_bbox_x_min = user_utm_x - search_distance_meters
    utm_bbox_y_min = user_utm_y - search_distance_meters
    
    max_bbox_latitude, max_bbox_longitude = utm.to_latlon(utm_bbox_x_max, utm_bbox_y_max, zone_num, zone_letter)
    min_bbox_latitude, min_bbox_longitude = utm.to_latlon(utm_bbox_x_min, utm_bbox_y_min, zone_num, zone_letter)

    return (max_bbox_latitude, max_bbox_longitude, min_bbox_latitude, min_bbox_longitude)
