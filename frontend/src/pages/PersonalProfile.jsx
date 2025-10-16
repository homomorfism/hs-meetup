import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { usersAPI } from '../services/api';
import EventCard from '../components/EventCard';
import GroupCard from '../components/GroupCard';
import UserCard from '../components/UserCard';
import styles from './PersonalProfile.module.css';

export default function PersonalProfile() {
  const { user, updateUser } = useAuth();
  const [organizedEvents, setOrganizedEvents] = useState([]);
  const [attendingEvents, setAttendingEvents] = useState([]);
  const [groups, setGroups] = useState([]);
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditingBio, setIsEditingBio] = useState(false);
  const [bioText, setBioText] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [profileData, setProfileData] = useState({ name: '', location: '', avatar: '' });

  useEffect(() => {
    const fetchUserData = async () => {
      if (!user) return;

      try {
        setLoading(true);
        const [organized, attending, userGroups, friendsList] = await Promise.all([
          usersAPI.getEvents(user.id),
          usersAPI.getAttending(user.id),
          usersAPI.getGroups(user.id).catch(() => []),
          usersAPI.getFriends(user.id).catch(() => []), // Friends endpoint might not exist yet
        ]);

        setOrganizedEvents(organized);
        setAttendingEvents(attending);
        setGroups(userGroups);
        setFriends(friendsList);

        console.log('Profile data loaded:', {
          groups: userGroups.length,
          upcomingEvents: attending.filter(e => new Date(e.date) >= new Date()).length,
          friends: friendsList.length
        });
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

  const handleEditBio = () => {
    setBioText(user.bio || '');
    setIsEditingBio(true);
  };

  const handleSaveBio = async () => {
    try {
      setIsSaving(true);
      await usersAPI.update(user.id, { bio: bioText });
      updateUser({ ...user, bio: bioText });
      setIsEditingBio(false);
      alert('Bio updated successfully!');
    } catch (err) {
      console.error('Error updating bio:', err);
      alert('Failed to update bio. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancelEdit = () => {
    setIsEditingBio(false);
    setBioText('');
  };

  const handleEditProfile = () => {
    setProfileData({
      name: user.name || '',
      location: user.location || '',
      avatar: user.avatar || ''
    });
    setIsEditingProfile(true);
  };

  const handleSaveProfile = async () => {
    try {
      setIsSaving(true);
      await usersAPI.update(user.id, profileData);
      updateUser({ ...user, ...profileData });
      setIsEditingProfile(false);
      alert('Profile updated successfully!');
    } catch (err) {
      console.error('Error updating profile:', err);
      alert('Failed to update profile. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancelProfileEdit = () => {
    setIsEditingProfile(false);
    setProfileData({ name: '', location: '', avatar: '' });
  };

  const now = new Date();
  const upcomingEvents = attendingEvents.filter(event => new Date(event.date) >= now);
  const pastEvents = attendingEvents.filter(event => new Date(event.date) < now);

  return (
    <div className={styles.personalProfile}>
      <div className={styles.header}>
        <div className={styles.container}>
          {isEditingProfile ? (
            <div className={styles.headerContent}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '2rem' }}>
                  <div>
                    <img
                      src={profileData.avatar || 'https://i.pravatar.cc/300?img=1'}
                      alt="Profile"
                      className={styles.avatar}
                      onError={(e) => {
                        e.target.src = 'https://i.pravatar.cc/300?img=1';
                      }}
                    />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ marginBottom: '1rem' }}>
                      <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold', color: '#333' }}>
                        Profile Picture URL
                      </label>
                      <input
                        type="text"
                        value={profileData.avatar}
                        onChange={(e) => setProfileData({ ...profileData, avatar: e.target.value })}
                        placeholder="Enter image URL (e.g., https://i.imgur.com/example.jpg)"
                        style={{
                          width: '100%',
                          padding: '0.5rem',
                          border: '1px solid #ddd',
                          borderRadius: '4px',
                          fontSize: '0.875rem'
                        }}
                      />
                      <div style={{ fontSize: '0.75rem', color: '#666', marginTop: '0.25rem' }}>
                        Use image URLs from Imgur, i.pravatar.cc, or other image hosting services
                      </div>
                    </div>
                    <div style={{ marginBottom: '1rem' }}>
                      <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold', color: '#333' }}>
                        Name
                      </label>
                      <input
                        type="text"
                        value={profileData.name}
                        onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
                        placeholder="Enter your name"
                        style={{
                          width: '100%',
                          padding: '0.5rem',
                          border: '1px solid #ddd',
                          borderRadius: '4px',
                          fontSize: '0.875rem'
                        }}
                      />
                    </div>
                    <div style={{ marginBottom: '1rem' }}>
                      <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold', color: '#333' }}>
                        Location
                      </label>
                      <input
                        type="text"
                        value={profileData.location}
                        onChange={(e) => setProfileData({ ...profileData, location: e.target.value })}
                        placeholder="Enter your location"
                        style={{
                          width: '100%',
                          padding: '0.5rem',
                          border: '1px solid #ddd',
                          borderRadius: '4px',
                          fontSize: '0.875rem'
                        }}
                      />
                    </div>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      <button
                        onClick={handleSaveProfile}
                        disabled={isSaving}
                        style={{
                          padding: '0.5rem 1.5rem',
                          background: '#00798a',
                          color: 'white',
                          border: 'none',
                          borderRadius: '4px',
                          cursor: isSaving ? 'not-allowed' : 'pointer',
                          fontSize: '0.875rem',
                          opacity: isSaving ? 0.6 : 1
                        }}
                      >
                        {isSaving ? 'Saving...' : 'Save'}
                      </button>
                      <button
                        onClick={handleCancelProfileEdit}
                        disabled={isSaving}
                        style={{
                          padding: '0.5rem 1.5rem',
                          background: '#ccc',
                          color: '#333',
                          border: 'none',
                          borderRadius: '4px',
                          cursor: isSaving ? 'not-allowed' : 'pointer',
                          fontSize: '0.875rem'
                        }}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className={styles.headerContent}>
              <img
                src={user.avatar || 'https://i.pravatar.cc/300?img=1'}
                alt={user.name}
                className={styles.avatar}
                onError={(e) => {
                  e.target.src = 'https://i.pravatar.cc/300?img=1';
                }}
              />
              <div className={styles.headerInfo}>
                <h1 className={styles.name}>{user.name}</h1>
                <div className={styles.location}>{user.location || 'No location set'}</div>
                <div className={styles.memberSince}>
                  Member since {formatDate(user.member_since)}
                </div>
              </div>
              <button
                onClick={handleEditProfile}
                style={{
                  padding: '0.5rem 1.5rem',
                  background: '#00798a',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '0.875rem',
                  marginLeft: 'auto'
                }}
              >
                Edit Profile
              </button>
            </div>
          )}
        </div>
      </div>

      <div className={styles.container}>
        <div className={styles.layout}>
          <aside className={styles.sidebar}>
            <div className={styles.card}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 className={styles.cardTitle}>About</h2>
                {!isEditingBio && (
                  <button
                    onClick={handleEditBio}
                    style={{
                      padding: '0.5rem 1rem',
                      background: '#00798a',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontSize: '0.875rem'
                    }}
                  >
                    Edit
                  </button>
                )}
              </div>
              {isEditingBio ? (
                <div>
                  <textarea
                    value={bioText}
                    onChange={(e) => setBioText(e.target.value)}
                    placeholder="Tell us about yourself..."
                    rows={6}
                    style={{
                      width: '100%',
                      padding: '0.75rem',
                      border: '1px solid #ddd',
                      borderRadius: '4px',
                      fontSize: '0.875rem',
                      fontFamily: 'inherit',
                      resize: 'vertical'
                    }}
                  />
                  <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem' }}>
                    <button
                      onClick={handleSaveBio}
                      disabled={isSaving}
                      style={{
                        padding: '0.5rem 1rem',
                        background: '#00798a',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: isSaving ? 'not-allowed' : 'pointer',
                        fontSize: '0.875rem',
                        opacity: isSaving ? 0.6 : 1
                      }}
                    >
                      {isSaving ? 'Saving...' : 'Save'}
                    </button>
                    <button
                      onClick={handleCancelEdit}
                      disabled={isSaving}
                      style={{
                        padding: '0.5rem 1rem',
                        background: '#ccc',
                        color: '#333',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: isSaving ? 'not-allowed' : 'pointer',
                        fontSize: '0.875rem'
                      }}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <p className={styles.bio}>{user.bio || 'No bio added yet.'}</p>
              )}
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
            {groups.length > 0 && (
              <section className={styles.section}>
                <h2 className={styles.sectionTitle}>
                  My Groups ({groups.length})
                </h2>
                <div className={styles.eventsGrid}>
                  {groups.map((group) => (
                    <GroupCard key={group.id} group={group} />
                  ))}
                </div>
              </section>
            )}

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

            {groups.length === 0 &&
              upcomingEvents.length === 0 &&
              pastEvents.length === 0 &&
              organizedEvents.length === 0 && (
                <div className={styles.emptyState}>
                  <h3>No groups or events yet</h3>
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
