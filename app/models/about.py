from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class About(Base):
    __tablename__ = "about"
    id = Column(Integer, primary_key=True)
    bio = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
    favorites = Column(Text, nullable=True)
