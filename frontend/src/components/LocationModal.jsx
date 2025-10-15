import { useState } from 'react';
import styles from './LocationModal.module.css';

const POPULAR_CITIES = [
  { name: 'Barcelona', country: 'Spain', latitude: 41.3851, longitude: 2.1734 },
  { name: 'Madrid', country: 'Spain', latitude: 40.4168, longitude: -3.7038 },
  { name: 'London', country: 'UK', latitude: 51.5074, longitude: -0.1278 },
  { name: 'Paris', country: 'France', latitude: 48.8566, longitude: 2.3522 },
  { name: 'Berlin', country: 'Germany', latitude: 52.5200, longitude: 13.4050 },
  { name: 'Amsterdam', country: 'Netherlands', latitude: 52.3676, longitude: 4.9041 },
  { name: 'Rome', country: 'Italy', latitude: 41.9028, longitude: 12.4964 },
  { name: 'Lisbon', country: 'Portugal', latitude: 38.7223, longitude: -9.1393 },
  { name: 'New York', country: 'USA', latitude: 40.7128, longitude: -74.0060 },
  { name: 'San Francisco', country: 'USA', latitude: 37.7749, longitude: -122.4194 },
  { name: 'Los Angeles', country: 'USA', latitude: 34.0522, longitude: -118.2437 },
  { name: 'Toronto', country: 'Canada', latitude: 43.6532, longitude: -79.3832 },
  { name: 'Sydney', country: 'Australia', latitude: -33.8688, longitude: 151.2093 },
  { name: 'Tokyo', country: 'Japan', latitude: 35.6762, longitude: 139.6503 },
  { name: 'Singapore', country: 'Singapore', latitude: 1.3521, longitude: 103.8198 },
];

export default function LocationModal({ onSelectLocation, onUseGeolocation }) {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredCities = POPULAR_CITIES.filter(city =>
    city.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    city.country.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleCitySelect = (city) => {
    onSelectLocation({
      latitude: city.latitude,
      longitude: city.longitude,
      city: city.name,
    });
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modal}>
        <h2 className={styles.title}>Choose Your Location</h2>
        <p className={styles.subtitle}>
          Select your city to see events near you
        </p>

        <button
          className={styles.geolocationBtn}
          onClick={onUseGeolocation}
        >
          📍 Use My Current Location
        </button>

        <div className={styles.divider}>
          <span>or choose a city</span>
        </div>

        <input
          type="text"
          placeholder="Search for a city..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className={styles.searchInput}
        />

        <div className={styles.citiesList}>
          {filteredCities.map((city) => (
            <button
              key={`${city.name}-${city.country}`}
              className={styles.cityButton}
              onClick={() => handleCitySelect(city)}
            >
              <span className={styles.cityName}>{city.name}</span>
              <span className={styles.cityCountry}>{city.country}</span>
            </button>
          ))}
        </div>

        {filteredCities.length === 0 && (
          <p className={styles.noResults}>
            No cities found. Try a different search.
          </p>
        )}
      </div>
    </div>
  );
}
