import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import styles from './Login.module.css';

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const from = location.state?.from?.pathname || '/';

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.email || !formData.password) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    const result = await login(formData.email, formData.password);
    setLoading(false);

    if (result.success) {
      navigate(from, { replace: true });
    } else {
      setError(result.error || 'Login failed. Please try again.');
    }
  };

  return (
    <div className={styles.loginPage}>
      <div className={styles.container}>
        <div className={styles.loginCard}>
          <h1 className={styles.title}>Log in to Meetup</h1>
          <p className={styles.subtitle}>Welcome back! Please enter your details.</p>

          {error && <div className={styles.error}>{error}</div>}

          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.formGroup}>
              <label htmlFor="email" className={styles.label}>
                Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={styles.input}
                placeholder="Enter your email"
                disabled={loading}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="password" className={styles.label}>
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={styles.input}
                placeholder="Enter your password"
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              className={styles.submitBtn}
              disabled={loading}
            >
              {loading ? 'Logging in...' : 'Log in'}
            </button>
          </form>

          <p className={styles.footer}>
            Don't have an account?{' '}
            <Link to="/signup" className={styles.link}>
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
