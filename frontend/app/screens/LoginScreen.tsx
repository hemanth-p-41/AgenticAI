import React, { useState } from 'react';
import { View, Text } from 'react-native';
import Input from '../components/Input';
import Button from '../components/Button';
import { login } from '../services/authService';
import { useAuth } from '../hooks/useAuth';

export default function LoginScreen({ navigation }: any) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { setToken } = useAuth();

  const handleLogin = async () => {
    try {
      const data = await login(email, password);
      setToken(data.access_token);
    } catch (err) {
      console.warn(err);
    }
  };

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 24, marginBottom: 16 }}>Login</Text>
      <Input label="Email" value={email} onChange={setEmail} />
      <Input label="Password" value={password} onChange={setPassword} secure />
      <Button title="Login" onPress={handleLogin} />
      <View style={{ marginTop: 12 }}>
        <Button title="Register" onPress={() => navigation.navigate('Register')} />
      </View>
    </View>
  );
}
