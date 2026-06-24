import api from './api';

export async function uploadResume(file: any, token: string) {
  const fd = new FormData();
  fd.append('file', file);
  const r = await api.post('/resume/upload', fd, { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' } });
  return r.data;
}

export async function getResume(id: number, token: string) {
  const r = await api.get(`/resume/${id}`, { headers: { Authorization: `Bearer ${token}` } });
  return r.data;
}
