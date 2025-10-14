import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import styles from './Header.module.css';

export default function Header() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link to="/" className={styles.logo}>
          Meetup
        </Link>
        <nav className={styles.nav}>
          <Link to="/find" className={styles.navLink}>Find events</Link>
          <Link to="/groups" className={styles.navLink}>Groups</Link>
          {isAuthenticated && (
            <>
              <Link to="/profile" className={styles.navLink}>My Profile</Link>
              <Link to="/chat" className={styles.navLink}>Messages</Link>
            </>
          )}
        </nav>
        <div className={styles.actions}>
          {isAuthenticated ? (
            <>
              <span className={styles.userName}>Hi, {user?.name}</span>
              <button onClick={handleLogout} className={styles.logoutBtn}>
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className={styles.loginBtn}>
                Log in
              </Link>
              <Link to="/signup" className={styles.signupBtn}>
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
