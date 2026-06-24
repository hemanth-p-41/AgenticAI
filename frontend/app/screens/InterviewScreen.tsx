import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';
import Input from '../components/Input';
import Button from '../components/Button';
import { nextQuestion, submitAnswer } from '../services/interviewService';
import { useAuth } from '../hooks/useAuth';

export default function InterviewScreen({ route }: any) {
  const { interviewId } = route.params;
  const { token } = useAuth();
  const [question, setQuestion] = useState<any>(null);
  const [answer, setAnswer] = useState('');

  const loadNext = async () => {
    const q = await nextQuestion(interviewId, token as string);
    setQuestion(q);
    setAnswer('');
  };

  useEffect(() => {
    loadNext();
  }, []);

  const handleSubmit = async () => {
    if (!question) return;
    await submitAnswer(question.question_id, answer, token as string);
    await loadNext();
  };

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 20 }}>Interview</Text>
      {question ? <Text style={{ marginVertical: 12 }}>{question.question}</Text> : <Text>No question</Text>}
      <Input label="Your Answer" value={answer} onChange={setAnswer} />
      <Button title="Submit Answer" onPress={handleSubmit} />
    </View>
  );
}
