from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.db.database import engine, Base
from app.models.post import Post
from app.models.about import About
from app.models.social import Social
from app.models.travel import TravelPin
from app.routers import posts, auth, about, social, travel

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://njeri-blog-m5n6-mauve.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(about.router)
app.include_router(social.router)
app.include_router(travel.router)

@app.get("/")
def home():
    return {"message": "Backend is working 🚀"}

Base.metadata.create_all(bind=engine)
