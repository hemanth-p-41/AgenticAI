import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView } from 'react-native';
import { getStudyPlan } from '../services/studyPlanService';
import { useAuth } from '../hooks/useAuth';

export default function StudyPlanScreen() {
  const { token } = useAuth();
  const [plan, setPlan] = useState<any>(null);

  useEffect(() => {
    if (token) getStudyPlan(token).then(setPlan).catch(console.warn);
  }, [token]);

  return (
    <ScrollView style={{ padding: 16 }}>
      <Text style={{ fontSize: 20 }}>Study Plan</Text>
      {plan ? (
        <View>
          <Text style={{ marginTop: 8, fontWeight: '600' }}>3 Day</Text>
          {plan.three_day_plan.map((t: any) => <Text key={t.day}>{t.task}</Text>)}
          <Text style={{ marginTop: 8, fontWeight: '600' }}>7 Day</Text>
          {plan.seven_day_plan.map((t: any) => <Text key={t.day}>{t.task}</Text>)}
        </View>
      ) : (
        <Text>Loading...</Text>
      )}
    </ScrollView>
  );
}
