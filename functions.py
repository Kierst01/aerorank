import utm, requests, json, uuid, math
from models import Plane, Time
from sqlalchemy import select
from sqlalchemy.orm import Session
from initialize import engine

def get_bounding_box (user_latitude, user_longitude, search_distance_meters):
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

def get_plane_states ():
    """Returns a dictionary containing the time and states of all known active aircraft
    
    params: null
        
    returns:
    data: dict
        Dictionary containing the requested time and states
        """

    url = f"https://opensky-network.org/api/states/all"
    #?lamin={min_bbox_latitude}&lomin={min_bbox_longitude}&lamax={max_bbox_latitude}&lomax={max_bbox_longitude}

    payload = {}
    headers = {
    'Authorization': 'Basic SkdpbGJlcmc6S29kYWsyMjA5',
    'Cookie': 'XSRF-TOKEN=7b7b99c3-c8f5-420d-a941-1560c7423dc9'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    return (data)

def insert_states(data):
    """Given open sky api response data, inserts the states into the data.db plane_states table
    
    params: 
    data: dict
        A dictionary containing the output of get_plane_states
        
    returns: null
        """
    print(data)
    time = data['time']
    states = data['states']
    if (states == None): return

    with Session(engine) as session:
        session.add(Time(time))
        for state in states:
            del state[12]
            id_ = str(uuid.uuid4())
            plane = Plane(id_, time, *state)
            session.add(plane)
        session.commit()

def select_states(max_bbox_latitude, max_bbox_longitude, min_bbox_latitude, min_bbox_longitude, time):
    """Given a bounding box, and a timestamp for which plane_states exists, returns the state vectors with that timestamp, within the box, and which are not 'on_ground'
    
    params:
    max_bbox_latitude: float
        Maximum latitude of the bounding box
    max_bbox_longitude: float
        Maximum longitude of the bounding box
    min_bbox_latitude: float
        Minimum latitude of the bounding box
    min_bbox_longitude: float
        Minimum longitude of the bounding box
    time: int
        The UNIX timestamp for which the states ar
        
    returns: 
    results: list
        A list containing the requested Plane objects
        """
    with Session(engine) as session:
        results = list(session.scalars(select(Plane).where(
            Plane.latitude < max_bbox_latitude,
            Plane.latitude > min_bbox_latitude,
            Plane.longitude < max_bbox_longitude,
            Plane.longitude > min_bbox_longitude,
            Plane.on_ground == False,
            Plane.time == time)))
        
        return (results)
    
def select_most_recent_time ():
     """Selects the most recent time in the 'requested_times' table
    
    params: null
        
    returns: 
    most_recent_time: int
        the most recent time in the 'requested_times' table
        """
     with Session(engine) as session:
         results = list(session.scalars(select(Time.time)))
         most_recent_time = max(results)
         return most_recent_time

def check_collision(user_lat, user_lon, plane_lat, plane_lon, plane_alt, plane_vel, plane_true_track, intersection_radius=10000):  
    """Given information about a user and planes position and velocity, returns whether the plane will intersect with the user
    
    params:
    user_lat: float
        The users latitude in degrees
    user_lon: float
        The users longitude in degrees
    plane_lat: float
        The planes latitude in degrees
    plane_lon: float
        The planes longitude in degrees
    plane_alt: float
        The planes altitude in m
    plane_vel: float
        The planes ground velocity in m/s
    plane_true_track: float
        The planes true track angle in degrees
    intersection_radius: float
        The radius in meters for which the lane will be considered to intersect with the users location
        
    returns: 
    min_time: float
        The time until the two plane is at its closest point to the user (negative indicates it is past the closest point)
    min_dist: float
        The distance at which the plane is closest point to the user 
    intersects: bool
        Whether or not the plane will intersect with the users location, whether in the past or future.
        """

    user_utm_x, user_utm_y, zone_num, zone_letter = utm.from_latlon(user_lat, user_lon)

    plane_utm_x, plane_utm_y, _, _ = utm.from_latlon(plane_lat, plane_lon, zone_num, zone_letter)

    angle = -(plane_true_track - 90)

    plane_vel_x = plane_vel * math.cos(math.radians(angle))
    plane_vel_y = plane_vel * math.sin(math.radians(angle))

    min_time = - ( - (user_utm_x - plane_utm_x) * plane_vel_x - (user_utm_y - plane_utm_y) * plane_vel_y) / ((plane_vel_x ** 2) + (plane_vel_y ** 2))

    min_dist = math.sqrt(
        ( - min_time * plane_vel_x + user_utm_x - plane_utm_x) ** 2 + 
        ( - min_time * plane_vel_y + user_utm_y - plane_utm_y) ** 2
        )
    
    intersects = min_dist < intersection_radius

    return (min_time, min_dist, intersects)

