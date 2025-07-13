/**
 * Jest Setup for React Native Testing
 * Configures mocks and global test environment
 */

import 'react-native-gesture-handler/jestSetup';
import mockAsyncStorage from '@react-native-async-storage/async-storage/jest/async-storage-mock';

// Mock React Native modules
jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');

// Mock AsyncStorage
jest.mock('@react-native-async-storage/async-storage', () => mockAsyncStorage);

// Mock React Navigation
jest.mock('@react-navigation/native', () => ({
  ...jest.requireActual('@react-navigation/native'),
  useNavigation: () => ({
    navigate: jest.fn(),
    goBack: jest.fn(),
    dispatch: jest.fn(),
    setOptions: jest.fn(),
    isFocused: jest.fn(() => true),
    addListener: jest.fn(() => jest.fn()),
  }),
  useRoute: () => ({
    params: {},
    key: 'test-route',
    name: 'test-route',
  }),
  useFocusEffect: jest.fn(),
  useIsFocused: () => true,
}));

// Mock React Native Vector Icons
jest.mock('react-native-vector-icons/MaterialIcons', () => 'Icon');
jest.mock('react-native-vector-icons/Ionicons', () => 'Icon');
jest.mock('react-native-vector-icons/FontAwesome', () => 'Icon');

// Mock React Native Gesture Handler
jest.mock('react-native-gesture-handler', () => ({
  ...jest.requireActual('react-native-gesture-handler'),
  PanGestureHandler: 'PanGestureHandler',
  TapGestureHandler: 'TapGestureHandler',
  FlingGestureHandler: 'FlingGestureHandler',
  ForceTouchGestureHandler: 'ForceTouchGestureHandler',
  LongPressGestureHandler: 'LongPressGestureHandler',
  PinchGestureHandler: 'PinchGestureHandler',
  RotationGestureHandler: 'RotationGestureHandler',
  State: {
    BEGAN: 'BEGAN',
    FAILED: 'FAILED',
    CANCELLED: 'CANCELLED',
    ACTIVE: 'ACTIVE',
    END: 'END',
    UNDETERMINED: 'UNDETERMINED',
  },
}));

// Mock React Native Safe Area Context
jest.mock('react-native-safe-area-context', () => ({
  SafeAreaProvider: ({ children }: { children: React.ReactNode }) => children,
  SafeAreaView: ({ children }: { children: React.ReactNode }) => children,
  useSafeAreaInsets: () => ({ top: 0, bottom: 0, left: 0, right: 0 }),
  useSafeAreaFrame: () => ({ x: 0, y: 0, width: 390, height: 844 }),
}));

// Mock React Native Paper
jest.mock('react-native-paper', () => ({
  ...jest.requireActual('react-native-paper'),
  Provider: ({ children }: { children: React.ReactNode }) => children,
  DefaultTheme: {
    colors: {
      primary: '#6200ee',
      accent: '#03dac4',
      background: '#f6f6f6',
      surface: '#ffffff',
      error: '#b00020',
      text: '#000000',
      onSurface: '#000000',
      disabled: 'rgba(0, 0, 0, 0.26)',
      placeholder: 'rgba(0, 0, 0, 0.54)',
      backdrop: 'rgba(0, 0, 0, 0.5)',
      notification: '#f50057',
    },
  },
}));

// Mock React Native Charts
jest.mock('react-native-chart-kit', () => ({
  LineChart: 'LineChart',
  BarChart: 'BarChart',
  PieChart: 'PieChart',
  ProgressChart: 'ProgressChart',
  ContributionGraph: 'ContributionGraph',
}));

// Mock React Native SVG
jest.mock('react-native-svg', () => ({
  Svg: 'Svg',
  Circle: 'Circle',
  Ellipse: 'Ellipse',
  G: 'G',
  Text: 'Text',
  TSpan: 'TSpan',
  TextPath: 'TextPath',
  Path: 'Path',
  Polygon: 'Polygon',
  Polyline: 'Polyline',
  Line: 'Line',
  Rect: 'Rect',
  Use: 'Use',
  Image: 'Image',
  Symbol: 'Symbol',
  Defs: 'Defs',
  LinearGradient: 'LinearGradient',
  RadialGradient: 'RadialGradient',
  Stop: 'Stop',
  ClipPath: 'ClipPath',
  Pattern: 'Pattern',
  Mask: 'Mask',
}));

