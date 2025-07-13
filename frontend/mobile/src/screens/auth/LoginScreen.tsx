import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  TextInput,
  Alert,
} from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { RootStackParamList, LoginRequest } from '@/types';
import { useAppDispatch, useTheme, useFormValidation } from '@/utils/hooks';
import { loginUser } from '@/store/slices/authSlice';
import { lightTheme, darkTheme } from '@/constants/theme';
import { VALIDATION } from '@/constants';

type LoginScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Login'>;

interface Props {
  navigation: LoginScreenNavigationProp;
}

const LoginScreen: React.FC<Props> = ({ navigation }) => {
  const dispatch = useAppDispatch();
  const { isDarkMode } = useTheme();
  const theme = isDarkMode ? darkTheme : lightTheme;
  const styles = createStyles(theme);
  
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const initialValues: LoginRequest = {
    email: '',
    password: '',
  };

  const validationRules = {
    email: (value: string) => {
      if (!value) return 'Email is required';
      if (!VALIDATION.email.pattern.test(value)) return 'Please enter a valid email';
      return null;
    },
    password: (value: string) => {
      if (!value) return 'Password is required';
      if (value.length < VALIDATION.password.minLength) {
        return `Password must be at least ${VALIDATION.password.minLength} characters`;
      }
      return null;
    },
  };

  const {
    values,
    errors,
    touched,
    setValue,
    setFieldTouched,
    validateAll,
    isValid,
  } = useFormValidation(initialValues, validationRules);

  const handleLogin = async () => {
    if (!validateAll()) {
      return;
    }

    try {
      setIsLoading(true);
      await dispatch(loginUser(values)).unwrap();
      // Navigation will be handled automatically by AppNavigator when auth state changes
    } catch (error: any) {
      Alert.alert(
        'Login Failed',
        error.message || 'Please check your credentials and try again.',
        [{ text: 'OK' }]
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView 
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <Icon name="psychology" size={48} color={theme.colors.primary} />
          <Text style={styles.title}>Welcome Back</Text>
          <Text style={styles.subtitle}>Sign in to continue your mental health journey</Text>
        </View>

        {/* Form */}
        <View style={styles.form}>
          {/* Email Field */}
          <View style={styles.fieldContainer}>
            <Text style={styles.fieldLabel}>Email</Text>
            <View style={[
              styles.inputContainer,
              touched.email && errors.email && styles.inputError
            ]}>
              <Icon name="email" size={20} color={theme.colors.textSecondary} />
              <TextInput
                style={styles.input}
                placeholder="Enter your email"
                placeholderTextColor={theme.colors.textSecondary}
                value={values.email}
                onChangeText={(text) => setValue('email', text)}
                onBlur={() => setFieldTouched('email')}
                keyboardType="email-address"
                autoCapitalize="none"
                autoCorrect={false}
                editable={!isLoading}
              />
            </View>
            {touched.email && errors.email && (
              <Text style={styles.errorText}>{errors.email}</Text>
            )}
          </View>

          {/* Password Field */}
          <View style={styles.fieldContainer}>
            <Text style={styles.fieldLabel}>Password</Text>
            <View style={[
              styles.inputContainer,
              touched.password && errors.password && styles.inputError
            ]}>
              <Icon name="lock" size={20} color={theme.colors.textSecondary} />
              <TextInput
                style={styles.input}
                placeholder="Enter your password"
                placeholderTextColor={theme.colors.textSecondary}
                value={values.password}
                onChangeText={(text) => setValue('password', text)}
                onBlur={() => setFieldTouched('password')}
                secureTextEntry={!showPassword}
                autoCapitalize="none"
                autoCorrect={false}
                editable={!isLoading}
              />
              <TouchableOpacity
                onPress={() => setShowPassword(!showPassword)}
                disabled={isLoading}
              >
                <Icon 
                  name={showPassword ? 'visibility-off' : 'visibility'} 
                  size={20} 
                  color={theme.colors.textSecondary} 
                />
              </TouchableOpacity>
            </View>
            {touched.password && errors.password && (
              <Text style={styles.errorText}>{errors.password}</Text>
            )}
          </View>

          {/* Forgot Password Link */}
          <TouchableOpacity 
            style={styles.forgotPassword}
            onPress={() => {
              // TODO: Implement forgot password functionality
              Alert.alert('Coming Soon', 'Forgot password feature will be available soon.');
            }}
            disabled={isLoading}
          >
            <Text style={styles.forgotPasswordText}>Forgot Password?</Text>
          </TouchableOpacity>
        </View>

        {/* Sign In Button */}
        <TouchableOpacity
          style={[
            styles.signInButton,
            (!isValid || isLoading) && styles.signInButtonDisabled
          ]}
          onPress={handleLogin}
          disabled={!isValid || isLoading}
          activeOpacity={0.8}
        >
          {isLoading ? (
            <View style={styles.loadingContainer}>
              <Icon name="hourglass-empty" size={20} color="#FFFFFF" />
              <Text style={styles.signInButtonText}>Signing In...</Text>
            </View>
          ) : (
            <Text style={styles.signInButtonText}>Sign In</Text>
          )}
        </TouchableOpacity>

        {/* Sign Up Link */}
        <View style={styles.signUpContainer}>
          <Text style={styles.signUpText}>Don't have an account? </Text>
          <TouchableOpacity
            onPress={() => navigation.navigate('Register')}
            disabled={isLoading}
          >
            <Text style={styles.signUpLink}>Sign Up</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const createStyles = (theme: any) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  scrollContent: {
    flexGrow: 1,
    padding: 24,
  },
  header: {
    alignItems: 'center',
    marginTop: 40,
    marginBottom: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginTop: 16,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    lineHeight: 22,
  },
  form: {
    marginBottom: 32,
  },
  fieldContainer: {
    marginBottom: 20,
  },
  fieldLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: 8,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: theme.colors.surface,
    borderWidth: 1,
    borderColor: theme.colors.border,
    borderRadius: 12,
    paddingHorizontal: 16,
    height: 52,
    gap: 12,
  },
  inputError: {
    borderColor: theme.colors.error,
  },
  input: {
    flex: 1,
    fontSize: 16,
    color: theme.colors.text,
  },
  errorText: {
    fontSize: 14,
    color: theme.colors.error,
    marginTop: 4,
  },
  forgotPassword: {
    alignSelf: 'flex-end',
    marginTop: 8,
  },
  forgotPasswordText: {
    fontSize: 14,
    color: theme.colors.primary,
    fontWeight: '500',
  },
  signInButton: {
    backgroundColor: theme.colors.primary,
    height: 52,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 24,
  },
  signInButtonDisabled: {
    backgroundColor: theme.colors.textSecondary,
    opacity: 0.6,
  },
  signInButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  signUpContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  signUpText: {
    fontSize: 14,
    color: theme.colors.textSecondary,
  },
  signUpLink: {
    fontSize: 14,
    color: theme.colors.primary,
    fontWeight: '600',
  },
});

export default LoginScreen; 