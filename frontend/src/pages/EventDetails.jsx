import { useParams, Link } from 'react-router-dom';
import EventCard from '../components/EventCard';
import UserCard from '../components/UserCard';
import { events, groups, users } from '../data';
import styles from './EventDetails.module.css';

export default function EventDetails() {
  const { id } = useParams();
  const event = events.find(e => e.id === parseInt(id));

  if (!event) {
    return <div className={styles.notFound}>Event not found</div>;
  }

  const group = groups.find(g => g.id === event.group);
  const organizer = users.find(u => u.id === event.organizer);

  // Get similar events (same category, exclude current)
  const similarEvents = events
    .filter(e => e.category === event.category && e.id !== event.id)
    .slice(0, 3);

  // Get some attendees
  const attendees = users.slice(0, Math.min(event.attendees, 6));

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className={styles.eventDetails}>
      <div className={styles.hero}>
        <img src={event.image} alt={event.title} className={styles.heroImage} />
      </div>

      <div className={styles.container}>
        <div className={styles.layout}>
          <main className={styles.main}>
            <h1 className={styles.title}>{event.title}</h1>

            <div className={styles.meta}>
              <div className={styles.metaItem}>
                <strong>Date:</strong> {formatDate(event.date)} at {event.time}
              </div>
              <div className={styles.metaItem}>
                <strong>Duration:</strong> {event.duration}
              </div>
              <div className={styles.metaItem}>
                <strong>Location:</strong> {event.isOnline ? 'Online event' : event.location}
              </div>
              <div className={styles.metaItem}>
                <strong>Price:</strong> {event.price}
              </div>
            </div>

            <div className={styles.section}>
              <h2>Details</h2>
              <p className={styles.description}>{event.description}</p>
            </div>

            <div className={styles.section}>
              <h2>Attendees ({event.attendees})</h2>
              <div className={styles.attendeesGrid}>
                {attendees.map(user => (
                  <UserCard key={user.id} user={user} />
                ))}
              </div>
            </div>

            {similarEvents.length > 0 && (
              <div className={styles.section}>
                <h2>Similar events</h2>
                <div className={styles.similarEvents}>
                  {similarEvents.map(e => (
                    <EventCard key={e.id} event={e} />
                  ))}
                </div>
              </div>
            )}
          </main>

          <aside className={styles.sidebar}>
            <div className={styles.card}>
              <button className={styles.attendBtn}>Attend</button>
              <div className={styles.attendInfo}>
                <span>{event.attendees} attending</span>
                {event.maxAttendees && (
                  <span>{event.maxAttendees - event.attendees} spots left</span>
                )}
              </div>
            </div>

            {group && (
              <div className={styles.card}>
                <h3>Hosted by</h3>
                <Link to={`/groups/${group.id}`} className={styles.groupLink}>
                  <img src={group.image} alt={group.name} className={styles.groupImage} />
                  <div>
                    <div className={styles.groupName}>{group.name}</div>
                    <div className={styles.groupMembers}>{group.members.toLocaleString()} members</div>
                  </div>
                </Link>
              </div>
            )}

            {organizer && (
              <div className={styles.card}>
                <h3>Organizer</h3>
                <Link to={`/members/${organizer.id}`} className={styles.organizerLink}>
                  <img src={organizer.avatar} alt={organizer.name} className={styles.organizerAvatar} />
                  <span>{organizer.name}</span>
                </Link>
              </div>
            )}
          </aside>
        </div>
      </div>
    </div>
  );
}
