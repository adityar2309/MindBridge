/**
 * Test Setup and Utilities for React Native Testing
 * Provides custom matchers, test helpers, and utilities
 */

import '@testing-library/jest-native/extend-expect';

// Extend Jest matchers for better assertions
declare global {
  namespace jest {
    interface Matchers<R> {
      toBeVisible(): R;
      toHaveProp(prop: string, value?: any): R;
      toHaveTextContent(text: string | RegExp): R;
      toBeDisabled(): R;
      toBeEnabled(): R;
      toHaveDisplayValue(value: string | RegExp): R;
      toBeChecked(): R;
      toBePartiallyChecked(): R;
      toHaveAccessibilityState(state: any): R;
      toHaveAccessibilityValue(value: any): R;
    }
  }
}

// Global test utilities
export const TestUtils = {
  /**
   * Wait for async operations to complete
   */
  waitForAsync: async (timeout = 1000) => {
    return new Promise<void>(resolve => setTimeout(resolve, timeout));
  },

  /**
   * Mock console methods during tests
   */
  suppressConsole: () => {
    const originalConsole = global.console;
    global.console = {
      ...console,
      log: jest.fn(),
      warn: jest.fn(),
      error: jest.fn(),
      info: jest.fn(),
      debug: jest.fn(),
    };
    return originalConsole;
  },

  /**
   * Restore console methods after tests
   */
  restoreConsole: (originalConsole: any) => {
    global.console = originalConsole;
  },

  /**
   * Mock Date for consistent testing
   */
  mockDate: (date: string | Date) => {
    const mockDate = new Date(date);
    jest.spyOn(global, 'Date').mockImplementation(() => mockDate as any);
    return mockDate;
  },

  /**
   * Restore Date mock
   */
  restoreDate: () => {
    jest.restoreAllMocks();
  },

  /**
   * Generate mock user data for testing
   */
  createMockUser: (overrides = {}) => ({
    id: 'test-user-123',
    email: 'test@mindbridge.com',
    name: 'Test User',
    avatar: 'https://example.com/avatar.jpg',
    preferences: {
      theme: 'light',
      notifications: true,
      reminderTime: '09:00',
    },
    profile: {
      age: 28,
      timezone: 'UTC',
      onboardingCompleted: true,
    },
    ...overrides,
  }),

  /**
   * Generate mock checkin data for testing
   */
  createMockCheckin: (overrides = {}) => ({
    id: 'checkin-123',
    userId: 'test-user-123',
    timestamp: new Date().toISOString(),
    mood: 7,
    anxiety: 3,
    stress: 4,
    energy: 6,
    sleep: {
      hours: 8,
      quality: 7,
    },
    notes: 'Feeling good today',
    tags: ['work', 'exercise'],
    activities: ['meditation', 'exercise'],
    ...overrides,
  }),

  /**
   * Generate mock analytics data for testing
   */
  createMockAnalytics: (overrides = {}) => ({
    period: '7d',
    averageMood: 7.2,
    moodTrend: 'improving',
    topTriggers: ['work stress', 'sleep'],
    insights: [
      'Your mood improves after exercise',
      'Consider reducing caffeine intake',
    ],
    chartData: [
      { date: '2025-01-07', mood: 6 },
      { date: '2025-01-08', mood: 7 },
      { date: '2025-01-09', mood: 8 },
      { date: '2025-01-10', mood: 7 },
      { date: '2025-01-11', mood: 8 },
      { date: '2025-01-12', mood: 9 },
      { date: '2025-01-13', mood: 8 },
    ],
    ...overrides,
  }),
};

// Redux Store Test Utilities
const ReduxTestUtils = {
  /**
   * Create mock Redux store for testing
   */
  createMockStore: (initialState = {}) => {
    const store = {
      getState: jest.fn(() => initialState),
      dispatch: jest.fn(),
      subscribe: jest.fn(),
      replaceReducer: jest.fn(),
    };
    return store;
  },

  /**
   * Create mock Redux action for testing
   */
  createMockAction: (type: string, payload?: any) => ({
    type,
    payload,
  }),

  /**
   * Mock Redux dispatch function
   */
  mockDispatch: jest.fn(),
};

// API Test Utilities
const ApiTestUtils = {
  /**
   * Mock successful API response
   */
  mockSuccessResponse: (data: any) => ({
    status: 200,
    data,
    headers: {},
    config: {},
    statusText: 'OK',
  }),

  /**
   * Mock API error response
   */
  mockErrorResponse: (status = 500, message = 'Internal Server Error') => ({
    response: {
      status,
      data: { message },
      headers: {},
      config: {},
      statusText: message,
    },
  }),

  /**
   * Mock network error
   */
  mockNetworkError: () => ({
    message: 'Network Error',
    code: 'NETWORK_ERROR',
  }),
};

// Navigation Test Utilities
const NavigationTestUtils = {
  /**
   * Create mock navigation prop
   */
  createMockNavigation: (overrides = {}) => ({
    navigate: jest.fn(),
    goBack: jest.fn(),
    dispatch: jest.fn(),
    setOptions: jest.fn(),
    isFocused: jest.fn(() => true),
    addListener: jest.fn(() => jest.fn()),
    removeListener: jest.fn(),
    canGoBack: jest.fn(() => true),
    getId: jest.fn(() => 'test-navigation-id'),
    getParent: jest.fn(),
    getState: jest.fn(() => ({
      key: 'test-state',
      index: 0,
      routeNames: ['Home'],
      routes: [{ key: 'test-route', name: 'Home', params: {} }],
    })),
    ...overrides,
  }),

  /**
   * Create mock route prop
   */
  createMockRoute: (overrides = {}) => ({
    key: 'test-route',
    name: 'TestScreen',
    params: {},
    ...overrides,
  }),
};

// Form Test Utilities
const FormTestUtils = {
  /**
   * Fill form field with value
   */
  fillField: async (getByTestId: any, testId: string, value: string) => {
    const field = getByTestId(testId);
    field.props.onChangeText(value);
    return field;
  },

  /**
   * Submit form
   */
  submitForm: async (getByTestId: any, testId = 'submit-button') => {
    const submitButton = getByTestId(testId);
    submitButton.props.onPress();
    return submitButton;
  },

  /**
   * Validate form error
   */
  expectFormError: (getByText: any, errorMessage: string) => {
    expect(getByText(errorMessage)).toBeDefined();
  },
};

// Animation Test Utilities
const AnimationTestUtils = {
  /**
   * Fast forward animations
   */
  runAllTimers: () => {
    jest.runAllTimers();
  },

  /**
   * Advance timers by time
   */
  advanceTimersByTime: (time: number) => {
    jest.advanceTimersByTime(time);
  },

  /**
   * Mock animation completion
   */
  mockAnimationEnd: () => {
    jest.runOnlyPendingTimers();
  },
};

// Setup global test environment
beforeEach(() => {
  // Clear all mocks before each test
  jest.clearAllMocks();
  
  // Reset timers
  jest.clearAllTimers();
  
  // Reset console
  TestUtils.restoreDate();
});

afterEach(() => {
  // Clean up after each test
  jest.clearAllMocks();
  jest.clearAllTimers();
});

// Export test utilities for use in test files
export {
  TestUtils as default,
  ReduxTestUtils,
  ApiTestUtils,
  NavigationTestUtils,
  FormTestUtils,
  AnimationTestUtils,
}; 