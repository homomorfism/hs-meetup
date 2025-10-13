# Meetup Clone - Frontend Application

A full-featured frontend clone of Meetup.com built with React, featuring event discovery, user profiles, and group management.

## Features

### Pages
- **Home Page** - Hero section, category browse, upcoming events
- **Find Events** - Search and filter events by location, category, date, format, and price
- **Event Details** - Full event information with attendees, organizer, and similar events
- **User Profile** - User information, organized groups and events
- **Group Details** - Group information with upcoming/past events and members

### Components
- Event cards with images and metadata
- User cards with interests
- Group cards with member counts
- Search bar with location and keyword filters
- Advanced filtering sidebar
- Responsive header and footer

### Mock Data
- 50+ events across various categories
- 20+ user profiles
- 15+ groups
- 12 event categories

## Tech Stack

- **React 18** - UI framework
- **React Router v6** - Client-side routing
- **Vite** - Build tool and dev server
- **CSS Modules** - Component-scoped styling
- **Docker** - Containerization

## Getting Started

### Prerequisites
- Docker and Docker Compose
- OR Node.js 20+ and npm

### Running with Docker (Recommended)

1. Clone the repository and navigate to project directory:
```bash
cd hs-meetup
```

2. Start the application:
```bash
docker-compose up
```

3. Open your browser and navigate to:
```
http://localhost:3000
```

The application will run with hot-reload enabled.

### Running without Docker

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to:
```
http://localhost:3000
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── EventCard.jsx
│   │   ├── UserCard.jsx
│   │   ├── GroupCard.jsx
│   │   ├── SearchBar.jsx
│   │   └── Filters.jsx
│   ├── pages/               # Page components
│   │   ├── Home.jsx
│   │   ├── FindEvents.jsx
│   │   ├── EventDetails.jsx
│   │   ├── UserProfile.jsx
│   │   └── GroupDetails.jsx
│   ├── data/                # Mock data
│   │   ├── categories.js
│   │   ├── events.js
│   │   ├── users.js
│   │   ├── groups.js
│   │   └── index.js
│   ├── App.jsx              # Main app component with routing
│   ├── App.css              # Global styles
│   └── main.jsx             # Entry point
├── public/                  # Static assets
├── Dockerfile               # Docker configuration
└── package.json
```

## Available Routes

- `/` - Home page
- `/find` - Event search page
- `/events/:id` - Event details page
- `/members/:id` - User profile page
- `/groups/:id` - Group details page

## Features Overview

### Search & Discovery
- Keyword search for events
- Location-based filtering
- Category filtering (Technology, Arts, Sports, etc.)
- Date range filters
- Online/In-person event filtering
- Free/Paid event filtering

### Event Management
- View event details with full descriptions
- See attendee lists
- View organizer and group information
- Discover similar events

### User Profiles
- View user information and bio
- See user's interests
- Browse organized groups and events

### Groups
- View group details and descriptions
- Browse upcoming and past events
- See member lists
- View group organizer information

## Mock Data

The application uses realistic mock data including:
- Events with images from Unsplash
- User avatars from Pravatar
- Various event categories and formats
- Multiple cities and locations
- Different price points (free and paid events)

## Development

### Building for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Docker Commands

### Build and start containers
```bash
docker-compose up --build
```

### Stop containers
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT License

## Acknowledgments

- Images provided by Unsplash
- Avatars provided by Pravatar
- Inspired by Meetup.com
