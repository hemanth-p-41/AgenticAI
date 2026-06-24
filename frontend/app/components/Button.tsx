import React from 'react';
import { TouchableOpacity, Text } from 'react-native';

export default function Button({ title, onPress }: { title: string; onPress: () => void }) {
  return (
    <TouchableOpacity onPress={onPress} style={{ backgroundColor: '#2563eb', padding: 12, borderRadius: 6, alignItems: 'center' }}>
      <Text style={{ color: 'white', fontWeight: '600' }}>{title}</Text>
    </TouchableOpacity>
  );
}
