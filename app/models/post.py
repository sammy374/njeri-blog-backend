from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    category = Column(String, default="ENTRIES")
    image_url = Column(String, nullable=True)
