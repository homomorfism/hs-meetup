import { Link } from 'react-router-dom';
import styles from './UserCard.module.css';

export default function UserCard({ user }) {
  return (
    <Link to={`/members/${user.id}`} className={styles.card}>
      <img src={user.avatar} alt={user.name} className={styles.avatar} />
      <div className={styles.info}>
        <h3 className={styles.name}>{user.name}</h3>
        <p className={styles.location}>{user.location}</p>
        <div className={styles.interests}>
          {user.interests.slice(0, 2).map((interest, index) => (
            <span key={index} className={styles.interest}>{interest}</span>
          ))}
        </div>
      </div>
    </Link>
  );
}
