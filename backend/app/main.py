from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import auth, users, categories, groups, events

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Meetup Clone API",
    description="Backend API for Meetup clone application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(groups.router, prefix="/api")
app.include_router(events.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to Meetup Clone API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
