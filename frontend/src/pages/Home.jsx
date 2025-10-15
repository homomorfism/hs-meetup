import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import EventCard from '../components/EventCard';
import EventMap from '../components/EventMap';
import LocationModal from '../components/LocationModal';
import { eventsAPI, categoriesAPI } from '../services/api';
import { getUserLocation, saveUserLocation, getSavedUserLocation } from '../services/geolocation';
import styles from './Home.module.css';

export default function Home() {
  const navigate = useNavigate();
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [allEvents, setAllEvents] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [searchLocation, setSearchLocation] = useState('');
  const [userLocation, setUserLocation] = useState(null);
  const [locationPermissionDenied, setLocationPermissionDenied] = useState(false);
  const [importing, setImporting] = useState(false);
  const [showLocationModal, setShowLocationModal] = useState(false);

  useEffect(() => {
    const initializeLocation = async () => {
      // Try to get saved location first
      const savedLocation = getSavedUserLocation();

      if (savedLocation) {
        setUserLocation(savedLocation);
        setSearchLocation(savedLocation.city || '');
        fetchData(savedLocation);
      } else {
        // Show location selection modal
        setShowLocationModal(true);
        setLoading(false);
      }
    };

    initializeLocation();
  }, []);

  const handleLocationSelected = async (location) => {
    setShowLocationModal(false);
    setLoading(true);
    setUserLocation(location);
    setSearchLocation(location.city || '');
    saveUserLocation(location);

    // Auto-import events
    await handleImportEvents(location);
  };

  const handleUseGeolocation = async () => {
    setShowLocationModal(false);
    setLoading(true);

    try {
      const location = await getUserLocation();
      setUserLocation(location);
      setSearchLocation(location.city || '');
      saveUserLocation(location);

      // Auto-import events
      await handleImportEvents(location);
    } catch (err) {
      console.error('Location error:', err);
      setLocationPermissionDenied(true);
      alert('Location access denied. Please select a city manually.');
      setShowLocationModal(true);
      setLoading(false);
    }
  };

  const handleImportEvents = async (location = userLocation) => {
    if (!location || importing) return;

    setImporting(true);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:10001/api'}/meetup-sync/import-by-geolocation?latitude=${location.latitude}&longitude=${location.longitude}&limit=50`,
        { method: 'POST' }
      );

      if (response.ok) {
        const result = await response.json();
        console.log(`✓ Imported ${result.imported_count} events near ${location.city || 'you'}`);
        // Refresh events
        await fetchData(location);
      } else {
        console.error('Failed to import events');
        await fetchData(location);
      }
    } catch (error) {
      console.error('Import error:', error);
      await fetchData(location);
    } finally {
      setImporting(false);
    }
  };

  const fetchData = async (location) => {
    try {
      setLoading(true);

      // Don't filter by city name - show all imported events
      // (they're already filtered by geolocation radius on import)
      const [eventsData, categoriesData] = await Promise.all([
        eventsAPI.getAll(),
        categoriesAPI.getAll()
      ]);

      // Store all events for the map
      setAllEvents(eventsData);
      // Get first 8 events for display
      setUpcomingEvents(eventsData.slice(0, 8));
      setCategories(categoriesData);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchChange = ({ keyword, location }) => {
    setSearchKeyword(keyword);
    setSearchLocation(location);
    // Navigate to find page with search params when user types
    if (keyword || location) {
      const params = new URLSearchParams();
      if (keyword) params.append('keyword', keyword);
      if (location) params.append('location', location);
      navigate(`/find?${params.toString()}`);
    }
  };

  if (loading) {
    return (
      <div className={styles.home}>
        <div className={styles.loading}>
          {!userLocation && !locationPermissionDenied && 'Getting your location...'}
          {!userLocation && locationPermissionDenied && 'Loading events...'}
          {userLocation && 'Loading events...'}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.home}>
        <div className={styles.error}>Error: {error}</div>
      </div>
    );
  }

  return (
    <div className={styles.home}>
      {/* Location Selection Modal */}
      {showLocationModal && (
        <LocationModal
          onSelectLocation={handleLocationSelected}
          onUseGeolocation={handleUseGeolocation}
        />
      )}

      {/* Location Banner */}
      {userLocation && (
        <div className={styles.locationBanner}>
          <p>
            📍 Showing events in {userLocation.city || 'your area'}
            <button
              onClick={() => setShowLocationModal(true)}
              style={{
                marginLeft: '1rem',
                padding: '0.25rem 0.75rem',
                borderRadius: '4px',
                border: '1px solid white',
                background: 'transparent',
                color: 'white',
                cursor: 'pointer',
                fontSize: '0.875rem'
              }}
            >
              Change Location
            </button>
          </p>
        </div>
      )}

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>The people platform</h1>
          <p className={styles.heroSubtitle}>
            Whatever your interest, from hiking and reading to networking and skill sharing,
            there are thousands of people who share it on Meetup.
          </p>
          <SearchBar
            keyword={searchKeyword}
            location={searchLocation}
            onChange={handleSearchChange}
          />
        </div>
      </section>

      {/* Categories Section */}
      {categories.length > 0 && (
        <section className={styles.section}>
          <div className={styles.container}>
            <h2 className={styles.sectionTitle}>Explore by category</h2>
            <div className={styles.categories}>
              {categories.map(category => (
                <Link
                  key={category.id}
                  to={`/find?category=${category.name}`}
                  className={styles.categoryCard}
                >
                  <span className={styles.categoryIcon}>{category.icon}</span>
                  <span className={styles.categoryName}>{category.name}</span>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Events Map Section */}
      {allEvents.length > 0 && (
        <section className={styles.section}>
          <div className={styles.container}>
            <h2 className={styles.sectionTitle}>Events near you</h2>
            <EventMap
              events={allEvents}
              height="600px"
              zoom={12}
              center={userLocation ? { lat: userLocation.latitude, lng: userLocation.longitude } : undefined}
            />
          </div>
        </section>
      )}

      {/* Upcoming Events Section */}
      {upcomingEvents.length > 0 && (
        <section className={styles.section}>
          <div className={styles.container}>
            <div className={styles.sectionHeader}>
              <h2 className={styles.sectionTitle}>Upcoming events</h2>
              <Link to="/find" className={styles.seeAll}>See all</Link>
            </div>
            <div className={styles.eventsGrid}>
              {upcomingEvents.map(event => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className={styles.ctaSection}>
        <div className={styles.container}>
          <h2 className={styles.ctaTitle}>How Meetup works</h2>
          <div className={styles.steps}>
            <div className={styles.step}>
              <div className={styles.stepNumber}>1</div>
              <h3>Discover events</h3>
              <p>Find events that match your interests</p>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>2</div>
              <h3>Join a group</h3>
              <p>Connect with people who share your passion</p>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>3</div>
              <h3>Start meeting</h3>
              <p>Attend events and make new friends</p>
            </div>
          </div>
          <button className={styles.ctaButton}>Join Meetup</button>
        </div>
      </section>
    </div>
  );
}
