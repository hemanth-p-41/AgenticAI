import React, { useState } from 'react';
import { View, Text } from 'react-native';
import Input from '../components/Input';
import Button from '../components/Button';
import { createInterview } from '../services/interviewService';
import { useAuth } from '../hooks/useAuth';

export default function CreateInterviewScreen({ navigation }: any) {
  const [company, setCompany] = useState('');
  const [role, setRole] = useState('');
  const [resumeId, setResumeId] = useState<number | null>(null);
  const { token } = useAuth();

  const handleCreate = async () => {
    if (!resumeId) return;
    const r = await createInterview({ company, role, resume_id: resumeId }, token as string);
    navigation.navigate('Interview', { interviewId: r.interview_id });
  };

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 20 }}>Create Interview</Text>
      <Input label="Company" value={company} onChange={setCompany} />
      <Input label="Role" value={role} onChange={setRole} />
      <Input label="Resume ID" value={resumeId ? String(resumeId) : ''} onChange={(v) => setResumeId(Number(v) || null)} />
      <Button title="Create Interview" onPress={handleCreate} />
    </View>
  );
}
