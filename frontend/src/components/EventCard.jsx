import { Link } from 'react-router-dom';
import { groups } from '../data';
import styles from './EventCard.module.css';

export default function EventCard({ event }) {
  const group = groups.find(g => g.id === event.group);

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
  };

  return (
    <Link to={`/events/${event.id}`} className={styles.card}>
      <div className={styles.imageContainer}>
        <img src={event.image} alt={event.title} className={styles.image} />
        {event.isOnline && <span className={styles.onlineBadge}>Online</span>}
      </div>
      <div className={styles.content}>
        <div className={styles.date}>
          {formatDate(event.date)} &bull; {event.time}
        </div>
        <h3 className={styles.title}>{event.title}</h3>
        <div className={styles.group}>{group?.name}</div>
        <div className={styles.footer}>
          <span className={styles.attendees}>{event.attendees} attendees</span>
          <span className={styles.price}>{event.price}</span>
        </div>
      </div>
    </Link>
  );
}
