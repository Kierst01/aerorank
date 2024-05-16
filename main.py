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
bbox = fns.get_bounding_box(49.248866, -123.173949, 150000)
time = fns.select_most_recent_time()
results = fns.select_states(*bbox, time)
for result in results:
    min_time, min_dist, intersects = fns.check_collision(user_coords[0], user_coords[1], result.latitude, result.longitude, result.baro_altitude, result.velocity, result.true_track)
    print(result.callsign, min_time, min_dist, intersects)
