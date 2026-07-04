from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.travel import TravelPin
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

class PinData(BaseModel):
    city: str
    country: str
    note: Optional[str] = None
    latitude: float
    longitude: float

@router.get("/travel")
def get_pins(db: Session = Depends(get_db)):
    return db.query(TravelPin).all()

@router.post("/travel", dependencies=[Depends(verify_token)])
def add_pin(data: PinData, db: Session = Depends(get_db)):
    pin = TravelPin(**data.dict())
    db.add(pin)
    db.commit()
    db.refresh(pin)
    return pin

@router.delete("/travel/{pin_id}", dependencies=[Depends(verify_token)])
def delete_pin(pin_id: int, db: Session = Depends(get_db)):
    pin = db.query(TravelPin).filter(TravelPin.id == pin_id).first()
    db.delete(pin)
    db.commit()
    return {"message": "Pin deleted"}
