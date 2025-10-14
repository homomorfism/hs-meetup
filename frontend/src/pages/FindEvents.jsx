import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import EventCard from '../components/EventCard';
import Filters from '../components/Filters';
import SearchBar from '../components/SearchBar';
import { eventsAPI } from '../services/api';
import { useDebounce } from '../hooks/useDebounce';
import styles from './FindEvents.module.css';

export default function FindEvents() {
  const [searchParams] = useSearchParams();
  const [filters, setFilters] = useState({
    keyword: searchParams.get('keyword') || '',
    location: searchParams.get('location') || '',
    category: searchParams.get('category') || '',
    date: '',
    isOnline: '',
    price: '',
  });
  const [filteredEvents, setFilteredEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState(null);

  // Debounce keyword and location to avoid excessive API calls
  const debouncedKeyword = useDebounce(filters.keyword, 500);
  const debouncedLocation = useDebounce(filters.location, 500);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        // Only show full loading on initial load
        if (filteredEvents.length === 0) {
          setLoading(true);
        } else {
          // Show subtle searching indicator for subsequent searches
          setIsSearching(true);
        }

        // Build API filter params
        const apiFilters = {};
        if (debouncedKeyword) apiFilters.keyword = debouncedKeyword;
        if (debouncedLocation) apiFilters.location = debouncedLocation;
        if (filters.category) apiFilters.category = filters.category;
        if (filters.isOnline === 'online') apiFilters.isOnline = 'true';
        if (filters.isOnline === 'in-person') apiFilters.isOnline = 'false';
        if (filters.price === 'free') apiFilters.price = 'free';
        if (filters.price === 'paid') apiFilters.price = 'paid';

        const events = await eventsAPI.getAll(apiFilters);
        setFilteredEvents(events);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching events:', err);
      } finally {
        setLoading(false);
        setIsSearching(false);
      }
    };

    fetchEvents();
  }, [debouncedKeyword, debouncedLocation, filters.category, filters.isOnline, filters.price]);

  const handleSearchChange = ({ keyword, location }) => {
    setFilters(prev => ({ ...prev, keyword, location }));
  };

  return (
    <div className={styles.findEvents}>
      <div className={styles.searchSection}>
        <div className={styles.container}>
          <h1 className={styles.title}>Find events</h1>
          <SearchBar
            keyword={filters.keyword}
            location={filters.location}
            onChange={handleSearchChange}
          />
        </div>
      </div>

      <div className={styles.container}>
        <div className={styles.layout}>
          <aside className={styles.sidebar}>
            <h2 className={styles.filterTitle}>Filters</h2>
            <Filters filters={filters} onChange={setFilters} />
          </aside>

          <main className={styles.main}>
            {loading ? (
              <div className={styles.loading}>Loading events...</div>
            ) : error ? (
              <div className={styles.error}>Error: {error}</div>
            ) : (
              <>
                <div className={styles.resultsHeader}>
                  <h2 className={styles.resultsTitle}>
                    {filteredEvents.length} events
                    {isSearching && <span className={styles.searchingIndicator}> (searching...)</span>}
                  </h2>
                </div>
                <div className={styles.eventsGrid} style={{ opacity: isSearching ? 0.6 : 1, transition: 'opacity 0.2s ease' }}>
                  {filteredEvents.map(event => (
                    <EventCard key={event.id} event={event} />
                  ))}
                </div>
                {filteredEvents.length === 0 && !isSearching && (
                  <div className={styles.noResults}>
                    <p>No events found matching your criteria.</p>
                    <p>Try adjusting your filters or search terms.</p>
                  </div>
                )}
              </>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
