import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { AuthProvider } from './app/context/AuthContext';
import RootNavigator from './app/navigation';
import { SafeAreaView, StatusBar } from 'react-native';

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <AuthProvider>
        <NavigationContainer>
          <StatusBar barStyle="dark-content" />
          <SafeAreaView style={{ flex: 1 }}>
            <RootNavigator />
          </SafeAreaView>
        </NavigationContainer>
      </AuthProvider>
    </GestureHandlerRootView>
  );
}
