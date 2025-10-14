import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { usersAPI } from '../services/api';
import EventCard from '../components/EventCard';
import UserCard from '../components/UserCard';
import styles from './PersonalProfile.module.css';

export default function PersonalProfile() {
  const { user } = useAuth();
  const [organizedEvents, setOrganizedEvents] = useState([]);
  const [attendingEvents, setAttendingEvents] = useState([]);
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      if (!user) return;

      try {
        setLoading(true);
        const [organized, attending, friendsList] = await Promise.all([
          usersAPI.getEvents(user.id),
          usersAPI.getAttending(user.id),
          usersAPI.getFriends(user.id).catch(() => []), // Friends endpoint might not exist yet
        ]);

        setOrganizedEvents(organized);
        setAttendingEvents(attending);
        setFriends(friendsList);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching user data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [user]);

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error) {
    return <div className={styles.error}>Error loading profile: {error}</div>;
  }

  if (!user) {
    return <div className={styles.error}>Please log in to view your profile</div>;
  }

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  };

  const now = new Date();
  const upcomingEvents = attendingEvents.filter(event => new Date(event.date) >= now);
  const pastEvents = attendingEvents.filter(event => new Date(event.date) < now);

  return (
    <div className={styles.personalProfile}>
      <div className={styles.header}>
        <div className={styles.container}>
          <div className={styles.headerContent}>
            <img
              src={user.avatar || 'https://i.pravatar.cc/300?img=1'}
              alt={user.name}
              className={styles.avatar}
            />
            <div className={styles.headerInfo}>
              <h1 className={styles.name}>{user.name}</h1>
              <div className={styles.location}>{user.location || 'No location set'}</div>
              <div className={styles.memberSince}>
                Member since {formatDate(user.member_since)}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.container}>
        <div className={styles.layout}>
          <aside className={styles.sidebar}>
            <div className={styles.card}>
              <h2 className={styles.cardTitle}>About</h2>
              <p className={styles.bio}>{user.bio || 'No bio added yet.'}</p>
            </div>

            {friends.length > 0 && (
              <div className={styles.card}>
                <h2 className={styles.cardTitle}>Friends ({friends.length})</h2>
                <div className={styles.friendsList}>
                  {friends.slice(0, 10).map((friend) => (
                    <Link
                      key={friend.id}
                      to={`/members/${friend.id}`}
                      className={styles.friendItem}
                    >
                      <img
                        src={friend.avatar || 'https://i.pravatar.cc/150'}
                        alt={friend.name}
                        className={styles.friendAvatar}
                      />
                      <span className={styles.friendName}>{friend.name}</span>
                    </Link>
                  ))}
                </div>
                {friends.length > 10 && (
                  <div className={styles.showMore}>
                    and {friends.length - 10} more...
                  </div>
                )}
              </div>
            )}

            {user.interests && user.interests.length > 0 && (
              <div className={styles.card}>
                <h2 className={styles.cardTitle}>Interests</h2>
                <div className={styles.interests}>
                  {user.interests.map((interest, index) => (
                    <span key={index} className={styles.interest}>
                      {interest}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </aside>

          <main className={styles.main}>
            {upcomingEvents.length > 0 && (
              <section className={styles.section}>
                <h2 className={styles.sectionTitle}>
                  Upcoming Events ({upcomingEvents.length})
                </h2>
                <div className={styles.eventsGrid}>
                  {upcomingEvents.map((event) => (
                    <EventCard key={event.id} event={event} />
                  ))}
                </div>
              </section>
            )}

            {pastEvents.length > 0 && (
              <section className={styles.section}>
                <h2 className={styles.sectionTitle}>
                  Past Events ({pastEvents.length})
                </h2>
                <div className={styles.eventsGrid}>
                  {pastEvents.slice(0, 6).map((event) => (
                    <EventCard key={event.id} event={event} />
                  ))}
                </div>
                {pastEvents.length > 6 && (
                  <div className={styles.showMoreEvents}>
                    Showing 6 of {pastEvents.length} past events
                  </div>
                )}
              </section>
            )}

            {organizedEvents.length > 0 && (
              <section className={styles.section}>
                <h2 className={styles.sectionTitle}>
                  Events I Organize ({organizedEvents.length})
                </h2>
                <div className={styles.eventsGrid}>
                  {organizedEvents.map((event) => (
                    <EventCard key={event.id} event={event} />
                  ))}
                </div>
              </section>
            )}

            {upcomingEvents.length === 0 &&
              pastEvents.length === 0 &&
              organizedEvents.length === 0 && (
                <div className={styles.emptyState}>
                  <h3>No events yet</h3>
                  <p>Start exploring events and join the community!</p>
                  <Link to="/find" className={styles.findEventsBtn}>
                    Find Events
                  </Link>
                </div>
              )}
          </main>
        </div>
      </div>
    </div>
  );
}
