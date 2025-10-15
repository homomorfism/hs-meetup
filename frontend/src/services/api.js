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
      body: JSON.stringify({
        email: credentials.username || credentials.email,
        password: credentials.password,
      }),
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

  getAttending: async (id) => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/attending`);
    return handleResponse(response);
  },

  getGroups: async (id) => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/groups`);
    return handleResponse(response);
  },

  getFriends: async (id) => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/friends`);
    return handleResponse(response);
  },

  addFriend: async (userId, friendId) => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/friends/${friendId}`, {
      method: 'POST',
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  removeFriend: async (userId, friendId) => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/friends/${friendId}`, {
      method: 'DELETE',
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },
};

// Chat API
export const chatAPI = {
  getConversations: async () => {
    const response = await fetch(`${API_BASE_URL}/chats`, {
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  getOrCreateConversation: async (friendId) => {
    const response = await fetch(`${API_BASE_URL}/chats`, {
      method: 'POST',
      headers: createHeaders(true),
      body: JSON.stringify({ friend_id: friendId }),
    });
    return handleResponse(response);
  },

  getMessages: async (chatId) => {
    const response = await fetch(`${API_BASE_URL}/chats/${chatId}/messages`, {
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  sendMessage: async (chatId, content) => {
    const response = await fetch(`${API_BASE_URL}/chats/${chatId}/messages`, {
      method: 'POST',
      headers: createHeaders(true),
      body: JSON.stringify({ content }),
    });
    return handleResponse(response);
  },
};

// Saved Searches API
export const savedSearchesAPI = {
  getAll: async () => {
    const response = await fetch(`${API_BASE_URL}/saved-searches`, {
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  getById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/saved-searches/${id}`, {
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  create: async (searchData) => {
    const response = await fetch(`${API_BASE_URL}/saved-searches`, {
      method: 'POST',
      headers: createHeaders(true),
      body: JSON.stringify(searchData),
    });
    return handleResponse(response);
  },

  update: async (id, searchData) => {
    const response = await fetch(`${API_BASE_URL}/saved-searches/${id}`, {
      method: 'PUT',
      headers: createHeaders(true),
      body: JSON.stringify(searchData),
    });
    return handleResponse(response);
  },

  delete: async (id) => {
    const response = await fetch(`${API_BASE_URL}/saved-searches/${id}`, {
      method: 'DELETE',
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },
};

// Search History API
export const searchHistoryAPI = {
  getAll: async (limit = 10) => {
    const response = await fetch(`${API_BASE_URL}/search-history?limit=${limit}`, {
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  create: async (searchData) => {
    const response = await fetch(`${API_BASE_URL}/search-history`, {
      method: 'POST',
      headers: createHeaders(true),
      body: JSON.stringify(searchData),
    });
    return handleResponse(response);
  },

  delete: async (id) => {
    const response = await fetch(`${API_BASE_URL}/search-history/${id}`, {
      method: 'DELETE',
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  clear: async () => {
    const response = await fetch(`${API_BASE_URL}/search-history`, {
      method: 'DELETE',
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },
};
