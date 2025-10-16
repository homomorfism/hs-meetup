import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import EventCard from '../components/EventCard';
import UserCard from '../components/UserCard';
import { groupsAPI, usersAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import styles from './GroupDetails.module.css';

export default function GroupDetails() {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const [group, setGroup] = useState(null);
  const [organizer, setOrganizer] = useState(null);
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [pastEvents, setPastEvents] = useState([]);
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isJoined, setIsJoined] = useState(false);

  useEffect(() => {
    const fetchGroupData = async () => {
      try {
        setLoading(true);
        const groupData = await groupsAPI.getById(id);
        setGroup(groupData);

        const [organizerData, eventsData, membersData] = await Promise.all([
          groupData.organizer_id ? usersAPI.getById(groupData.organizer_id) : null,
          groupsAPI.getEvents(id),
          groupsAPI.getMembers(id)
        ]);

        setOrganizer(organizerData);

        // Filter upcoming and past events
        const now = new Date();
        setUpcomingEvents(eventsData.filter(e => new Date(e.date) >= now));
        setPastEvents(eventsData.filter(e => new Date(e.date) < now));

        setMembers(membersData.slice(0, 6));
      } catch (err) {
        setError(err.message);
        console.error('Error fetching group:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchGroupData();
  }, [id]);

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error || !group) {
    return <div className={styles.notFound}>Group not found</div>;
  }

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  };

  const handleJoin = async () => {
    if (!isAuthenticated) {
      alert('Please log in to join groups');
      return;
    }

    try {
      await groupsAPI.join(id);
      setIsJoined(true);
      // Update members count
      setGroup(prev => ({
        ...prev,
        members_count: (prev.members_count || 0) + 1
      }));
      alert('Successfully joined the group!');
    } catch (err) {
      console.error('Error joining group:', err);
      alert('Failed to join group. Please try again.');
    }
  };

  return (
    <div className={styles.groupDetails}>
      <div className={styles.hero}>
        <img src={group.image || `https://source.unsplash.com/1200x400/?community`} alt={group.name} className={styles.heroImage} />
      </div>

      <div className={styles.header}>
        <div className={styles.container}>
          <h1 className={styles.title}>{group.name}</h1>
          <div className={styles.meta}>
            <span>{group.location}</span>
            <span>{(group.members_count || 0).toLocaleString()} members</span>
            <span>Founded {formatDate(group.founded)}</span>
          </div>
        </div>
      </div>

      <div className={styles.container}>
        <div className={styles.layout}>
          <main className={styles.main}>
            <section className={styles.section}>
              <h2>About</h2>
              <p className={styles.description}>{group.description}</p>
            </section>

            {upcomingEvents.length > 0 && (
              <section className={styles.section}>
                <h2>Upcoming events ({upcomingEvents.length})</h2>
                <div className={styles.eventsGrid}>
                  {upcomingEvents.map(event => (
                    <EventCard key={event.id} event={event} />
                  ))}
                </div>
              </section>
            )}

            {pastEvents.length > 0 && (
              <section className={styles.section}>
                <h2>Past events ({pastEvents.length})</h2>
                <div className={styles.eventsGrid}>
                  {pastEvents.slice(0, 6).map(event => (
                    <EventCard key={event.id} event={event} />
                  ))}
                </div>
              </section>
            )}

            <section className={styles.section}>
              <h2>Members ({(group.members_count || 0).toLocaleString()})</h2>
              <div className={styles.membersGrid}>
                {members.map(user => (
                  <UserCard key={user.id} user={user} />
                ))}
              </div>
            </section>
          </main>

          <aside className={styles.sidebar}>
            <div className={styles.card}>
              <button
                className={styles.joinBtn}
                onClick={handleJoin}
                disabled={isJoined}
              >
                {isJoined ? 'Joined' : 'Join group'}
              </button>
              <div className={styles.memberInfo}>
                {(group.members_count || 0).toLocaleString()} members
              </div>
            </div>

            {organizer && (
              <div className={styles.card}>
                <h3>Organizer</h3>
                <Link to={`/members/${organizer.id}`} className={styles.organizerLink}>
                  <img src={organizer.avatar} alt={organizer.name} className={styles.organizerAvatar} />
                  <div>
                    <div className={styles.organizerName}>{organizer.name}</div>
                    <div className={styles.organizerRole}>Group organizer</div>
                  </div>
                </Link>
              </div>
            )}

            <div className={styles.card}>
              <h3>Category</h3>
              <div className={styles.category}>{group.category}</div>
            </div>

            <div className={styles.card}>
              <h3>Location</h3>
              <div className={styles.location}>{group.location}</div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
