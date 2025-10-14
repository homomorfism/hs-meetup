const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || `HTTP error ${response.status}`);
  }
  return response.json();
};

// Helper function to get auth token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('token');
};

// Helper function to create headers
const createHeaders = (includeAuth = false) => {
  const headers = {
    'Content-Type': 'application/json',
  };
  if (includeAuth) {
    const token = getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }
  return headers;
};

// Authentication API
export const authAPI = {
  signup: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: createHeaders(),
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },

  login: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: createHeaders(),
      body: JSON.stringify(credentials),
    });
    return handleResponse(response);
  },

  getMe: async () => {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },
};

// Categories API
export const categoriesAPI = {
  getAll: async () => {
    const response = await fetch(`${API_BASE_URL}/categories`);
    return handleResponse(response);
  },
};

// Events API
export const eventsAPI = {
  getAll: async (filters = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
        params.append(key, value);
      }
    });
    const url = `${API_BASE_URL}/events${params.toString() ? '?' + params.toString() : ''}`;
    const response = await fetch(url);
    return handleResponse(response);
  },

  getById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/events/${id}`);
    return handleResponse(response);
  },

  create: async (eventData) => {
    const response = await fetch(`${API_BASE_URL}/events`, {
      method: 'POST',
      headers: createHeaders(true),
      body: JSON.stringify(eventData),
    });
    return handleResponse(response);
  },

  update: async (id, eventData) => {
    const response = await fetch(`${API_BASE_URL}/events/${id}`, {
      method: 'PUT',
      headers: createHeaders(true),
      body: JSON.stringify(eventData),
    });
    return handleResponse(response);
  },

  attend: async (id) => {
    const response = await fetch(`${API_BASE_URL}/events/${id}/attend`, {
      method: 'POST',
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  getAttendees: async (id) => {
    const response = await fetch(`${API_BASE_URL}/events/${id}/attendees`);
    return handleResponse(response);
  },
};

// Groups API
export const groupsAPI = {
  getAll: async (filters = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
        params.append(key, value);
      }
    });
    const url = `${API_BASE_URL}/groups${params.toString() ? '?' + params.toString() : ''}`;
    const response = await fetch(url);
    return handleResponse(response);
  },

  getById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/groups/${id}`);
    return handleResponse(response);
  },

  create: async (groupData) => {
    const response = await fetch(`${API_BASE_URL}/groups`, {
      method: 'POST',
      headers: createHeaders(true),
      body: JSON.stringify(groupData),
    });
    return handleResponse(response);
  },

  update: async (id, groupData) => {
    const response = await fetch(`${API_BASE_URL}/groups/${id}`, {
      method: 'PUT',
      headers: createHeaders(true),
      body: JSON.stringify(groupData),
    });
    return handleResponse(response);
  },

  join: async (id) => {
    const response = await fetch(`${API_BASE_URL}/groups/${id}/join`, {
      method: 'POST',
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  getEvents: async (id) => {
    const response = await fetch(`${API_BASE_URL}/groups/${id}/events`);
    return handleResponse(response);
  },

  getMembers: async (id) => {
    const response = await fetch(`${API_BASE_URL}/groups/${id}/members`);
    return handleResponse(response);
  },
};

// Users API
export const usersAPI = {
  getAll: async () => {
    const response = await fetch(`${API_BASE_URL}/users`);
    return handleResponse(response);
  },

  getById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/users/${id}`);
    return handleResponse(response);
  },

  update: async (id, userData) => {
    const response = await fetch(`${API_BASE_URL}/users/${id}`, {
      method: 'PUT',
      headers: createHeaders(true),
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },

  getEvents: async (id) => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/events`);
    return handleResponse(response);
  },

  getGroups: async (id) => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/groups`);
    return handleResponse(response);
  },
};
