from sqlalchemy import Column, Integer, String, Float, Text
from app.db.database import Base

class TravelPin(Base):
    __tablename__ = "travel_pins"
    id = Column(Integer, primary_key=True)
    city = Column(String)
    country = Column(String)
    note = Column(Text, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
