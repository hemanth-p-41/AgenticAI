import React, { useState } from 'react';
import { View, Text } from 'react-native';
import Input from '../components/Input';
import Button from '../components/Button';
import { register } from '../services/authService';

export default function RegisterScreen({ navigation }: any) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    try {
      await register(name, email, password);
      navigation.navigate('Login');
    } catch (err) {
      console.warn(err);
    }
  };

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 24, marginBottom: 16 }}>Register</Text>
      <Input label="Name" value={name} onChange={setName} />
      <Input label="Email" value={email} onChange={setEmail} />
      <Input label="Password" value={password} onChange={setPassword} secure />
      <Button title="Register" onPress={handleRegister} />
    </View>
  );
}
