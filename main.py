# MODULES
from sqlalchemy.orm import Session
import functions as fns

#SETUP
# Hardcoded coordinates for now
user_coords = (49.248866, -123.173949)
search_distance_meters = 150000

#UPDATE STATES TABLE
data = fns.get_plane_states()
fns.insert_states(data)

#SELECT STATES
bbox = fns.get_bounding_box(49, -123, 150000)
results = fns.select_states_by_bbox(*bbox)