import utm
import requests
import json
from models import Plane
import uuid
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
    
    params: data
        Dictionary: The output of get_plane_states
        
    returns: null
        """
    print('Modules Completed')
    time = data['time']
    states = data['states']
    with Session(engine) as session:
        for state in states:
            del state[12]
            id_ = str(uuid.uuid4())
            plane = Plane(id_, time, *state)
            session.add(plane)
        session.commit()

def select_states_by_bbox(max_bbox_latitude, max_bbox_longitude, min_bbox_latitude, min_bbox_longitude):
    """Given a bounding box, returns the most recent state vectors within that box whic are not 'on_ground' 
    
    params: data
    max_bbox_latitude: float
        Maximum latitude of the bounding box
    max_bbox_longitude: float
        Maximum longitude of the bounding box
    min_bbox_latitude: float
        Minimum latitude of the bounding box
    min_bbox_longitude: float
        Minimum longitude of the bounding box
        
    returns: results
        A list containing the requested Plane objects
        """
    with Session(engine) as session:
        results = list(session.scalars(select(Plane).where(
            Plane.latitude < max_bbox_latitude,
            Plane.latitude > min_bbox_latitude,
            Plane.longitude < max_bbox_longitude,
            Plane.longitude > min_bbox_longitude,
            Plane.on_ground == False)))
        
        return (results)