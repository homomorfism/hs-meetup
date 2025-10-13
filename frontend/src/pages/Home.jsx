import { Link } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import EventCard from '../components/EventCard';
import { events, categories } from '../data';
import styles from './Home.module.css';

export default function Home() {
  // Get upcoming events (next 8)
  const upcomingEvents = events.slice(0, 8);

  return (
    <div className={styles.home}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>The people platform</h1>
          <p className={styles.heroSubtitle}>
            Whatever your interest, from hiking and reading to networking and skill sharing,
            there are thousands of people who share it on Meetup.
          </p>
          <SearchBar />
        </div>
      </section>

      {/* Categories Section */}
      <section className={styles.section}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Explore by category</h2>
          <div className={styles.categories}>
            {categories.map(category => (
              <Link
                key={category.id}
                to={`/find?category=${category.name}`}
                className={styles.categoryCard}
              >
                <span className={styles.categoryIcon}>{category.icon}</span>
                <span className={styles.categoryName}>{category.name}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Upcoming Events Section */}
      <section className={styles.section}>
        <div className={styles.container}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>Upcoming events</h2>
            <Link to="/find" className={styles.seeAll}>See all</Link>
          </div>
          <div className={styles.eventsGrid}>
            {upcomingEvents.map(event => (
              <EventCard key={event.id} event={event} />
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className={styles.ctaSection}>
        <div className={styles.container}>
          <h2 className={styles.ctaTitle}>How Meetup works</h2>
          <div className={styles.steps}>
            <div className={styles.step}>
              <div className={styles.stepNumber}>1</div>
              <h3>Discover events</h3>
              <p>Find events that match your interests</p>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>2</div>
              <h3>Join a group</h3>
              <p>Connect with people who share your passion</p>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>3</div>
              <h3>Start meeting</h3>
              <p>Attend events and make new friends</p>
            </div>
          </div>
          <button className={styles.ctaButton}>Join Meetup</button>
        </div>
      </section>
    </div>
  );
}