// Mock React Native Keychain
jest.mock('react-native-keychain', () => ({
  setInternetCredentials: jest.fn(() => Promise.resolve()),
  getInternetCredentials: jest.fn(() => Promise.resolve({ username: 'test', password: 'test' })),
  resetInternetCredentials: jest.fn(() => Promise.resolve()),
  canImplyAuthentication: jest.fn(() => Promise.resolve(true)),
  getSupportedBiometryType: jest.fn(() => Promise.resolve('FaceID')),
}));

// Mock React Native Device Info
jest.mock('react-native-device-info', () => ({
  getVersion: () => '1.0.0',
  getBuildNumber: () => '1',
  getApplicationName: () => 'MindBridge',
  getBundleId: () => 'com.mindbridge.app',
  getDeviceId: () => 'test-device-id',
  getSystemVersion: () => '15.0',
  isEmulator: () => Promise.resolve(true),
  hasNotch: () => false,
}));

// Mock React Native NetInfo
jest.mock('@react-native-community/netinfo', () => ({
  fetch: () => Promise.resolve({
    type: 'wifi',
    isConnected: true,
    isInternetReachable: true,
  }),
  addEventListener: jest.fn(() => jest.fn()),
  useNetInfo: () => ({
    type: 'wifi',
    isConnected: true,
    isInternetReachable: true,
  }),
}));

// Mock React Native Push Notification
jest.mock('react-native-push-notification', () => ({
  configure: jest.fn(),
  localNotification: jest.fn(),
  scheduleLocalNotification: jest.fn(),
  cancelLocalNotifications: jest.fn(),
  cancelAllLocalNotifications: jest.fn(),
  getApplicationIconBadgeNumber: jest.fn(),
  setApplicationIconBadgeNumber: jest.fn(),
  getChannels: jest.fn(),
  channelExists: jest.fn(),
  createChannel: jest.fn(),
  channelBlocked: jest.fn(),
  deleteChannel: jest.fn(),
}));

// Mock React Native Haptic Feedback
jest.mock('react-native-haptic-feedback', () => ({
  trigger: jest.fn(),
}));

// Mock Axios
jest.mock('axios', () => ({
  create: jest.fn(() => ({
    get: jest.fn(() => Promise.resolve({ data: {} })),
    post: jest.fn(() => Promise.resolve({ data: {} })),
    put: jest.fn(() => Promise.resolve({ data: {} })),
    delete: jest.fn(() => Promise.resolve({ data: {} })),
    interceptors: {
      request: { use: jest.fn(), eject: jest.fn() },
      response: { use: jest.fn(), eject: jest.fn() },
    },
  })),
  get: jest.fn(() => Promise.resolve({ data: {} })),
  post: jest.fn(() => Promise.resolve({ data: {} })),
  put: jest.fn(() => Promise.resolve({ data: {} })),
  delete: jest.fn(() => Promise.resolve({ data: {} })),
}));

// Global test console settings
globalThis.console = {
  ...console,
  // Suppress console.warn in tests unless explicitly needed
  warn: jest.fn(),
  error: jest.fn(),
};

// Mock timers
jest.useFakeTimers({
  legacyFakeTimers: true,
});

// Mock Dimensions
const mockDimensions = {
  window: {
    width: 390,
    height: 844,
    scale: 3,
    fontScale: 1,
  },
  screen: {
    width: 390,
    height: 844,
    scale: 3,
    fontScale: 1,
  },
};

jest.mock('react-native/Libraries/Utilities/Dimensions', () => ({
  get: jest.fn((dim: keyof typeof mockDimensions) => mockDimensions[dim]),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
})); 