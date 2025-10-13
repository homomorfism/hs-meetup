import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import EventCard from '../components/EventCard';
import Filters from '../components/Filters';
import SearchBar from '../components/SearchBar';
import { events } from '../data';
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
  const [filteredEvents, setFilteredEvents] = useState(events);

  useEffect(() => {
    let filtered = [...events];

    // Filter by keyword
    if (filters.keyword) {
      filtered = filtered.filter(event =>
        event.title.toLowerCase().includes(filters.keyword.toLowerCase()) ||
        event.description.toLowerCase().includes(filters.keyword.toLowerCase())
      );
    }

    // Filter by location
    if (filters.location) {
      filtered = filtered.filter(event =>
        event.locationCity.toLowerCase().includes(filters.location.toLowerCase())
      );
    }

    // Filter by category
    if (filters.category) {
      filtered = filtered.filter(event => event.category === filters.category);
    }

    // Filter by online/in-person
    if (filters.isOnline === 'online') {
      filtered = filtered.filter(event => event.isOnline);
    } else if (filters.isOnline === 'in-person') {
      filtered = filtered.filter(event => !event.isOnline);
    }

    // Filter by price
    if (filters.price === 'free') {
      filtered = filtered.filter(event => event.price.toLowerCase() === 'free');
    } else if (filters.price === 'paid') {
      filtered = filtered.filter(event => event.price.toLowerCase() !== 'free');
    }

    setFilteredEvents(filtered);
  }, [filters]);

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
          </main>
        </div>
      </div>
    </div>
  );
}
