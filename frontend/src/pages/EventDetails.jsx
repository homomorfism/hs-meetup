import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import EventCard from '../components/EventCard';
import UserCard from '../components/UserCard';
import EventMap from '../components/EventMap';
import { eventsAPI, groupsAPI, usersAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import styles from './EventDetails.module.css';

export default function EventDetails() {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const [event, setEvent] = useState(null);
  const [group, setGroup] = useState(null);
  const [organizer, setOrganizer] = useState(null);
  const [similarEvents, setSimilarEvents] = useState([]);
  const [attendees, setAttendees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAttending, setIsAttending] = useState(false);

  useEffect(() => {
    const fetchEventData = async () => {
      try {
        setLoading(true);
        // Fetch event details
        const eventData = await eventsAPI.getById(id);
        setEvent(eventData);

        // Fetch related data in parallel
        const [groupData, organizerData, attendeesData, allEvents] = await Promise.all([
          eventData.group_id ? groupsAPI.getById(eventData.group_id) : null,
          eventData.organizer_id ? usersAPI.getById(eventData.organizer_id) : null,
          eventsAPI.getAttendees(id),
          eventsAPI.getAll({ category: eventData.category })
        ]);

        setGroup(groupData);
        setOrganizer(organizerData);
        setAttendees(attendeesData.slice(0, 6));

        // Filter similar events (exclude current)
        setSimilarEvents(allEvents.filter(e => e.id !== parseInt(id)).slice(0, 3));
      } catch (err) {
        setError(err.message);
        console.error('Error fetching event:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchEventData();
  }, [id]);

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error || !event) {
    return <div className={styles.notFound}>Event not found</div>;
  }

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const handleHeroImageError = (e) => {
    e.target.src = `https://source.unsplash.com/1200x400/?${event.category || 'event'}`;
  };

  const handleGroupImageError = (e) => {
    e.target.src = `https://source.unsplash.com/200x200/?community`;
  };

  const handleOrganizerImageError = (e) => {
    e.target.src = `https://i.pravatar.cc/150?u=${organizer?.id || 'default'}`;
  };

  const handleAttend = async () => {
    if (!isAuthenticated) {
      alert('Please log in to attend events');
      return;
    }

    try {
      await eventsAPI.attend(id);
      setIsAttending(true);
      // Update attendees count
      setEvent(prev => ({
        ...prev,
        attendees_count: (prev.attendees_count || 0) + 1
      }));
      alert('Successfully registered for event!');
    } catch (err) {
      console.error('Error attending event:', err);
      alert('Failed to register for event. Please try again.');
    }
  };

  return (
    <div className={styles.eventDetails}>
      <div className={styles.hero}>
        <img
          src={event.image || `https://source.unsplash.com/1200x400/?${event.category || 'event'}`}
          alt={event.title}
          className={styles.heroImage}
          onError={handleHeroImageError}
        />
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
                <strong>Duration:</strong> {event.duration || 'TBD'}
              </div>
              <div className={styles.metaItem}>
                <strong>Location:</strong> {event.is_online ? 'Online event' : event.location}
              </div>
              <div className={styles.metaItem}>
                <strong>Price:</strong> {event.price || 'Free'}
              </div>
            </div>

            <div className={styles.section}>
              <h2>Details</h2>
              <p className={styles.description}>{event.description}</p>
            </div>

            {/* Event Location Map */}
            {!event.is_online && event.latitude && event.longitude && (
              <div className={styles.section}>
                <h2>Location</h2>
                <EventMap events={[event]} height="400px" zoom={15} />
              </div>
            )}

            <div className={styles.section}>
              <h2>Attendees ({event.attendees_count || 0})</h2>
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
              <button
                className={styles.attendBtn}
                onClick={handleAttend}
                disabled={isAttending}
              >
                {isAttending ? 'Attending' : 'Attend'}
              </button>
              <div className={styles.attendInfo}>
                <span>{event.attendees_count || 0} attending</span>
                {event.max_attendees && (
                  <span>{event.max_attendees - (event.attendees_count || 0)} spots left</span>
                )}
              </div>
            </div>

            {group && (
              <div className={styles.card}>
                <h3>Hosted by</h3>
                <Link to={`/groups/${group.id}`} className={styles.groupLink}>
                  <img
                    src={group.image || `https://source.unsplash.com/200x200/?community`}
                    alt={group.name}
                    className={styles.groupImage}
                    onError={handleGroupImageError}
                  />
                  <div>
                    <div className={styles.groupName}>{group.name}</div>
                    <div className={styles.groupMembers}>{(group.members_count || 0).toLocaleString()} members</div>
                  </div>
                </Link>
              </div>
            )}

            {organizer && (
              <div className={styles.card}>
                <h3>Organizer</h3>
                <Link to={`/members/${organizer.id}`} className={styles.organizerLink}>
                  <img
                    src={organizer.avatar || `https://i.pravatar.cc/150?u=${organizer.id}`}
                    alt={organizer.name}
                    className={styles.organizerAvatar}
                    onError={handleOrganizerImageError}
                  />
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
