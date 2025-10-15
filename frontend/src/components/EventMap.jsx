import { APIProvider, Map, AdvancedMarker, InfoWindow, Pin } from '@vis.gl/react-google-maps';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './EventMap.module.css';

// Google Maps API Key - should be set in environment variable
const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '';

export default function EventMap({ events, center, zoom = 10, height = '500px' }) {
  const [selectedEvent, setSelectedEvent] = useState(null);
  const navigate = useNavigate();

  // Filter events that have valid coordinates
  const eventsWithCoords = events.filter(
    event => event.latitude && event.longitude && !event.is_online
  );

  // Calculate center if not provided
  const mapCenter = center || (eventsWithCoords.length > 0
    ? {
        lat: eventsWithCoords.reduce((sum, e) => sum + e.latitude, 0) / eventsWithCoords.length,
        lng: eventsWithCoords.reduce((sum, e) => sum + e.longitude, 0) / eventsWithCoords.length
      }
    : { lat: 37.7749, lng: -122.4194 }); // Default to SF

  // If no API key, show message
  if (!GOOGLE_MAPS_API_KEY) {
    return (
      <div className={styles.noApiKey} style={{ height }}>
        <p>Google Maps API key not configured</p>
        <p>Add VITE_GOOGLE_MAPS_API_KEY to your .env file</p>
      </div>
    );
  }

  // If no events with coordinates
  if (eventsWithCoords.length === 0) {
    return (
      <div className={styles.noEvents} style={{ height }}>
        <p>No events with location data to display</p>
      </div>
    );
  }

  const handleMarkerClick = (event) => {
    setSelectedEvent(event);
  };

  const handleInfoWindowClose = () => {
    setSelectedEvent(null);
  };

  const handleViewEvent = (eventId) => {
    navigate(`/events/${eventId}`);
  };

  return (
    <div className={styles.mapContainer} style={{ height }}>
      <APIProvider apiKey={GOOGLE_MAPS_API_KEY}>
        <Map
          mapId={'event-map'}
          defaultCenter={mapCenter}
          defaultZoom={zoom}
          gestureHandling={'greedy'}
          disableDefaultUI={false}
        >
          {eventsWithCoords.map((event) => (
            <AdvancedMarker
              key={event.id}
              position={{ lat: event.latitude, lng: event.longitude }}
              onClick={() => handleMarkerClick(event)}
            >
              <Pin
                background={'#ea4335'}
                borderColor={'#c5221f'}
                glyphColor={'#fff'}
              />
            </AdvancedMarker>
          ))}

          {selectedEvent && (
            <InfoWindow
              position={{ lat: selectedEvent.latitude, lng: selectedEvent.longitude }}
              onCloseClick={handleInfoWindowClose}
            >
              <div className={styles.infoWindow}>
                {selectedEvent.image && (
                  <img
                    src={selectedEvent.image}
                    alt={selectedEvent.title}
                    className={styles.eventImage}
                  />
                )}
                <h3>{selectedEvent.title}</h3>
                <p className={styles.date}>
                  {new Date(selectedEvent.date).toLocaleDateString()}
                </p>
                <p className={styles.location}>{selectedEvent.location}</p>
                <button
                  className={styles.viewButton}
                  onClick={() => handleViewEvent(selectedEvent.id)}
                >
                  View Details
                </button>
              </div>
            </InfoWindow>
          )}
        </Map>
      </APIProvider>
    </div>
  );
}
