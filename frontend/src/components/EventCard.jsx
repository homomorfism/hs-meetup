import { Link } from 'react-router-dom';
import styles from './EventCard.module.css';

export default function EventCard({ event }) {
  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
  };

  return (
    <Link to={`/events/${event.id}`} className={styles.card}>
      <div className={styles.imageContainer}>
        <img src={event.image || `https://source.unsplash.com/400x300/?event`} alt={event.title} className={styles.image} />
        {event.is_online && <span className={styles.onlineBadge}>Online</span>}
      </div>
      <div className={styles.content}>
        <div className={styles.date}>
          {formatDate(event.date)} &bull; {event.time}
        </div>
        <h3 className={styles.title}>{event.title}</h3>
        <div className={styles.group}>{event.group_name || 'Group'}</div>
        <div className={styles.footer}>
          <span className={styles.attendees}>{event.attendees_count || 0} attendees</span>
          <span className={styles.price}>{event.price || 'Free'}</span>
        </div>
      </div>
    </Link>
  );
}
