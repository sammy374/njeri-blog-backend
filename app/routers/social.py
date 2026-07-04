from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.social import Social
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

class SocialData(BaseModel):
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    twitter: Optional[str] = None

@router.get("/social")
def get_social(db: Session = Depends(get_db)):
    social = db.query(Social).first()
    if not social:
        return {"instagram": "", "tiktok": "", "twitter": ""}
    return social

@router.put("/social", dependencies=[Depends(verify_token)])
def update_social(data: SocialData, db: Session = Depends(get_db)):
    social = db.query(Social).first()
    if not social:
        social = Social(**data.dict())
        db.add(social)
    else:
        for key, value in data.dict().items():
            setattr(social, key, value)
    db.commit()
    db.refresh(social)
    return social
