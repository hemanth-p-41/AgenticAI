import React from 'react';
import { TextInput, View, Text } from 'react-native';

type Props = { label?: string; value: string; onChange: (v: string) => void; secure?: boolean };

export default function Input({ label, value, onChange, secure }: Props) {
  return (
    <View style={{ marginVertical: 8 }}>
      {label ? <Text style={{ marginBottom: 4 }}>{label}</Text> : null}
      <TextInput value={value} onChangeText={onChange} secureTextEntry={secure} style={{ borderWidth: 1, padding: 8, borderRadius: 6 }} />
    </View>
  );
}
