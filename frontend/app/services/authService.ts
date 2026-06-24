import api from './api';

export async function login(email: string, password: string) {
  const r = await api.post('/auth/login', { email, password });
  return r.data;
}

export async function register(name: string, email: string, password: string) {
  const r = await api.post('/auth/register', { name, email, password });
  return r.data;
}
