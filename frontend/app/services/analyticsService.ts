import api from './api';

export async function getAnalytics(token: string) {
  const r = await api.get('/analytics/me', { headers: { Authorization: `Bearer ${token}` } });
  return r.data;
}

export async function getTrends(token: string) {
  const r = await api.get('/analytics/trends', { headers: { Authorization: `Bearer ${token}` } });
  return r.data;
}
