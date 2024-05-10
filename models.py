from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Creates a "Base" class that inherits from DeclarativeBase class
class Base(DeclarativeBase):
    pass

#Any model we want to make (structure of database table), inherits from our created "Base" class
class Plane(Base):
    __tablename__ = "plane_states"

    id_:Mapped[str] = mapped_column(primary_key = True)
    time:Mapped[int]
    icao24:Mapped[str]
    callsign:Mapped[str] = mapped_column(nullable=True)
    origin_country:Mapped[str]
    time_position:Mapped[int] = mapped_column(nullable=True)
    last_contact:Mapped[int]
    longitude:Mapped[float] = mapped_column(nullable=True)
    latitude:Mapped[float] = mapped_column(nullable=True)
    baro_altitude:Mapped[float] = mapped_column(nullable=True)
    on_ground:Mapped[bool]
    velocity:Mapped[float] = mapped_column(nullable=True)
    true_track:Mapped[float] = mapped_column(nullable=True)
    vertical_rate:Mapped[float] = mapped_column(nullable=True)
    geo_altitude:Mapped[float] = mapped_column(nullable=True)
    squawk:Mapped[str] = mapped_column(nullable=True)
    spi:Mapped[bool]
    position_source:Mapped[int]

    def __init__(self,id_:str, time:int, icao24:str,callsign:str, origin_country:str, time_position:int, last_contact:int, longitude:float, latitude:float, baro_altitude:float, on_ground:bool, velocity:float, true_track:float, vertical_rate:float, geo_altitude:float, squawk:str, spi:bool, position_source:int):
        self.id_ = id_
        self.time = time
        self.icao24 = icao24
        self.callsign = callsign
        self.origin_country = origin_country
        self.time_position = time_position
        self.last_contact = last_contact
        self.longitude = longitude
        self.latitude = latitude
        self.baro_altitude = baro_altitude
        self.on_ground = on_ground
        self.velocity = velocity
        self.true_track = true_track
        self.vertical_rate = vertical_rate
        self.geo_altitude = geo_altitude
        self.squawk = squawk
        self.spi = spi
        self.position_source = position_source

    def __repr__(self):
        return f'Time: {self.time_position}, Icao24: {self.icao24}, Callsign:{self.callsign}, Latitude{self.latitude}, Longitude: {self.longitude}, On Ground: {self.on_ground}, Velocity: {self.velocity}: True Track: {self.true_track}'