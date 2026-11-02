from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from jose import jwt, JWTError
from typing import Optional
import httpx
import os
import uuid

router = APIRouter()

SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
BUCKET = "blog-images"
MAX_SIZE = 5 * 1024 * 1024  # 5 MB

EXTENSIONS = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
}

def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")
    token = authorization.split(" ")[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/upload", dependencies=[Depends(verify_token)])
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, WEBP or GIF images")

    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Image is too big (max 5 MB)")

    name = f"{uuid.uuid4().hex}.{EXTENSIONS[file.content_type]}"

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{name}",
            headers={
                "apikey": SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
                "Content-Type": file.content_type,
            },
            content=data,
        )

    if res.status_code not in (200, 201):
        raise HTTPException(status_code=500, detail="Upload to storage failed")

    return {"url": f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{name}"}
