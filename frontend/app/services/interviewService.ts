import api from './api';

export async function createInterview(payload: { company: string; role: string; resume_id: number }, token: string) {
  const r = await api.post('/interview/create', payload, { headers: { Authorization: `Bearer ${token}` } });
  return r.data;
}

export async function nextQuestion(interview_id: number, token: string) {
  const r = await api.get(`/interview/${interview_id}/next`, { headers: { Authorization: `Bearer ${token}` } });
  return r.data;
}

export async function submitAnswer(question_id: number, answer: string, token: string) {
  const r = await api.post('/interview/answer', { question_id, answer }, { headers: { Authorization: `Bearer ${token}` } });
  return r.data;
}
