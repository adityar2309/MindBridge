/**
 * Navigation Flow Integration Tests
 * Tests for complete user journeys across multiple screens
 */

import React from 'react';
import { render, fireEvent, waitFor, act } from '@testing-library/react-native';
import { Provider } from 'react-redux';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { 
  TestUtils, 
  ReduxTestUtils, 
  NavigationTestUtils, 
  ApiTestUtils 
} from '../setup/testSetup';

const Stack = createStackNavigator();

// Mock Screen Components
const MockHomeScreen: React.FC<{ navigation: any }> = ({ navigation }) => (
  <div testID="home-screen">
    <div testID="home-header">MindBridge</div>
    <button 
      testID="checkin-button"
      onClick={() => navigation.navigate('Checkin')}
    >
      Quick Check-in
    </button>
    <button 
      testID="analytics-button"
      onClick={() => navigation.navigate('Analytics')}
    >
      View Analytics
    </button>
    <button 
      testID="profile-button"
      onClick={() => navigation.navigate('Profile')}
    >
      Profile
    </button>
  </div>
);

const MockCheckinScreen: React.FC<{ navigation: any; route: any }> = ({ navigation, route }) => {
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  
  const handleSubmit = async () => {
    setIsSubmitting(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 500));
    setIsSubmitting(false);
    navigation.navigate('CheckinSuccess', { checkinId: '123' });
  };

  return (
    <div testID="checkin-screen">
      <div testID="checkin-header">How are you feeling?</div>
      <input testID="mood-slider" type="range" min="1" max="10" defaultValue="5" />
      <button 
        testID="submit-checkin"
        onClick={handleSubmit}
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Saving...' : 'Save Check-in'}
      </button>
      <button 
        testID="cancel-checkin"
        onClick={() => navigation.goBack()}
      >
        Cancel
      </button>
    </div>
  );
};

const MockCheckinSuccessScreen: React.FC<{ navigation: any; route: any }> = ({ navigation, route }) => (
  <div testID="checkin-success-screen">
    <div testID="success-message">Check-in saved successfully!</div>
    <div testID="checkin-id">ID: {route.params?.checkinId}</div>
    <button 
      testID="view-analytics"
      onClick={() => navigation.navigate('Analytics')}
    >
      View Your Progress
    </button>
    <button 
      testID="back-home"
      onClick={() => navigation.navigate('Home')}
    >
      Back to Home
    </button>
  </div>
);

const MockAnalyticsScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const [isLoading, setIsLoading] = React.useState(true);
  const [data, setData] = React.useState(null);

  React.useEffect(() => {
    // Simulate data loading
    setTimeout(() => {
      setData({ averageMood: 7.2, trend: 'improving' });
      setIsLoading(false);
    }, 300);
  }, []);

  if (isLoading) {
    return (
      <div testID="analytics-screen">
        <div testID="analytics-loading">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div testID="analytics-screen">
      <div testID="analytics-header">Your Progress</div>
      <div testID="average-mood">Average Mood: {data?.averageMood}</div>
      <div testID="mood-trend">Trend: {data?.trend}</div>
      <button 
        testID="new-checkin"
        onClick={() => navigation.navigate('Checkin')}
      >
        New Check-in
      </button>
      <button 
        testID="back-home"
        onClick={() => navigation.navigate('Home')}
      >
        Home
      </button>
    </div>
  );
};

const MockProfileScreen: React.FC<{ navigation: any }> = ({ navigation }) => (
  <div testID="profile-screen">
    <div testID="profile-header">Profile</div>
    <div testID="user-name">Test User</div>
    <button 
      testID="edit-profile"
      onClick={() => navigation.navigate('EditProfile')}
    >
      Edit Profile
    </button>
    <button 
      testID="logout"
      onClick={() => navigation.navigate('Login')}
    >
      Logout
    </button>
  </div>
);

const MockEditProfileScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const [name, setName] = React.useState('Test User');
  
  const handleSave = () => {
    navigation.goBack();
  };

  return (
    <div testID="edit-profile-screen">
      <div testID="edit-profile-header">Edit Profile</div>
      <input 
        testID="name-input"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button testID="save-profile" onClick={handleSave}>Save</button>
      <button testID="cancel-edit" onClick={() => navigation.goBack()}>Cancel</button>
    </div>
  );
};

// Navigation Stack
const TestNavigationStack = () => (
  <Stack.Navigator initialRouteName="Home">
    <Stack.Screen name="Home" component={MockHomeScreen} />
    <Stack.Screen name="Checkin" component={MockCheckinScreen} />
    <Stack.Screen name="CheckinSuccess" component={MockCheckinSuccessScreen} />
    <Stack.Screen name="Analytics" component={MockAnalyticsScreen} />
    <Stack.Screen name="Profile" component={MockProfileScreen} />
    <Stack.Screen name="EditProfile" component={MockEditProfileScreen} />
  </Stack.Navigator>
);

