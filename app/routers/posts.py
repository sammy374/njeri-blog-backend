from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.post import Post
from pydantic import BaseModel
from jose import jwt, JWTError
from typing import Optional

router = APIRouter()

SECRET_KEY = "supersecretkey"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PostCreate(BaseModel):
    title: str
    content: str

# Token verification
def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")
    token = authorization.split(" ")[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Get all posts — public
@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

# Get one post — public
@router.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.id == post_id).first()

# Create a post — protected
@router.post("/posts", dependencies=[Depends(verify_token)])
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Update a post — protected
@router.put("/posts/{post_id}", dependencies=[Depends(verify_token)])
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    existing = db.query(Post).filter(Post.id == post_id).first()
    existing.title = post.title
    existing.content = post.content
    db.commit()
    db.refresh(existing)
    return existing

# Delete a post — protected
@router.delete("/posts/{post_id}", dependencies=[Depends(verify_token)])
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
