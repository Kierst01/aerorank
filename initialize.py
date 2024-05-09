from sqlalchemy import create_engine
from models import Base

#Initializes the engine which is used to connect to the database
engine = create_engine("sqlite:///data.db", echo = True)

#Creates the tables if they dont already exist
Base.metadata.create_all(bind=engine)


