import { Link } from 'react-router-dom';
import styles from './GroupCard.module.css';

export default function GroupCard({ group }) {
  return (
    <Link to={`/groups/${group.id}`} className={styles.card}>
      <div className={styles.imageContainer}>
        <img src={group.image || `https://source.unsplash.com/400x300/?community`} alt={group.name} className={styles.image} />
      </div>
      <div className={styles.content}>
        <h3 className={styles.title}>{group.name}</h3>
        <p className={styles.description}>{group.description}</p>
        <div className={styles.footer}>
          <span className={styles.members}>{(group.members_count || 0).toLocaleString()} members</span>
          <span className={styles.category}>{group.category}</span>
        </div>
      </div>
    </Link>
  );
}
