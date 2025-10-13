# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack Meetup.com clone with a FastAPI backend, PostgreSQL database, and React frontend. The application supports event discovery, user profiles, group management, and JWT authentication.

## Architecture

### Tech Stack
- **Backend**: FastAPI (synchronous), SQLAlchemy ORM, PostgreSQL, JWT authentication
- **Frontend**: React 18, React Router v6, Vite, CSS Modules
- **Infrastructure**: Docker Compose for orchestration

### Service Ports
- **Frontend**: `localhost:10002` (Docker) or `localhost:3000` (local dev)
- **Backend API**: `localhost:10001` (Docker) or `localhost:8000` (local dev)
- **PostgreSQL**: `localhost:10000` (exposed from Docker)

### Data Flow
Frontend → Backend API (`/api/*` endpoints) → PostgreSQL. Backend uses synchronous SQLAlchemy ORM with Pydantic schemas for validation. Authentication via JWT tokens stored client-side.

## Common Commands

### Docker (Recommended)
```bash
# Start all services (postgres, backend, frontend)
docker-compose up

# Start with rebuild
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service-name]
```

### Backend Development
```bash
cd backend

# Local setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run backend (local)
uvicorn app.main:app --reload

# Seed database
python -m app.seed_data

# API docs available at:
# http://localhost:8000/docs (Swagger)
# http://localhost:8000/redoc
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# Lint code
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

## Backend Architecture

### Models & Relationships (SQLAlchemy)
- **User** → many Groups (organized_groups), many Events (organized_events)
- **Group** → many Events, many Users (members via group_members)
- **Event** → one Group, one User (organizer), many Users (attendees via event_attendees)
- **Category** → many Users (interested_users via user_interests)

Association tables: `user_interests`, `event_attendees`, `group_members`

### API Structure
All endpoints prefixed with `/api`:
- **auth.py** - `/api/auth/*` - signup, login, me
- **users.py** - `/api/users/*` - CRUD, user events/groups
- **groups.py** - `/api/groups/*` - CRUD, join, members, events
- **events.py** - `/api/events/*` - CRUD, attend, attendees, search filters
- **categories.py** - `/api/categories` - list categories

### Authentication
JWT tokens via `app.core.security`. Use `get_current_user` dependency from `app.core.dependencies` for protected routes. Test credentials: `test1@example.com` / `password123`.

### Database
SQLAlchemy with PostgreSQL. Connection managed in `app.database.py`. Tables auto-created via `Base.metadata.create_all()` in `main.py`. Seed data via `app.seed_data.py`.

## Frontend Architecture

### Routing
React Router v6 in `App.jsx`:
- `/` - Home page
- `/find` - Event search with filters
- `/events/:id` - Event details
- `/members/:id` - User profile
- `/groups/:id` - Group details

### Components
Reusable UI components in `src/components/`:
- **Header.jsx**, **Footer.jsx** - Layout
- **EventCard.jsx**, **UserCard.jsx**, **GroupCard.jsx** - Display cards
- **SearchBar.jsx**, **Filters.jsx** - Search/filter UI

### Mock Data (Frontend only currently)
Static data in `src/data/`: `categories.js`, `events.js`, `users.js`, `groups.js`. Used for frontend development before backend integration.

## Database Schema

### Key Tables
- **users**: email, password_hash, name, bio, location, avatar, member_since
- **groups**: name, description, category, location, members_count, organizer_id, founded
- **events**: title, description, date, time, group_id, organizer_id, location, location_city, attendees_count, max_attendees, price, is_online, category
- **categories**: name, icon, color

### Cascading Deletes
- Deleting user → deletes their organized groups/events, removes from attendees/members
- Deleting group → deletes all associated events
- Deleting event → removes from attendees list

## Configuration

### Backend Environment Variables
Required in `backend/.env`:
```
DATABASE_URL=postgresql://meetup_user:meetup_password@postgres:5432/meetup_db
SECRET_KEY=<jwt-secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Docker Compose Configuration
Services defined in `docker-compose.yml`. Note: Backend uses volumes line 27-28 as both volumes AND environment variables (incorrect syntax but functional). Postgres uses healthcheck to ensure database ready before backend starts.

## Development Notes

### Backend
- Uses **synchronous** FastAPI (no async/await in route handlers)
- SQLAlchemy ORM with session management via `get_db()` dependency
- Pydantic schemas for request/response validation (separate from SQLAlchemy models)
- Password hashing with bcrypt via passlib
- JWT tokens with python-jose

### Frontend
- Vite dev server configured for `host: 0.0.0.0` and `port: 3001` in `vite.config.js`
- CSS Modules for component styling (scoped)
- Currently using mock data; API integration in progress
- Images from Unsplash, avatars from Pravatar

### Port Discrepancy
Frontend vite.config.js specifies port 3001, but docker-compose exposes 10002→3000. Frontend README says port 3000. Likely docker-compose overrides vite config.
