# Meetup.com API Integration

This document explains how to use the Meetup API integration to fetch real event data.

## Setup

### 1. Get Your Meetup API Key

1. Go to https://www.meetup.com/api/authentication/
2. Sign in to your Meetup account
3. Create an OAuth consumer (requires Meetup Pro subscription)
4. Get your OAuth access token

### 2. Configure the API Key

Add your Meetup API key to the backend configuration:

**Option A: Using .env file (Recommended)**
```bash
cd backend
echo "MEETUP_API_KEY=your-actual-api-key-here" >> .env
```

**Option B: Using Docker Compose**
Edit `docker-compose.yml` and update line 34:
```yaml
- MEETUP_API_KEY=your-actual-api-key-here
```

### 3. Restart Backend

If using Docker:
```bash
docker-compose restart backend
```

## Usage

### Method 1: Using the CLI Script (Recommended for Initial Import)

The CLI script provides a simple way to import events from Meetup:

```bash
cd backend

# Import technology events
python sync_meetup_events.py --keyword "technology" --limit 50

# Import yoga events in San Francisco
python sync_meetup_events.py --keyword "yoga" --location "San Francisco, CA" --limit 30

# Import sports events
python sync_meetup_events.py --keyword "sports" --limit 20
```

**Arguments:**
- `--keyword` (required): Search term (e.g., "technology", "yoga", "hiking")
- `--location` (optional): City or location (e.g., "San Francisco, CA")
- `--limit` (optional): Max events to fetch (default: 20, max: 100)

**Example Output:**
```
============================================================
Meetup Event Sync Tool
============================================================
Using user: sarah.johnson@example.com as event organizer

Searching Meetup for: 'technology'
Fetching up to 50 events...
✓ Found 50 events from Meetup

[1/50] Processing: Tech Talks: AI & Machine Learning...
  → Creating group: SF Tech Community
  → Geocoding location...
    Coordinates: 37.7749, -122.4194
  ✓ Imported successfully

[2/50] Processing: Startup Networking Event...
  ⊘ Skipped (already exists)

...

============================================================
Sync completed!
  ✓ Imported: 45
  ⊘ Skipped:  3
  ✗ Errors:   2
============================================================
```

### Method 2: Using the API Endpoint

You can also import events via the REST API:

**Test Connection:**
```bash
curl http://localhost:8000/api/meetup-sync/test-connection \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Import Events:**
```bash
curl -X POST http://localhost:8000/api/meetup-sync/search-and-import \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "technology",
    "location": "San Francisco",
    "limit": 50,
    "create_group_if_missing": true
  }'
```

**Response:**
```json
{
  "success": true,
  "imported_count": 45,
  "skipped_count": 3,
  "error_count": 2,
  "errors": [
    "Error importing event 'Example': Missing required field"
  ]
}
```

### Method 3: Import by Location (Latitude/Longitude)

```bash
curl -X POST "http://localhost:8000/api/meetup-sync/import-by-location?latitude=37.7749&longitude=-122.4194&radius=50&limit=30" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## What Gets Imported

For each Meetup event, the following data is imported:

- **Basic Info**: Title, description, date, time
- **Location**: Address, city, coordinates (auto-geocoded if missing)
- **Event Type**: Online, in-person, or hybrid
- **Category**: Mapped from Meetup topics to our categories
- **Attendance**: Current attendee count, max capacity
- **Group**: Meetup group name (creates group if doesn't exist)
- **Media**: Featured event photo
- **Metadata**: Meetup URL, Meetup ID (stored in description)

## Category Mapping

Meetup topics are automatically mapped to our categories:

| Meetup Topic | Our Category |
|-------------|--------------|
| Technology, Tech | Technology |
| Sports, Fitness | Sports & Fitness |
| Arts, Culture | Arts & Culture |
| Food | Food & Drink |
| Business, Career | Business & Professional |
| Education | Learning & Education |
| Music | Music |
| Health, Wellness | Health & Wellness |
| Outdoors, Adventure | Outdoors & Adventure |

## Features

✅ **Auto-Geocoding**: Addresses are automatically converted to coordinates for map display
✅ **Duplicate Detection**: Events are checked to avoid importing duplicates
✅ **Group Creation**: Meetup groups are automatically created in your database
✅ **Error Handling**: Failed imports are logged, successful ones continue
✅ **Batch Import**: Import multiple events in one operation
✅ **Metadata Preservation**: Meetup URL and ID are preserved for reference

## Troubleshooting

### "MEETUP_API_KEY is not configured"

Make sure you've added your API key to `.env` or `docker-compose.yml` and restarted the backend.

### "No events found on Meetup"

- Check that your API key is valid
- Try a different keyword or location
- Verify your Meetup API key has proper permissions

### "Connected to Meetup API but no events found"

Your API key might not have permission to search events. Check your Meetup API settings.

### Events Import But Don't Show on Map

Make sure:
1. Google Maps API key is configured
2. Event has a valid address
3. Geocoding succeeded (check logs)

## API Documentation

Full API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Look for the "Meetup Sync" section.

## Rate Limits

Be mindful of Meetup API rate limits:
- Start with small limits (20-50 events)
- Don't run sync too frequently
- Use the CLI script for large imports

## Example Workflows

### Initial Setup - Import Diverse Events

```bash
# Import tech events
python sync_meetup_events.py --keyword "technology" --limit 50

# Import sports events
python sync_meetup_events.py --keyword "sports" --limit 30

# Import arts events
python sync_meetup_events.py --keyword "arts" --limit 30

# Import yoga/wellness events
python sync_meetup_events.py --keyword "yoga" --limit 20
```

### Location-Specific Import

```bash
# San Francisco events
python sync_meetup_events.py --keyword "networking" --location "San Francisco, CA" --limit 40

# New York events
python sync_meetup_events.py --keyword "tech meetup" --location "New York, NY" --limit 40
```

### Regular Updates (Cron Job)

Add to your crontab to sync daily:
```bash
# Sync tech events every day at 2 AM
0 2 * * * cd /path/to/backend && python sync_meetup_events.py --keyword "technology" --limit 20
```

## Next Steps

After importing events:
1. Check the frontend - events should appear on the "Find Events" page
2. Search for events using the filters
3. View events on the map (if geocoded successfully)
4. Users can RSVP, save searches, and view event details

## Support

For issues with:
- Meetup API: https://www.meetup.com/api/
- This integration: Check backend logs with `docker-compose logs backend`
