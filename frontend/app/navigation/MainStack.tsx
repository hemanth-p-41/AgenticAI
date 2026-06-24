import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import DashboardScreen from '../screens/DashboardScreen';
import ResumeScreen from '../screens/ResumeScreen';
import CreateInterviewScreen from '../screens/CreateInterviewScreen';
import InterviewScreen from '../screens/InterviewScreen';
import EvaluationScreen from '../screens/EvaluationScreen';
import AnalyticsScreen from '../screens/AnalyticsScreen';
import StudyPlanScreen from '../screens/StudyPlanScreen';

const Stack = createNativeStackNavigator();

export default function MainStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Dashboard" component={DashboardScreen} />
      <Stack.Screen name="Resume" component={ResumeScreen} />
      <Stack.Screen name="CreateInterview" component={CreateInterviewScreen} />
      <Stack.Screen name="Interview" component={InterviewScreen} />
      <Stack.Screen name="Evaluation" component={EvaluationScreen} />
      <Stack.Screen name="Analytics" component={AnalyticsScreen} />
      <Stack.Screen name="StudyPlan" component={StudyPlanScreen} />
    </Stack.Navigator>
  );
}
