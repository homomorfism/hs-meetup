import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import EventCard from '../components/EventCard';
import GroupCard from '../components/GroupCard';
import { usersAPI } from '../services/api';
import styles from './UserProfile.module.css';

export default function UserProfile() {
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const [userEvents, setUserEvents] = useState([]);
  const [userGroups, setUserGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        setLoading(true);
        const [userData, eventsData, groupsData] = await Promise.all([
          usersAPI.getById(id),
          usersAPI.getEvents(id),
          usersAPI.getGroups(id)
        ]);

        setUser(userData);
        setUserEvents(eventsData);
        setUserGroups(groupsData);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching user:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [id]);

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error || !user) {
    return <div className={styles.notFound}>User not found</div>;
  }

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
              <div className={styles.memberSince}>Member since {formatDate(user.member_since)}</div>
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

            {user.interests && user.interests.length > 0 && (
              <div className={styles.card}>
                <h2 className={styles.cardTitle}>Interests</h2>
                <div className={styles.interests}>
                  {user.interests.map((interest, index) => (
                    <span key={index} className={styles.interest}>{interest}</span>
                  ))}
                </div>
              </div>
            )}
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
