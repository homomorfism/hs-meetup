import styles from './SearchBar.module.css';

export default function SearchBar({ keyword, location, onChange }) {
  const handleKeywordChange = (e) => {
    onChange({ keyword: e.target.value, location });
  };

  const handleLocationChange = (e) => {
    onChange({ keyword, location: e.target.value });
  };

  return (
    <div className={styles.searchBar}>
      <div className={styles.inputGroup}>
        <input
          type="text"
          placeholder="Search for events"
          value={keyword}
          onChange={handleKeywordChange}
          className={styles.input}
        />
      </div>
      <div className={styles.inputGroup}>
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={handleLocationChange}
          className={styles.input}
        />
      </div>
    </div>
  );
}
