import { categories } from '../data';
import styles from './Filters.module.css';

export default function Filters({ filters, onChange }) {
  const handleChange = (key, value) => {
    onChange({ ...filters, [key]: value });
  };

  return (
    <div className={styles.filters}>
      <div className={styles.filterGroup}>
        <label className={styles.label}>Date</label>
        <select
          value={filters.date || ''}
          onChange={(e) => handleChange('date', e.target.value)}
          className={styles.select}
        >
          <option value="">Any date</option>
          <option value="today">Today</option>
          <option value="tomorrow">Tomorrow</option>
          <option value="this-week">This week</option>
          <option value="this-weekend">This weekend</option>
          <option value="next-week">Next week</option>
        </select>
      </div>

      <div className={styles.filterGroup}>
        <label className={styles.label}>Category</label>
        <select
          value={filters.category || ''}
          onChange={(e) => handleChange('category', e.target.value)}
          className={styles.select}
        >
          <option value="">All categories</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.name}>{cat.name}</option>
          ))}
        </select>
      </div>

      <div className={styles.filterGroup}>
        <label className={styles.label}>Format</label>
        <select
          value={filters.isOnline || ''}
          onChange={(e) => handleChange('isOnline', e.target.value)}
          className={styles.select}
        >
          <option value="">All events</option>
          <option value="online">Online</option>
          <option value="in-person">In person</option>
        </select>
      </div>

      <div className={styles.filterGroup}>
        <label className={styles.label}>Price</label>
        <select
          value={filters.price || ''}
          onChange={(e) => handleChange('price', e.target.value)}
          className={styles.select}
        >
          <option value="">Any price</option>
          <option value="free">Free</option>
          <option value="paid">Paid</option>
        </select>
      </div>
    </div>
  );
}
