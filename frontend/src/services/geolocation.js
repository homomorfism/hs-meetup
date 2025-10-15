/**
 * Geolocation service to get user's current location
 */

/**
 * Get user's current geolocation coordinates
 * @returns {Promise<{latitude: number, longitude: number, city: string}>}
 */
export const getUserLocation = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported by your browser'));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;

        // Try to get city name from reverse geocoding
        try {
          const city = await reverseGeocode(latitude, longitude);
          resolve({ latitude, longitude, city });
        } catch (error) {
          // If reverse geocoding fails, still return coordinates
          resolve({ latitude, longitude, city: null });
        }
      },
      (error) => {
        reject(new Error(`Location access denied: ${error.message}`));
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000 // Cache for 5 minutes
      }
    );
  });
};

/**
 * Reverse geocode coordinates to city name using Google Maps API
 * @param {number} latitude
 * @param {number} longitude
 * @returns {Promise<string>}
 */
const reverseGeocode = async (latitude, longitude) => {
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

  if (!apiKey) {
    return null;
  }

  try {
    const response = await fetch(
      `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${apiKey}`
    );

    const data = await response.json();

    if (data.status === 'OK' && data.results.length > 0) {
      // Find city name from address components
      const result = data.results[0];
      const cityComponent = result.address_components.find(
        component => component.types.includes('locality')
      );

      return cityComponent ? cityComponent.long_name : null;
    }

    return null;
  } catch (error) {
    console.error('Reverse geocoding error:', error);
    return null;
  }
};

/**
 * Store user location in localStorage
 * @param {{latitude: number, longitude: number, city: string}} location
 */
export const saveUserLocation = (location) => {
  localStorage.setItem('user_location', JSON.stringify(location));
};

/**
 * Get stored user location from localStorage
 * @returns {{latitude: number, longitude: number, city: string} | null}
 */
export const getSavedUserLocation = () => {
  const stored = localStorage.getItem('user_location');
  return stored ? JSON.parse(stored) : null;
};

/**
 * Clear stored user location
 */
export const clearUserLocation = () => {
  localStorage.removeItem('user_location');
};
