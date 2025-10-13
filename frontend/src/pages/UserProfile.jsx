import { useParams } from 'react-router-dom';
import EventCard from '../components/EventCard';
import GroupCard from '../components/GroupCard';
import { users, events, groups } from '../data';
import styles from './UserProfile.module.css';

export default function UserProfile() {
  const { id } = useParams();
  const user = users.find(u => u.id === parseInt(id));

  if (!user) {
    return <div className={styles.notFound}>User not found</div>;
  }

  // Get events organized by this user
  const userEvents = events.filter(e => e.organizer === user.id);

  // Get groups where this user is an organizer
  const userGroups = groups.filter(g => g.organizer === user.id);

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  };

  return (
    <div className={styles.userProfile}>
      <div className={styles.header}>
        <div className={styles.container}>
          <div className={styles.headerContent}>
            <img src={user.avatar} alt={user.name} className={styles.avatar} />
            <div className={styles.headerInfo}>
              <h1 className={styles.name}>{user.name}</h1>
              <div className={styles.location}>{user.location}</div>
              <div className={styles.memberSince}>Member since {formatDate(user.memberSince)}</div>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.container}>
        <div className={styles.layout}>
          <aside className={styles.sidebar}>
            <div className={styles.card}>
              <h2 className={styles.cardTitle}>About</h2>
              <p className={styles.bio}>{user.bio}</p>
            </div>

            <div className={styles.card}>
              <h2 className={styles.cardTitle}>Interests</h2>
              <div className={styles.interests}>
                {user.interests.map((interest, index) => (
                  <span key={index} className={styles.interest}>{interest}</span>
                ))}
              </div>
            </div>
          </aside>

          <main className={styles.main}>
            {userGroups.length > 0 && (
              <section className={styles.section}>
                <h2 className={styles.sectionTitle}>Groups ({userGroups.length})</h2>
                <div className={styles.groupsGrid}>
                  {userGroups.map(group => (
                    <GroupCard key={group.id} group={group} />
                  ))}
                </div>
              </section>
            )}

            {userEvents.length > 0 && (
              <section className={styles.section}>
                <h2 className={styles.sectionTitle}>Events organized ({userEvents.length})</h2>
                <div className={styles.eventsGrid}>
                  {userEvents.map(event => (
                    <EventCard key={event.id} event={event} />
                  ))}
                </div>
              </section>
            )}

            {userGroups.length === 0 && userEvents.length === 0 && (
              <div className={styles.emptyState}>
                <p>This user hasn't organized any groups or events yet.</p>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
