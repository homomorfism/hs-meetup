import { useState, useEffect } from 'react';
import { categoriesAPI } from '../services/api';
import styles from './GroupFilters.module.css';

export default function GroupFilters({ filters, onChange }) {
  const [categories, setCategories] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState(filters.categories || []);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const data = await categoriesAPI.getAll();
        setCategories(data);
      } catch (err) {
        console.error('Error fetching categories:', err);
      }
    };

    fetchCategories();
  }, []);

  const handleCategoryToggle = (categoryName) => {
    const newSelectedCategories = selectedCategories.includes(categoryName)
      ? selectedCategories.filter(c => c !== categoryName)
      : [...selectedCategories, categoryName];

    setSelectedCategories(newSelectedCategories);
    onChange({ ...filters, categories: newSelectedCategories });
  };

  const handleClearCategories = () => {
    setSelectedCategories([]);
    onChange({ ...filters, categories: [] });
  };

  return (
    <div className={styles.filters}>
      <div className={styles.filterGroup}>
        <div className={styles.labelRow}>
          <label className={styles.label}>Category</label>
          {selectedCategories.length > 0 && (
            <button
              onClick={handleClearCategories}
              className={styles.clearButton}
            >
              Clear all
            </button>
          )}
        </div>
        <div className={styles.checkboxList}>
          {categories.map(cat => (
            <label key={cat.id} className={styles.checkboxLabel}>
              <input
                type="checkbox"
                checked={selectedCategories.includes(cat.name)}
                onChange={() => handleCategoryToggle(cat.name)}
                className={styles.checkbox}
              />
              <span className={styles.checkboxText}>{cat.name}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
}
