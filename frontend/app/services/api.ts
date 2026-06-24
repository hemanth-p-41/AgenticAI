import axios from 'axios';

const API_BASE = process.env.BACKEND_URL || 'http://localhost:8000';

const api = axios.create({ baseURL: API_BASE, timeout: 10000 });

export default api;
