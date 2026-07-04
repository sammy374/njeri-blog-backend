from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.about import About
from pydantic import BaseModel
from jose import jwt, JWTError
from typing import Optional
import os

router = APIRouter()
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")
    token = authorization.split(" ")[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

class AboutData(BaseModel):
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    email: Optional[str] = None
    favorites: Optional[str] = None

@router.get("/about")
def get_about(db: Session = Depends(get_db)):
    about = db.query(About).first()
    if not about:
        return {"bio": "", "photo_url": "", "email": "", "favorites": ""}
    return about

@router.put("/about", dependencies=[Depends(verify_token)])
def update_about(data: AboutData, db: Session = Depends(get_db)):
    about = db.query(About).first()
    if not about:
        about = About(**data.dict())
        db.add(about)
    else:
        for key, value in data.dict().items():
            setattr(about, key, value)
    db.commit()
    db.refresh(about)
    return about
