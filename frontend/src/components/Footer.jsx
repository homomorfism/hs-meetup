import styles from './Footer.module.css';

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div className={styles.section}>
          <h3>Your Account</h3>
          <ul>
            <li><a href="#">Sign up</a></li>
            <li><a href="#">Log in</a></li>
            <li><a href="#">Help</a></li>
          </ul>
        </div>
        <div className={styles.section}>
          <h3>Discover</h3>
          <ul>
            <li><a href="#">Groups</a></li>
            <li><a href="#">Calendar</a></li>
            <li><a href="#">Topics</a></li>
            <li><a href="#">Cities</a></li>
          </ul>
        </div>
        <div className={styles.section}>
          <h3>Meetup</h3>
          <ul>
            <li><a href="#">About</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Careers</a></li>
            <li><a href="#">Apps</a></li>
          </ul>
        </div>
        <div className={styles.copyright}>
          <p>&copy; 2025 Meetup Clone</p>
        </div>
      </div>
    </footer>
  );
}
