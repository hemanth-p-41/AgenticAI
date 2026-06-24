import api from './api';

export async function getStudyPlan(token: string) {
  const r = await api.get('/study-plan/me', { headers: { Authorization: `Bearer ${token}` } });
  return r.data;
}
