from models import Plane
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from initialize import engine

def insert_states(time, states):
    with Session(engine) as session:
        for state in states:
            del state[12]
            id_ = str(uuid.uuid4())
            plane = Plane(id_, time, *state)
            session.add(plane)
        session.commit()

def get_recent_states_by_bbox(max_bbox_latitude, max_bbox_longitude, min_bbox_latitude, min_bbox_longitude):
    with Session(engine) as session:
        results = session.scalars(select(Plane).where(
            Plane.latitude < max_bbox_latitude,
            Plane.latitude > min_bbox_latitude,
            Plane.longitude < max_bbox_longitude,
            Plane.longitude > min_bbox_longitude,
            Plane.on_ground == False))
        
        return (list(results))
