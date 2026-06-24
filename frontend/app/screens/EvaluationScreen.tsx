import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';
import { useAuth } from '../hooks/useAuth';
import { getAnalytics } from '../services/analyticsService';

export default function EvaluationScreen() {
  const { token } = useAuth();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (token) getAnalytics(token).then(setData).catch(console.warn);
  }, [token]);

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 20 }}>Evaluation</Text>
      {data ? (
        <View style={{ marginTop: 12 }}>
          <Text>Overall: {data.overall_score.toFixed(1)}</Text>
        </View>
      ) : (
        <Text>Loading...</Text>
      )}
    </View>
  );
}
