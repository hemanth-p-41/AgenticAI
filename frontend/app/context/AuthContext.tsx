import React, { createContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

type AuthContextValue = {
  token: string | null;
  user: any | null;
  setToken: (t: string | null) => void;
};

export const AuthContext = createContext<AuthContextValue>({ token: null, user: null, setToken: () => {} });

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setTokenState] = useState<string | null>(null);
  const [user, setUser] = useState<any | null>(null);

  useEffect(() => {
    AsyncStorage.getItem('token').then((t) => {
      if (t) setTokenState(t);
    });
  }, []);

  const setToken = async (t: string | null) => {
    if (t) {
      await AsyncStorage.setItem('token', t);
      setTokenState(t);
    } else {
      await AsyncStorage.removeItem('token');
      setTokenState(null);
    }
  };

  return <AuthContext.Provider value={{ token, user, setToken }}>{children}</AuthContext.Provider>;
};
