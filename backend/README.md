# Meetup Clone - Backend API

FastAPI backend with PostgreSQL database for the Meetup clone application.

## Features

- **JWT Authentication** - Secure login/signup with password hashing
- **RESTful API** - Full CRUD operations for users, events, groups
- **PostgreSQL Database** - Relational database with SQLAlchemy ORM
- **Auto Documentation** - Interactive API docs with Swagger UI
- **CORS Enabled** - Configured for frontend integration
- **Database Seeding** - Automatic population with test data

## Tech Stack

- **FastAPI** - Modern Python web framework (synchronous)
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **JWT** - Token-based authentication
- **Bcrypt** - Password hashing
- **Uvicorn** - ASGI server

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login (returns JWT token)
- `GET /api/auth/me` - Get current user profile

### Users
- `GET /api/users` - List all users
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user (auth required)
- `GET /api/users/{id}/events` - Get user's events
- `GET /api/users/{id}/groups` - Get user's groups

### Categories
- `GET /api/categories` - List all categories

### Groups
- `GET /api/groups` - List groups (with filters)
- `GET /api/groups/{id}` - Get group details
- `POST /api/groups` - Create group (auth required)
- `PUT /api/groups/{id}` - Update group (auth required)
- `POST /api/groups/{id}/join` - Join group (auth required)
- `GET /api/groups/{id}/events` - Get group events
- `GET /api/groups/{id}/members` - Get group members

### Events
- `GET /api/events` - List events (with filters: keyword, location, category, isOnline, price)
- `GET /api/events/{id}` - Get event details
- `POST /api/events` - Create event (auth required)
- `PUT /api/events/{id}` - Update event (auth required)
- `POST /api/events/{id}/attend` - Attend event (auth required)
- `GET /api/events/{id}/attendees` - Get event attendees

## Running with Docker

The easiest way to run the backend is with Docker Compose from the project root:

```bash
cd /path/to/hs-meetup
docker-compose up
```

This will start:
- **PostgreSQL** on port 5432
- **Backend API** on port 8000
- **Frontend** on port 3000

The database will be automatically seeded with test data on first run.

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Test User Credentials

The database is seeded with test users:

```text
Email: sarah.johnson@example.com | Password: password123
Email: michael.chen@example.com | Password: password123
Email: emily.rodriguez@example.com | Password: password123
```

All other users also have password: `password123`

## Running Locally (Without Docker)

1. Install PostgreSQL and create a database:
```bash
createdb meetup_db
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/meetup_db"
export SECRET_KEY="your-secret-key"
```

5. Seed the database:
```bash
python -m app.seed_data
```

6. Run the server:
```bash
uvicorn app.main:app --reload
```

## Database Schema

### Tables
- **users** - User profiles with authentication
- **categories** - Event categories
- **groups** - Meetup groups
- **events** - Meetup events
- **user_interests** - Many-to-many: users ↔ categories
- **event_attendees** - Many-to-many: users ↔ events
- **group_members** - Many-to-many: users ↔ groups

## Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://meetup_user:meetup_password@postgres:10000/meetup_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Development

The API uses:
- **Synchronous** FastAPI (no async/await)
- **SQLAlchemy** ORM for database operations
- **Pydantic** for request/response validation
- **JWT tokens** for authentication
- **Bcrypt** for password hashing

## Project Structure

```
backend/
├── app/
│   ├── api/              # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── users.py      # User endpoints
│   │   ├── categories.py # Category endpoints
│   │   ├── groups.py     # Group endpoints
│   │   └── events.py     # Event endpoints
│   ├── core/             # Core functionality
│   │   ├── security.py   # Password hashing, JWT
│   │   └── dependencies.py # Auth dependencies
│   ├── models/           # SQLAlchemy models
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── group.py
│   │   └── event.py
│   ├── schemas/          # Pydantic schemas
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── group.py
│   │   └── event.py
│   ├── config.py         # Configuration
│   ├── database.py       # Database connection
│   ├── main.py           # FastAPI app
│   └── seed_data.py      # Database seeding script
├── Dockerfile
├── requirements.txt
└── .env.example
```

## License

MIT License
