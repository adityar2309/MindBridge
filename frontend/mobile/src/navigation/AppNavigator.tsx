import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { useAppSelector, useAppDispatch, useTheme } from '@/utils/hooks';
import { loadStoredAuth } from '@/store/slices/authSlice';
import { RootStackParamList, MainTabParamList } from '@/types';
import { lightTheme, darkTheme } from '@/constants/theme';

// Screen imports
import WelcomeScreen from '@/screens/auth/WelcomeScreen';
import LoginScreen from '@/screens/auth/LoginScreen';
import RegisterScreen from '@/screens/auth/RegisterScreen';
import HomeScreen from '@/screens/main/HomeScreen';
import CheckinScreen from '@/screens/main/CheckinScreen';
import AnalyticsScreen from '@/screens/main/AnalyticsScreen';
import ProfileScreen from '@/screens/main/ProfileScreen';
import SettingsScreen from '@/screens/main/SettingsScreen';
import CheckinFlowScreen from '@/screens/checkin/CheckinFlowScreen';
import HistoryScreen from '@/screens/main/HistoryScreen';

const RootStack = createStackNavigator<RootStackParamList>();
const MainTab = createBottomTabNavigator<MainTabParamList>();

/**
 * Main tab navigator for authenticated users.
 */
const MainTabNavigator: React.FC = () => {
  const { isDarkMode } = useTheme();
  const theme = isDarkMode ? darkTheme : lightTheme;

  return (
    <MainTab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: string;

          switch (route.name) {
            case 'Home':
              iconName = 'home';
              break;
            case 'Checkin':
              iconName = 'add-circle';
              break;
            case 'Analytics':
              iconName = 'analytics';
              break;
            case 'Profile':
              iconName = 'person';
              break;
            default:
              iconName = 'circle';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: theme.colors.textSecondary,
        tabBarStyle: {
          backgroundColor: theme.colors.surface,
          borderTopColor: theme.colors.border,
          paddingTop: theme.spacing.xs,
          paddingBottom: theme.spacing.sm,
          height: 60,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '500',
        },
        headerStyle: {
          backgroundColor: theme.colors.background,
          elevation: 0,
          shadowOpacity: 0,
          borderBottomWidth: 1,
          borderBottomColor: theme.colors.border,
        },
        headerTitleStyle: {
          color: theme.colors.text,
          fontSize: 18,
          fontWeight: '600',
        },
        headerTintColor: theme.colors.primary,
      })}
    >
      <MainTab.Screen 
        name="Home" 
        component={HomeScreen}
        options={{ title: 'Home' }}
      />
      <MainTab.Screen 
        name="Checkin" 
        component={CheckinScreen}
        options={{ title: 'Check-in' }}
      />
      <MainTab.Screen 
        name="Analytics" 
        component={AnalyticsScreen}
        options={{ title: 'Analytics' }}
      />
      <MainTab.Screen 
        name="Profile" 
        component={ProfileScreen}
        options={{ title: 'Profile' }}
      />
    </MainTab.Navigator>
  );
};

/**
 * Authentication stack navigator for non-authenticated users.
 */
const AuthStackNavigator: React.FC = () => {
  const { isDarkMode } = useTheme();
  const theme = isDarkMode ? darkTheme : lightTheme;

  return (
    <RootStack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: theme.colors.background,
          elevation: 0,
          shadowOpacity: 0,
        },
        headerTitleStyle: {
          color: theme.colors.text,
          fontSize: 18,
          fontWeight: '600',
        },
        headerTintColor: theme.colors.primary,
        cardStyle: {
          backgroundColor: theme.colors.background,
        },
      }}
    >
      <RootStack.Screen 
        name="Welcome" 
        component={WelcomeScreen}
        options={{ headerShown: false }}
      />
      <RootStack.Screen 
        name="Login" 
        component={LoginScreen}
        options={{ title: 'Sign In' }}
      />
      <RootStack.Screen 
        name="Register" 
        component={RegisterScreen}
        options={{ title: 'Create Account' }}
      />
    </RootStack.Navigator>
  );
};

/**
 * Main app navigator that handles authentication flow.
 */
const AppNavigator: React.FC = () => {
  const dispatch = useAppDispatch();
  const { isAuthenticated, isLoading } = useAppSelector(state => state.auth);
  const { isDarkMode } = useTheme();
  const theme = isDarkMode ? darkTheme : lightTheme;

  useEffect(() => {
    // Try to load stored authentication on app start
    dispatch(loadStoredAuth());
  }, [dispatch]);

  // Show loading screen while checking authentication
  if (isLoading) {
    return null; // You might want to create a proper loading screen component
  }

  return (
    <NavigationContainer
      theme={{
        dark: isDarkMode,
        colors: {
          primary: theme.colors.primary,
          background: theme.colors.background,
          card: theme.colors.surface,
          text: theme.colors.text,
          border: theme.colors.border,
          notification: theme.colors.primary,
        },
      }}
    >
      <RootStack.Navigator
        screenOptions={{
          headerStyle: {
            backgroundColor: theme.colors.background,
            elevation: 0,
            shadowOpacity: 0,
          },
          headerTitleStyle: {
            color: theme.colors.text,
            fontSize: 18,
            fontWeight: '600',
          },
          headerTintColor: theme.colors.primary,
          cardStyle: {
            backgroundColor: theme.colors.background,
          },
        }}
      >
        {isAuthenticated ? (
          // Authenticated user screens
          <>
            <RootStack.Screen 
              name="Main" 
              component={MainTabNavigator}
              options={{ headerShown: false }}
            />
            <RootStack.Screen 
              name="CheckinFlow" 
              component={CheckinFlowScreen}
              options={{ 
                title: 'Daily Check-in',
                presentation: 'modal',
              }}
            />
            <RootStack.Screen 
              name="Settings" 
              component={SettingsScreen}
              options={{ title: 'Settings' }}
            />
            <RootStack.Screen 
              name="History" 
              component={HistoryScreen}
              options={{ title: 'Check-in History' }}
            />
          </>
        ) : (
          // Non-authenticated user screens
          <>
            <RootStack.Screen 
              name="Welcome" 
              component={WelcomeScreen}
              options={{ headerShown: false }}
            />
            <RootStack.Screen 
              name="Login" 
              component={LoginScreen}
              options={{ title: 'Sign In' }}
            />
            <RootStack.Screen 
              name="Register" 
              component={RegisterScreen}
              options={{ title: 'Create Account' }}
            />
          </>
        )}
      </RootStack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator; 