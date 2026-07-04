from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Social(Base):
    __tablename__ = "social"
    id = Column(Integer, primary_key=True)
    instagram = Column(String, nullable=True)
    tiktok = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
