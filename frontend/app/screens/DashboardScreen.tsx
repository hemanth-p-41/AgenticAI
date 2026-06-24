import React, { useEffect, useState } from 'react';
import { View, Text, Button as RNButton } from 'react-native';
import { getAnalytics } from '../services/analyticsService';
import { useAuth } from '../hooks/useAuth';

export default function DashboardScreen({ navigation }: any) {
  const { token } = useAuth();
  const [analytics, setAnalytics] = useState<any>(null);

  useEffect(() => {
    if (token) getAnalytics(token).then(setAnalytics).catch(console.warn);
  }, [token]);

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 24 }}>Dashboard</Text>
      {analytics ? (
        <View style={{ marginTop: 12 }}>
          <Text>Overall: {analytics.overall_score.toFixed(1)}</Text>
          <Text>Strongest: {analytics.strongest_area}</Text>
          <Text>Weakest: {analytics.weakest_area}</Text>
        </View>
      ) : (
        <Text>Loading...</Text>
      )}
      <View style={{ marginTop: 12 }}>
        <RNButton title="Create Interview" onPress={() => navigation.navigate('CreateInterview')} />
      </View>
    </View>
  );
}
