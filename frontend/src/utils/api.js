// utils/api.js
// Utility for making API calls using fetch

const API_BASE_URL = 'http://localhost:8000';   // Adjust as needed
export async function apiCall(url, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      },
      ...options
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'API Error');
    }
    return data;
  } catch (error) {
    throw error;
  }
}
