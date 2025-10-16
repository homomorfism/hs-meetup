import { Link } from 'react-router-dom';
import styles from './Footer.module.css';

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div className={styles.section}>
          <h3>Your Account</h3>
          <ul>
            <li><Link to="/signup">Sign up</Link></li>
            <li><Link to="/login">Log in</Link></li>
          </ul>
        </div>
        <div className={styles.section}>
          <h3>Discover</h3>
          <ul>
            <li><Link to="/find">Events</Link></li>
            <li><Link to="/groups">Groups</Link></li>
          </ul>
        </div>
        <div className={styles.copyright}>
          <p>&copy; 2025 Meetup Clone</p>
        </div>
      </div>
    </footer>
  );
}
