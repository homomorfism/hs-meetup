import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import GroupCard from '../components/GroupCard';
import GroupFilters from '../components/GroupFilters';
import { groupsAPI } from '../services/api';
import { useDebounce } from '../hooks/useDebounce';
import styles from './FindGroups.module.css';

export default function FindGroups() {
  const [searchParams] = useSearchParams();
  const [filters, setFilters] = useState({
    search: searchParams.get('search') || '',
    categories: [],
  });
  const [filteredGroups, setFilteredGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState(null);

  // Debounce search to avoid excessive API calls
  const debouncedSearch = useDebounce(filters.search, 500);

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        // Only show full loading on initial load
        if (filteredGroups.length === 0) {
          setLoading(true);
        } else {
          // Show subtle searching indicator for subsequent searches
          setIsSearching(true);
        }

        // Build API filter params
        const apiFilters = {};
        if (debouncedSearch) apiFilters.keyword = debouncedSearch;

        // If multiple categories are selected, we'll need to filter on frontend
        // or modify backend to support multiple categories
        if (filters.categories.length === 1) {
          apiFilters.category = filters.categories[0];
        }

        let groups = await groupsAPI.getAll(apiFilters);

        // Client-side filtering for multiple categories
        if (filters.categories.length > 1) {
          groups = groups.filter(group =>
            filters.categories.includes(group.category)
          );
        }

        setFilteredGroups(groups);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching groups:', err);
      } finally {
        setLoading(false);
        setIsSearching(false);
      }
    };

    fetchGroups();
  }, [debouncedSearch, filters.categories]);

  const handleSearchChange = (e) => {
    setFilters(prev => ({ ...prev, search: e.target.value }));
  };

  return (
    <div className={styles.findGroups}>
      <div className={styles.searchSection}>
        <div className={styles.container}>
          <h1 className={styles.title}>Find groups</h1>
          <div className={styles.searchBar}>
            <input
              type="text"
              placeholder="Search groups by name or description"
              value={filters.search}
              onChange={handleSearchChange}
              className={styles.searchInput}
            />
          </div>
        </div>
      </div>

      <div className={styles.container}>
        <div className={styles.layout}>
          <aside className={styles.sidebar}>
            <h2 className={styles.filterTitle}>Filters</h2>
            <GroupFilters filters={filters} onChange={setFilters} />
          </aside>

          <main className={styles.main}>
            {loading ? (
              <div className={styles.loading}>Loading groups...</div>
            ) : error ? (
              <div className={styles.error}>Error: {error}</div>
            ) : (
              <>
                <div className={styles.resultsHeader}>
                  <h2 className={styles.resultsTitle}>
                    {filteredGroups.length} groups
                    {isSearching && <span className={styles.searchingIndicator}> (searching...)</span>}
                  </h2>
                </div>
                <div className={styles.groupsGrid} style={{ opacity: isSearching ? 0.6 : 1, transition: 'opacity 0.2s ease' }}>
                  {filteredGroups.map(group => (
                    <GroupCard key={group.id} group={group} />
                  ))}
                </div>
                {filteredGroups.length === 0 && !isSearching && (
                  <div className={styles.noResults}>
                    <p>No groups found matching your criteria.</p>
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
