import { Link } from 'react-router-dom';
import styles from './Header.module.css';

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link to="/" className={styles.logo}>
          Meetup
        </Link>
        <nav className={styles.nav}>
          <Link to="/find" className={styles.navLink}>Find events</Link>
          <Link to="/groups" className={styles.navLink}>Groups</Link>
        </nav>
        <div className={styles.actions}>
          <button className={styles.loginBtn}>Log in</button>
          <button className={styles.signupBtn}>Sign up</button>
        </div>
      </div>
    </header>
  );
}
