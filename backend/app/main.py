from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import engine, Base, SessionLocal
from .api import auth, users, categories, groups, events, chats, saved_searches, search_history, meetup_sync
from .seed_data import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Seed database if needed (DISABLED - using real Meetup API data)
    # try:
    #     seed_database()
    # except Exception as e:
    #     print(f"Database seeding skipped or failed: {e}")

    yield
    # Cleanup on shutdown (if needed)


app = FastAPI(
    title="Meetup Clone API",
    description="Backend API for Meetup clone application",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:10002",
        "http://frontend:3000",
        "http://localhost",
        "http://frontend"
    ],
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
app.include_router(chats.router, prefix="/api")
app.include_router(saved_searches.router, prefix="/api")
app.include_router(search_history.router, prefix="/api")
app.include_router(meetup_sync.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to Meetup Clone API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
