import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';
import { getAnalytics, getTrends } from '../services/analyticsService';
import { useAuth } from '../hooks/useAuth';

export default function AnalyticsScreen() {
  const { token } = useAuth();
  const [analytics, setAnalytics] = useState<any>(null);
  const [trends, setTrends] = useState<any>(null);

  useEffect(() => {
    if (token) {
      getAnalytics(token).then(setAnalytics).catch(console.warn);
      getTrends(token).then(setTrends).catch(console.warn);
    }
  }, [token]);

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 20 }}>Analytics</Text>
      {analytics ? (
        <View>
          {Object.entries(analytics.categories || {}).map(([k, v]) => (
            <Text key={k}>{k}: {Number(v).toFixed(1)}</Text>
          ))}
        </View>
      ) : (
        <Text>Loading...</Text>
      )}
      {trends ? <Text>Recent: {trends.history.join(', ')}</Text> : null}
    </View>
  );
}
