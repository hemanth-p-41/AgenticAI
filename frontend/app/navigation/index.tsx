import React from 'react';
import { useAuth } from '../hooks/useAuth';
import AuthStack from './AuthStack';
import MainStack from './MainStack';

export default function RootNavigator() {
  const { token } = useAuth();
  return token ? <MainStack /> : <AuthStack />;
}
