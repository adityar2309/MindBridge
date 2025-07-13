module.exports = {
  preset: 'react-native',
  
  // Test Environment
  testEnvironment: 'node',
  
  // Setup Files
  setupFilesAfterEnv: [
    '@testing-library/jest-native/extend-expect',
    '<rootDir>/src/__tests__/setup/testSetup.ts'
  ],
  
  // Test File Patterns
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{js,jsx,ts,tsx}',
    '<rootDir>/src/**/*.{test,spec}.{js,jsx,ts,tsx}'
  ],
  
  // Coverage Configuration
  collectCoverage: false,
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/__tests__/**',
    '!src/**/__tests__/**',
    '!src/types/**',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/index.{js,jsx,ts,tsx}',
    '!src/**/index.{js,jsx,ts,tsx}'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html', 'json-summary'],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  },
  
  // Module Name Mapping
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@screens/(.*)$': '<rootDir>/src/screens/$1',
    '^@services/(.*)$': '<rootDir>/src/services/$1',
    '^@utils/(.*)$': '<rootDir>/src/utils/$1',
    '^@store/(.*)$': '<rootDir>/src/store/$1',
    '^@constants/(.*)$': '<rootDir>/src/constants/$1',
    '^@types/(.*)$': '<rootDir>/src/types/$1',
    '^@navigation/(.*)$': '<rootDir>/src/navigation/$1'
  },
  
  // Transform Settings
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest'
  },
  transformIgnorePatterns: [
    'node_modules/(?!(react-native|@react-native|react-native-.*|@react-navigation|@reduxjs/toolkit|react-redux)/)'
  ],
  
  // Mock Settings
  clearMocks: true,
  resetMocks: true,
  restoreMocks: true,
  
  // File Extensions
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  
  // Ignore Patterns
  testPathIgnorePatterns: [
    '<rootDir>/node_modules/',
    '<rootDir>/android/',
    '<rootDir>/ios/',
    '<rootDir>/coverage/'
  ],
  
  // Mock Files
  setupFiles: [
    '<rootDir>/src/__tests__/setup/jestSetup.ts'
  ],
  
  // Verbose Output
  verbose: true,
  
  // Test Categories
  projects: [
    {
      displayName: 'Unit Tests',
      testMatch: ['<rootDir>/src/**/__tests__/unit/**/*.{test,spec}.{js,jsx,ts,tsx}']
    },
    {
      displayName: 'Integration Tests', 
      testMatch: ['<rootDir>/src/**/__tests__/integration/**/*.{test,spec}.{js,jsx,ts,tsx}']
    },
    {
      displayName: 'Component Tests',
      testMatch: ['<rootDir>/src/**/__tests__/components/**/*.{test,spec}.{js,jsx,ts,tsx}']
    },
    {
      displayName: 'Screen Tests',
      testMatch: ['<rootDir>/src/**/__tests__/screens/**/*.{test,spec}.{js,jsx,ts,tsx}']
    }
  ],
  
  // Performance
  maxWorkers: '50%',
  
  // Error Handling
  errorOnDeprecated: true,
  
  // Debugging
  detectOpenHandles: false,
  detectLeaks: false
}; 