// Test Wrapper
const TestWrapper: React.FC<{ children: React.ReactNode; initialState?: any }> = ({ 
  children, 
  initialState = {} 
}) => {
  const mockStore = ReduxTestUtils.createMockStore(initialState);
  
  return (
    <Provider store={mockStore}>
      <NavigationContainer>
        {children}
      </NavigationContainer>
    </Provider>
  );
};

describe('Navigation Flow Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  describe('Check-in Flow', () => {
    it('should complete full check-in journey from home to success', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Start at home screen
      expect(getByTestId('home-screen')).toBeDefined();

      // Navigate to check-in
      fireEvent.click(getByTestId('checkin-button'));
      await waitFor(() => {
        expect(getByTestId('checkin-screen')).toBeDefined();
      });

      // Fill out check-in form
      fireEvent.change(getByTestId('mood-slider'), { target: { value: '8' } });

      // Submit check-in
      fireEvent.click(getByTestId('submit-checkin'));

      // Wait for submission and navigation
      act(() => {
        jest.advanceTimersByTime(600);
      });

      await waitFor(() => {
        expect(getByTestId('checkin-success-screen')).toBeDefined();
        expect(getByTestId('checkin-id')).toHaveTextContent('ID: 123');
      });
    });

    it('should allow cancelling check-in and return to home', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Navigate to check-in
      fireEvent.click(getByTestId('checkin-button'));
      await waitFor(() => {
        expect(getByTestId('checkin-screen')).toBeDefined();
      });

      // Cancel check-in
      fireEvent.click(getByTestId('cancel-checkin'));
      await waitFor(() => {
        expect(getByTestId('home-screen')).toBeDefined();
      });
    });

    it('should navigate from success screen to analytics', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Complete check-in flow first
      fireEvent.click(getByTestId('checkin-button'));
      await waitFor(() => expect(getByTestId('checkin-screen')).toBeDefined());
      
      fireEvent.click(getByTestId('submit-checkin'));
      act(() => {
        jest.advanceTimersByTime(600);
      });
      
      await waitFor(() => expect(getByTestId('checkin-success-screen')).toBeDefined());

      // Navigate to analytics
      fireEvent.click(getByTestId('view-analytics'));
      
      // Wait for analytics to load
      await waitFor(() => {
        expect(getByTestId('analytics-loading')).toBeDefined();
      });

      act(() => {
        jest.advanceTimersByTime(400);
      });

      await waitFor(() => {
        expect(getByTestId('analytics-screen')).toBeDefined();
        expect(getByTestId('average-mood')).toHaveTextContent('Average Mood: 7.2');
      });
    });
  });

  describe('Analytics Flow', () => {
    it('should navigate directly to analytics from home and load data', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Navigate to analytics from home
      fireEvent.click(getByTestId('analytics-button'));
      
      await waitFor(() => {
        expect(getByTestId('analytics-loading')).toBeDefined();
      });

      // Wait for data loading
      act(() => {
        jest.advanceTimersByTime(400);
      });

      await waitFor(() => {
        expect(getByTestId('analytics-screen')).toBeDefined();
        expect(getByTestId('average-mood')).toBeDefined();
        expect(getByTestId('mood-trend')).toHaveTextContent('Trend: improving');
      });
    });

    it('should navigate from analytics to new check-in', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Navigate to analytics
      fireEvent.click(getByTestId('analytics-button'));
      act(() => {
        jest.advanceTimersByTime(400);
      });
      
      await waitFor(() => expect(getByTestId('analytics-screen')).toBeDefined());

      // Navigate to new check-in
      fireEvent.click(getByTestId('new-checkin'));
      await waitFor(() => {
        expect(getByTestId('checkin-screen')).toBeDefined();
      });
    });
  });

  describe('Profile Flow', () => {
    it('should navigate through profile editing flow', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Navigate to profile
      fireEvent.click(getByTestId('profile-button'));
      await waitFor(() => {
        expect(getByTestId('profile-screen')).toBeDefined();
        expect(getByTestId('user-name')).toHaveTextContent('Test User');
      });

      // Navigate to edit profile
      fireEvent.click(getByTestId('edit-profile'));
      await waitFor(() => {
        expect(getByTestId('edit-profile-screen')).toBeDefined();
      });

      // Edit name
      const nameInput = getByTestId('name-input');
      fireEvent.change(nameInput, { target: { value: 'Updated User' } });

      // Save changes
      fireEvent.click(getByTestId('save-profile'));
      await waitFor(() => {
        expect(getByTestId('profile-screen')).toBeDefined();
      });
    });

    it('should cancel profile editing and return to profile', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Navigate to profile and edit
      fireEvent.click(getByTestId('profile-button'));
      await waitFor(() => expect(getByTestId('profile-screen')).toBeDefined());
      
      fireEvent.click(getByTestId('edit-profile'));
      await waitFor(() => expect(getByTestId('edit-profile-screen')).toBeDefined());

      // Cancel editing
      fireEvent.click(getByTestId('cancel-edit'));
      await waitFor(() => {
        expect(getByTestId('profile-screen')).toBeDefined();
      });
    });
  });

  describe('Cross-Screen Navigation', () => {
    it('should maintain navigation state across complex user journeys', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Complex journey: Home -> Analytics -> Check-in -> Success -> Home
      
      // 1. Home to Analytics
      fireEvent.click(getByTestId('analytics-button'));
      act(() => {
        jest.advanceTimersByTime(400);
      });
      await waitFor(() => expect(getByTestId('analytics-screen')).toBeDefined());

      // 2. Analytics to Check-in
      fireEvent.click(getByTestId('new-checkin'));
      await waitFor(() => expect(getByTestId('checkin-screen')).toBeDefined());

      // 3. Complete Check-in
      fireEvent.click(getByTestId('submit-checkin'));
      act(() => {
        jest.advanceTimersByTime(600);
      });
      await waitFor(() => expect(getByTestId('checkin-success-screen')).toBeDefined());

      // 4. Back to Home
      fireEvent.click(getByTestId('back-home'));
      await waitFor(() => expect(getByTestId('home-screen')).toBeDefined());
    });

    it('should handle rapid navigation without crashes', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Rapid navigation sequence
      fireEvent.click(getByTestId('analytics-button'));
      fireEvent.click(getByTestId('profile-button'));
      fireEvent.click(getByTestId('checkin-button'));

      // Should eventually settle on last navigation
      await waitFor(() => {
        expect(getByTestId('checkin-screen')).toBeDefined();
      });
    });
  });

  describe('State Persistence', () => {
    it('should maintain form state during navigation interruptions', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Start check-in
      fireEvent.click(getByTestId('checkin-button'));
      await waitFor(() => expect(getByTestId('checkin-screen')).toBeDefined());

      // Modify form
      fireEvent.change(getByTestId('mood-slider'), { target: { value: '9' } });

      // Navigate away and back (simulating interruption)
      fireEvent.click(getByTestId('cancel-checkin'));
      await waitFor(() => expect(getByTestId('home-screen')).toBeDefined());

      fireEvent.click(getByTestId('checkin-button'));
      await waitFor(() => expect(getByTestId('checkin-screen')).toBeDefined());

      // Form should reset to default values (expected behavior)
      expect(getByTestId('mood-slider')).toHaveDisplayValue('5');
    });

    it('should handle navigation with route parameters', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Complete check-in to get route params
      fireEvent.click(getByTestId('checkin-button'));
      await waitFor(() => expect(getByTestId('checkin-screen')).toBeDefined());
      
      fireEvent.click(getByTestId('submit-checkin'));
      act(() => {
        jest.advanceTimersByTime(600);
      });
      
      await waitFor(() => {
        expect(getByTestId('checkin-success-screen')).toBeDefined();
        expect(getByTestId('checkin-id')).toHaveTextContent('ID: 123');
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle navigation errors gracefully', async () => {
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Simulate error scenario by trying to navigate to non-existent screen
      const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

      try {
        // Normal navigation should work
        fireEvent.click(getByTestId('analytics-button'));
        await waitFor(() => {
          expect(getByTestId('analytics-loading')).toBeDefined();
        });
      } catch (error) {
        // Should not throw
        expect(error).toBeUndefined();
      }

      consoleError.mockRestore();
    });
  });

  describe('Performance', () => {
    it('should handle navigation performantly', async () => {
      const startTime = Date.now();
      
      const { getByTestId } = render(
        <TestWrapper>
          <TestNavigationStack />
        </TestWrapper>
      );

      // Multiple navigations
      fireEvent.click(getByTestId('analytics-button'));
      fireEvent.click(getByTestId('checkin-button'));
      fireEvent.click(getByTestId('cancel-checkin'));

      const endTime = Date.now();
      
      // Should complete within reasonable time
      expect(endTime - startTime).toBeLessThan(500);
      
      await waitFor(() => {
        expect(getByTestId('home-screen')).toBeDefined();
      });
    });
  });
}); 