import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import EventCard from '../components/EventCard';
import Filters from '../components/Filters';
import SearchBar from '../components/SearchBar';
import { eventsAPI, savedSearchesAPI, searchHistoryAPI } from '../services/api';
import { useDebounce } from '../hooks/useDebounce';
import { useAuth } from '../context/AuthContext';
import styles from './FindEvents.module.css';

export default function FindEvents() {
  const { isAuthenticated } = useAuth();
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

  // Saved searches state
  const [savedSearches, setSavedSearches] = useState([]);
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [searchName, setSearchName] = useState('');
  const [showSavedSearches, setShowSavedSearches] = useState(false);
  const [saveError, setSaveError] = useState(null);

  // Search history state
  const [searchHistory, setSearchHistory] = useState([]);
  const [showSearchHistory, setShowSearchHistory] = useState(false);

  // Debounce keyword and location to avoid excessive API calls
  const debouncedKeyword = useDebounce(filters.keyword, 500);
  const debouncedLocation = useDebounce(filters.location, 500);

  // Fetch saved searches and search history on mount (only if authenticated)
  useEffect(() => {
    if (!isAuthenticated) {
      return;
    }

    const fetchSavedSearches = async () => {
      try {
        const searches = await savedSearchesAPI.getAll();
        setSavedSearches(searches);
      } catch (err) {
        console.error('Error fetching saved searches:', err);
      }
    };

    const fetchSearchHistory = async () => {
      try {
        const history = await searchHistoryAPI.getAll(5);
        setSearchHistory(history);
      } catch (err) {
        console.error('Error fetching search history:', err);
      }
    };

    fetchSavedSearches();
    fetchSearchHistory();
  }, [isAuthenticated]);

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

  // Separate effect for recording search history (only after debounced values settle)
  useEffect(() => {
    // Don't record on initial load or if not authenticated
    if (!isAuthenticated || filteredEvents.length === 0) {
      return;
    }

    // Only record if there are any filters
    if (!debouncedKeyword && !debouncedLocation && !filters.category && !filters.isOnline && !filters.price) {
      return;
    }

    const recordHistory = async () => {
      try {
        const historyData = {
          keyword: debouncedKeyword || null,
          location: debouncedLocation || null,
          category: filters.category || null,
          is_online: filters.isOnline === 'online' ? true : filters.isOnline === 'in-person' ? false : null,
          price: filters.price || null,
        };
        const newHistory = await searchHistoryAPI.create(historyData);
        // Update history list, removing duplicates and keeping only recent 5
        setSearchHistory(prev => {
          const filtered = prev.filter(h => h.id !== newHistory.id);
          return [newHistory, ...filtered].slice(0, 5);
        });
      } catch (err) {
        console.error('Error recording search history:', err);
      }
    };

    recordHistory();
  }, [debouncedKeyword, debouncedLocation, filters.category, filters.isOnline, filters.price, isAuthenticated]);

  const handleSearchChange = ({ keyword, location }) => {
    setFilters(prev => ({ ...prev, keyword, location }));
  };

  const handleSaveSearch = async () => {
    if (!isAuthenticated) {
      setSaveError('Please log in to save searches');
      return;
    }

    if (!searchName.trim()) {
      setSaveError('Please enter a name for this search');
      return;
    }

    try {
      const searchData = {
        name: searchName.trim(),
        keyword: filters.keyword || null,
        location: filters.location || null,
        category: filters.category || null,
        is_online: filters.isOnline === 'online' ? true : filters.isOnline === 'in-person' ? false : null,
        price: filters.price || null,
      };

      const newSearch = await savedSearchesAPI.create(searchData);
      setSavedSearches([newSearch, ...savedSearches]);
      setShowSaveModal(false);
      setSearchName('');
      setSaveError(null);
    } catch (err) {
      setSaveError(err.message || 'Failed to save search');
      console.error('Error saving search:', err);
    }
  };

  const handleLoadSearch = (search) => {
    setFilters({
      keyword: search.keyword || '',
      location: search.location || '',
      category: search.category || '',
      date: '',
      isOnline: search.is_online === true ? 'online' : search.is_online === false ? 'in-person' : '',
      price: search.price || '',
    });
    setShowSavedSearches(false);
  };

  const handleDeleteSearch = async (searchId) => {
    try {
      await savedSearchesAPI.delete(searchId);
      setSavedSearches(savedSearches.filter(s => s.id !== searchId));
    } catch (err) {
      console.error('Error deleting search:', err);
    }
  };

  const hasActiveFilters = () => {
    return filters.keyword || filters.location || filters.category || filters.isOnline || filters.price;
  };

  const handleLoadHistory = (history) => {
    setFilters({
      keyword: history.keyword || '',
      location: history.location || '',
      category: history.category || '',
      date: '',
      isOnline: history.is_online === true ? 'online' : history.is_online === false ? 'in-person' : '',
      price: history.price || '',
    });
    setShowSearchHistory(false);
  };

  const handleDeleteHistory = async (historyId) => {
    try {
      await searchHistoryAPI.delete(historyId);
      setSearchHistory(searchHistory.filter(h => h.id !== historyId));
    } catch (err) {
      console.error('Error deleting history:', err);
    }
  };

  const handleClearHistory = async () => {
    try {
      await searchHistoryAPI.clear();
      setSearchHistory([]);
      setShowSearchHistory(false);
    } catch (err) {
      console.error('Error clearing history:', err);
    }
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

          <div className={styles.savedSearchActions}>
            {hasActiveFilters() && isAuthenticated && (
              <button
                className={styles.saveSearchBtn}
                onClick={() => setShowSaveModal(true)}
              >
                💾 Save this search
              </button>
            )}

            {isAuthenticated && savedSearches.length > 0 && (
              <div className={styles.savedSearchDropdown}>
                <button
                  className={styles.savedSearchBtn}
                  onClick={() => setShowSavedSearches(!showSavedSearches)}
                >
                  ⭐ My saved searches ({savedSearches.length})
                </button>

                {showSavedSearches && (
                  <div className={styles.savedSearchMenu}>
                    {savedSearches.map(search => (
                      <div key={search.id} className={styles.savedSearchItem}>
                        <button
                          className={styles.loadSearchBtn}
                          onClick={() => handleLoadSearch(search)}
                        >
                          <span className={styles.searchName}>{search.name}</span>
                          <span className={styles.searchDetails}>
                            {[
                              search.keyword && `"${search.keyword}"`,
                              search.location && `📍 ${search.location}`,
                              search.category && `🏷️ ${search.category}`,
                            ].filter(Boolean).join(' • ')}
                          </span>
                        </button>
                        <button
                          className={styles.deleteSearchBtn}
                          onClick={() => handleDeleteSearch(search.id)}
                          title="Delete search"
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {isAuthenticated && searchHistory.length > 0 && (
              <div className={styles.savedSearchDropdown}>
                <button
                  className={styles.historyBtn}
                  onClick={() => setShowSearchHistory(!showSearchHistory)}
                >
                  🕒 Recent searches ({searchHistory.length})
                </button>

                {showSearchHistory && (
                  <div className={styles.savedSearchMenu}>
                    <div className={styles.historyHeader}>
                      <span className={styles.historyTitle}>Recent Searches</span>
                      <button
                        className={styles.clearHistoryBtn}
                        onClick={handleClearHistory}
                      >
                        Clear all
                      </button>
                    </div>
                    {searchHistory.map(history => (
                      <div key={history.id} className={styles.savedSearchItem}>
                        <button
                          className={styles.loadSearchBtn}
                          onClick={() => handleLoadHistory(history)}
                        >
                          <span className={styles.searchDetails}>
                            {[
                              history.keyword && `"${history.keyword}"`,
                              history.location && `📍 ${history.location}`,
                              history.category && `🏷️ ${history.category}`,
                              history.is_online === true && '🌐 Online',
                              history.is_online === false && '📍 In-person',
                              history.price && `💰 ${history.price}`,
                            ].filter(Boolean).join(' • ') || 'All events'}
                          </span>
                        </button>
                        <button
                          className={styles.deleteSearchBtn}
                          onClick={() => handleDeleteHistory(history.id)}
                          title="Remove from history"
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Save Search Modal */}
      {showSaveModal && (
        <div className={styles.modalOverlay} onClick={() => setShowSaveModal(false)}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <h3 className={styles.modalTitle}>Save this search</h3>
            <p className={styles.modalDescription}>
              Give your search a name so you can quickly find it later
            </p>

            {saveError && (
              <div className={styles.modalError}>{saveError}</div>
            )}

            <input
              type="text"
              className={styles.modalInput}
              placeholder="e.g., Tech events in SF"
              value={searchName}
              onChange={(e) => setSearchName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSaveSearch()}
              autoFocus
            />

            <div className={styles.modalActions}>
              <button
                className={styles.modalCancel}
                onClick={() => {
                  setShowSaveModal(false);
                  setSearchName('');
                  setSaveError(null);
                }}
              >
                Cancel
              </button>
              <button
                className={styles.modalSave}
                onClick={handleSaveSearch}
              >
                Save search
              </button>
            </div>
          </div>
        </div>
      )}

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
