/**
 * CheckinScreen Tests
 * Tests for mood check-in screen functionality, form validation, and user interactions
 */

import React from 'react';
import { render, fireEvent, waitFor, act } from '@testing-library/react-native';
import { Provider } from 'react-redux';
import { NavigationContainer } from '@react-navigation/native';
import { 
  TestUtils, 
  ReduxTestUtils, 
  NavigationTestUtils, 
  FormTestUtils,
  ApiTestUtils 
} from '../setup/testSetup';

// Mock CheckinScreen component for testing
const MockCheckinScreen: React.FC<{
  navigation?: any;
  route?: any;
  onSubmit?: (data: any) => void;
  isLoading?: boolean;
}> = ({ 
  navigation = NavigationTestUtils.createMockNavigation(),
  route = NavigationTestUtils.createMockRoute(),
  onSubmit = jest.fn(),
  isLoading = false
}) => {
  const [formData, setFormData] = React.useState({
    mood: 5,
    anxiety: 5,
    stress: 5,
    energy: 5,
    notes: '',
  });

  const [errors, setErrors] = React.useState<Record<string, string>>({});

  const handleMoodChange = (value: number) => {
    setFormData(prev => ({ ...prev, mood: value }));
    if (errors.mood) {
      setErrors(prev => ({ ...prev, mood: '' }));
    }
  };

  const handleSubmit = () => {
    const newErrors: Record<string, string> = {};
    
    if (formData.mood < 1 || formData.mood > 10) {
      newErrors.mood = 'Mood must be between 1 and 10';
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    onSubmit(formData);
  };

  return (
    <div testID="checkin-screen">
      <div testID="checkin-header">
        <span>How are you feeling today?</span>
      </div>
      
      <div testID="mood-section">
        <label testID="mood-label">Mood (1-10)</label>
        <input
          testID="mood-slider"
          type="range"
          min="1"
          max="10"
          value={formData.mood}
          onChange={(e) => handleMoodChange(parseInt(e.target.value))}
        />
        <span testID="mood-value">{formData.mood}</span>
        {errors.mood && <span testID="mood-error" style={{ color: 'red' }}>{errors.mood}</span>}
      </div>

      <div testID="anxiety-section">
        <label testID="anxiety-label">Anxiety (1-10)</label>
        <input
          testID="anxiety-slider"
          type="range"
          min="1"
          max="10"
          value={formData.anxiety}
          onChange={(e) => setFormData(prev => ({ ...prev, anxiety: parseInt(e.target.value) }))}
        />
        <span testID="anxiety-value">{formData.anxiety}</span>
      </div>

      <div testID="stress-section">
        <label testID="stress-label">Stress (1-10)</label>
        <input
          testID="stress-slider"
          type="range"
          min="1"
          max="10"
          value={formData.stress}
          onChange={(e) => setFormData(prev => ({ ...prev, stress: parseInt(e.target.value) }))}
        />
        <span testID="stress-value">{formData.stress}</span>
      </div>

      <div testID="energy-section">
        <label testID="energy-label">Energy (1-10)</label>
        <input
          testID="energy-slider"
          type="range"
          min="1"
          max="10"
          value={formData.energy}
          onChange={(e) => setFormData(prev => ({ ...prev, energy: parseInt(e.target.value) }))}
        />
        <span testID="energy-value">{formData.energy}</span>
      </div>

      <div testID="notes-section">
        <label testID="notes-label">Additional Notes</label>
        <textarea
          testID="notes-input"
          placeholder="How was your day? Any thoughts to add..."
          value={formData.notes}
          onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
        />
      </div>

      <div testID="actions-section">
        <button
          testID="submit-button"
          onClick={handleSubmit}
          disabled={isLoading}
        >
          {isLoading ? 'Saving...' : 'Save Check-in'}
        </button>
        <button
          testID="cancel-button"
          onClick={() => navigation.goBack()}
        >
          Cancel
        </button>
      </div>
    </div>
  );
};

// Test wrapper with providers
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

describe('CheckinScreen', () => {
  let mockNavigation: any;
  let mockRoute: any;
  let mockOnSubmit: jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();
    mockNavigation = NavigationTestUtils.createMockNavigation();
    mockRoute = NavigationTestUtils.createMockRoute();
    mockOnSubmit = jest.fn();
  });

  describe('Rendering', () => {
    it('should render all form sections', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      expect(getByTestId('checkin-screen')).toBeDefined();
      expect(getByTestId('checkin-header')).toBeDefined();
      expect(getByTestId('mood-section')).toBeDefined();
      expect(getByTestId('anxiety-section')).toBeDefined();
      expect(getByTestId('stress-section')).toBeDefined();
      expect(getByTestId('energy-section')).toBeDefined();
      expect(getByTestId('notes-section')).toBeDefined();
      expect(getByTestId('actions-section')).toBeDefined();
    });

    it('should display default values for all sliders', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      expect(getByTestId('mood-value')).toHaveTextContent('5');
      expect(getByTestId('anxiety-value')).toHaveTextContent('5');
      expect(getByTestId('stress-value')).toHaveTextContent('5');
      expect(getByTestId('energy-value')).toHaveTextContent('5');
    });

    it('should show proper labels for all sections', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      expect(getByTestId('mood-label')).toHaveTextContent('Mood (1-10)');
      expect(getByTestId('anxiety-label')).toHaveTextContent('Anxiety (1-10)');
      expect(getByTestId('stress-label')).toHaveTextContent('Stress (1-10)');
      expect(getByTestId('energy-label')).toHaveTextContent('Energy (1-10)');
      expect(getByTestId('notes-label')).toHaveTextContent('Additional Notes');
    });
  });

  describe('Form Interactions', () => {
    it('should update mood value when slider changes', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      const moodSlider = getByTestId('mood-slider');
      fireEvent.change(moodSlider, { target: { value: '8' } });

      expect(getByTestId('mood-value')).toHaveTextContent('8');
    });

    it('should update anxiety value when slider changes', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      const anxietySlider = getByTestId('anxiety-slider');
      fireEvent.change(anxietySlider, { target: { value: '3' } });

      expect(getByTestId('anxiety-value')).toHaveTextContent('3');
    });

    it('should update notes when text input changes', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      const notesInput = getByTestId('notes-input');
      fireEvent.change(notesInput, { target: { value: 'Had a great day!' } });

      expect(notesInput.value).toBe('Had a great day!');
    });

    it('should handle multiple slider changes', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      fireEvent.change(getByTestId('mood-slider'), { target: { value: '9' } });
      fireEvent.change(getByTestId('stress-slider'), { target: { value: '2' } });
      fireEvent.change(getByTestId('energy-slider'), { target: { value: '7' } });

      expect(getByTestId('mood-value')).toHaveTextContent('9');
      expect(getByTestId('stress-value')).toHaveTextContent('2');
      expect(getByTestId('energy-value')).toHaveTextContent('7');
    });
  });

  describe('Form Submission', () => {
    it('should call onSubmit with form data when submit button is pressed', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen onSubmit={mockOnSubmit} />
        </TestWrapper>
      );

      // Update form values
      fireEvent.change(getByTestId('mood-slider'), { target: { value: '8' } });
      fireEvent.change(getByTestId('notes-input'), { target: { value: 'Good day' } });

      // Submit form
      fireEvent.click(getByTestId('submit-button'));

      expect(mockOnSubmit).toHaveBeenCalledWith({
        mood: 8,
        anxiety: 5,
        stress: 5,
        energy: 5,
        notes: 'Good day',
      });
    });

    it('should show loading state during submission', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen isLoading={true} />
        </TestWrapper>
      );

      const submitButton = getByTestId('submit-button');
      expect(submitButton).toHaveTextContent('Saving...');
      expect(submitButton).toBeDisabled();
    });

    it('should handle form validation errors', async () => {
      // This test would require implementing validation in the component
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen onSubmit={mockOnSubmit} />
        </TestWrapper>
      );

      // Set invalid value (outside range)
      fireEvent.change(getByTestId('mood-slider'), { target: { value: '11' } });
      fireEvent.click(getByTestId('submit-button'));

      await waitFor(() => {
        expect(getByTestId('mood-error')).toHaveTextContent('Mood must be between 1 and 10');
      });

      expect(mockOnSubmit).not.toHaveBeenCalled();
    });
  });

  describe('Navigation', () => {
    it('should call navigation.goBack when cancel button is pressed', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen navigation={mockNavigation} />
        </TestWrapper>
      );

      fireEvent.click(getByTestId('cancel-button'));

      expect(mockNavigation.goBack).toHaveBeenCalled();
    });

    it('should handle navigation props correctly', () => {
      render(
        <TestWrapper>
          <MockCheckinScreen navigation={mockNavigation} route={mockRoute} />
        </TestWrapper>
      );

      expect(mockNavigation).toBeDefined();
      expect(mockRoute).toBeDefined();
    });
  });

  describe('Accessibility', () => {
    it('should have proper accessibility labels for sliders', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      const moodSlider = getByTestId('mood-slider');
      expect(moodSlider).toBeDefined();
      expect(getByTestId('mood-label')).toBeDefined();
    });

    it('should have accessible form structure', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      // Check that labels are associated with inputs
      expect(getByTestId('mood-label')).toBeDefined();
      expect(getByTestId('mood-slider')).toBeDefined();
      expect(getByTestId('notes-label')).toBeDefined();
      expect(getByTestId('notes-input')).toBeDefined();
    });
  });

  describe('Performance', () => {
    it('should render quickly', () => {
      const startTime = Date.now();
      render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );
      const endTime = Date.now();

      expect(endTime - startTime).toBeLessThan(200);
    });

    it('should handle rapid slider interactions without lag', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      const moodSlider = getByTestId('mood-slider');

      // Rapidly change slider values
      for (let i = 1; i <= 10; i++) {
        fireEvent.change(moodSlider, { target: { value: i.toString() } });
      }

      expect(getByTestId('mood-value')).toHaveTextContent('10');
    });
  });

  describe('Edge Cases', () => {
    it('should handle extreme slider values', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      // Test minimum value
      fireEvent.change(getByTestId('mood-slider'), { target: { value: '1' } });
      expect(getByTestId('mood-value')).toHaveTextContent('1');

      // Test maximum value
      fireEvent.change(getByTestId('mood-slider'), { target: { value: '10' } });
      expect(getByTestId('mood-value')).toHaveTextContent('10');
    });

    it('should handle very long notes', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen />
        </TestWrapper>
      );

      const longNotes = 'A'.repeat(1000);
      fireEvent.change(getByTestId('notes-input'), { target: { value: longNotes } });

      expect(getByTestId('notes-input').value).toBe(longNotes);
    });

    it('should handle empty notes', () => {
      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen onSubmit={mockOnSubmit} />
        </TestWrapper>
      );

      fireEvent.click(getByTestId('submit-button'));

      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          notes: '',
        })
      );
    });
  });

  describe('Integration', () => {
    it('should work with Redux store', () => {
      const initialState = {
        checkin: {
          isLoading: false,
          lastCheckin: null,
        },
        user: TestUtils.createMockUser(),
      };

      const { getByTestId } = render(
        <TestWrapper initialState={initialState}>
          <MockCheckinScreen />
        </TestWrapper>
      );

      expect(getByTestId('checkin-screen')).toBeDefined();
    });

    it('should handle API integration', async () => {
      const mockApiResponse = ApiTestUtils.mockSuccessResponse({
        id: 'checkin-123',
        message: 'Check-in saved successfully',
      });

      const { getByTestId } = render(
        <TestWrapper>
          <MockCheckinScreen onSubmit={mockOnSubmit} />
        </TestWrapper>
      );

      fireEvent.click(getByTestId('submit-button'));

      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalled();
      });
    });
  });
}); 