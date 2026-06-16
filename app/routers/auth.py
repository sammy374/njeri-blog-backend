from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
import os

router = APIRouter()

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "njeri")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "njeri1234")
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")

class LoginData(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginData):
    if data.username != ADMIN_USERNAME or data.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode(
        {"sub": data.username, "exp": datetime.utcnow() + timedelta(days=7)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"token": token}
