import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import styles from './Login.module.css';

export default function Signup() {
  const navigate = useNavigate();
  const { signup } = useAuth();

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    location: '',
    bio: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

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

    // Validation
    if (!formData.name || !formData.email || !formData.password || !formData.confirmPassword) {
      setError('Please fill in all required fields');
      return;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    const result = await signup({
      name: formData.name,
      email: formData.email,
      password: formData.password,
      location: formData.location || null,
      bio: formData.bio || null,
    });
    setLoading(false);

    if (result.success) {
      navigate('/', { replace: true });
    } else {
      setError(result.error || 'Signup failed. Please try again.');
    }
  };

  return (
    <div className={styles.loginPage}>
      <div className={styles.container}>
        <div className={styles.loginCard}>
          <h1 className={styles.title}>Sign up for Meetup</h1>
          <p className={styles.subtitle}>Join the community and discover events near you.</p>

          {error && <div className={styles.error}>{error}</div>}

          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.formGroup}>
              <label htmlFor="name" className={styles.label}>
                Name *
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className={styles.input}
                placeholder="Enter your full name"
                disabled={loading}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="email" className={styles.label}>
                Email *
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
                Password *
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={styles.input}
                placeholder="Create a password"
                disabled={loading}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="confirmPassword" className={styles.label}>
                Confirm Password *
              </label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={styles.input}
                placeholder="Confirm your password"
                disabled={loading}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="location" className={styles.label}>
                Location
              </label>
              <input
                type="text"
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                className={styles.input}
                placeholder="e.g., San Francisco, CA"
                disabled={loading}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="bio" className={styles.label}>
                Bio
              </label>
              <textarea
                id="bio"
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                className={styles.input}
                placeholder="Tell us about yourself..."
                rows="3"
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              className={styles.submitBtn}
              disabled={loading}
            >
              {loading ? 'Creating account...' : 'Sign up'}
            </button>
          </form>

          <p className={styles.footer}>
            Already have an account?{' '}
            <Link to="/login" className={styles.link}>
              Log in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
