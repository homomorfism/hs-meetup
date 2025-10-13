import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import EventCard from '../components/EventCard';
import Filters from '../components/Filters';
import SearchBar from '../components/SearchBar';
import { eventsAPI } from '../services/api';
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
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        setLoading(true);
        // Build API filter params
        const apiFilters = {};
        if (filters.keyword) apiFilters.keyword = filters.keyword;
        if (filters.location) apiFilters.location = filters.location;
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
      }
    };

    fetchEvents();
  }, [filters.keyword, filters.location, filters.category, filters.isOnline, filters.price]);

  const handleSearch = ({ keyword, location }) => {
    setFilters(prev => ({ ...prev, keyword, location }));
  };

  return (
    <div className={styles.findEvents}>
      <div className={styles.searchSection}>
        <div className={styles.container}>
          <h1 className={styles.title}>Find events</h1>
          <SearchBar onSearch={handleSearch} />
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
                  </h2>
                </div>
                <div className={styles.eventsGrid}>
                  {filteredEvents.map(event => (
                    <EventCard key={event.id} event={event} />
                  ))}
                </div>
                {filteredEvents.length === 0 && (
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
