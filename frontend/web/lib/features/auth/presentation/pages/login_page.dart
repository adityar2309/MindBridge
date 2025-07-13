import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import 'package:form_builder_validators/form_builder_validators.dart';
import 'package:responsive_framework/responsive_framework.dart';
import '../bloc/auth_bloc.dart';
import '../../../../core/config/app_config.dart';
import '../../../../models/user_models.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormBuilderState>();
  bool _isPasswordVisible = false;
  bool _isRegistering = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: BlocListener<AuthBloc, AuthState>(
        listener: (context, state) {
          if (state is AuthAuthenticated) {
            Navigator.pushReplacementNamed(context, '/dashboard');
          } else if (state is AuthError) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Row(
                  children: [
                    const Icon(Icons.error, color: Colors.white),
                    const SizedBox(width: AppConfig.spacingMD),
                    Expanded(child: Text(state.message)),
                  ],
                ),
                backgroundColor: Theme.of(context).colorScheme.error,
                behavior: SnackBarBehavior.floating,
              ),
            );
          }
        },
        child: Center(
          child: SingleChildScrollView(
            padding: EdgeInsets.all(
              ResponsiveBreakpoints.of(context).isMobile 
                  ? AppConfig.spacingLG 
                  : AppConfig.spacingXXL,
            ),
            child: Container(
              constraints: const BoxConstraints(maxWidth: 450),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  _buildHeader(),
                  const SizedBox(height: AppConfig.spacingXXL),
                  _buildAuthForm(),
                  const SizedBox(height: AppConfig.spacingXL),
                  _buildToggleAuthMode(),
                  if (!ResponsiveBreakpoints.of(context).isMobile) ...[
                    const SizedBox(height: AppConfig.spacingXL),
                    _buildFeatures(),
                  ],
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Column(
      children: [
        Container(
          width: 80,
          height: 80,
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [
                Theme.of(context).colorScheme.primary,
                Theme.of(context).colorScheme.secondary,
              ],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(20),
            boxShadow: [
              BoxShadow(
                color: Theme.of(context).colorScheme.primary.withOpacity(0.3),
                blurRadius: 20,
                offset: const Offset(0, 10),
              ),
            ],
          ),
          child: const Icon(
            Icons.psychology,
            color: Colors.white,
            size: 40,
          ),
        ),
        const SizedBox(height: AppConfig.spacingLG),
        Text(
          AppConfig.appName,
          style: Theme.of(context).textTheme.displaySmall?.copyWith(
            fontWeight: FontWeight.bold,
            color: Theme.of(context).colorScheme.primary,
          ),
        ),
        const SizedBox(height: AppConfig.spacingSM),
        Text(
          'Your Mental Health Companion',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
          ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildAuthForm() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppConfig.spacingXL),
        child: FormBuilder(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                _isRegistering ? 'Create Account' : 'Welcome Back',
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppConfig.spacingSM),
              Text(
                _isRegistering 
                    ? 'Start your mental wellness journey today'
                    : 'Sign in to continue your journey',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppConfig.spacingXL),
              
              if (_isRegistering) ...[
                Row(
                  children: [
                    Expanded(
                      child: FormBuilderTextField(
                        name: 'firstName',
                        decoration: const InputDecoration(
                          labelText: 'First Name',
                          prefixIcon: Icon(Icons.person_outline),
                        ),
                        validator: FormBuilderValidators.compose([
                          FormBuilderValidators.required(),
                          FormBuilderValidators.minLength(2),
                        ]),
                      ),
                    ),
                    const SizedBox(width: AppConfig.spacingMD),
                    Expanded(
                      child: FormBuilderTextField(
                        name: 'lastName',
                        decoration: const InputDecoration(
                          labelText: 'Last Name',
                          prefixIcon: Icon(Icons.person_outline),
                        ),
                        validator: FormBuilderValidators.compose([
                          FormBuilderValidators.required(),
                          FormBuilderValidators.minLength(2),
                        ]),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: AppConfig.spacingLG),
              ],
              
              FormBuilderTextField(
                name: 'email',
                decoration: const InputDecoration(
                  labelText: 'Email Address',
                  prefixIcon: Icon(Icons.email_outlined),
                ),
                keyboardType: TextInputType.emailAddress,
                validator: FormBuilderValidators.compose([
                  FormBuilderValidators.required(),
                  FormBuilderValidators.email(),
                ]),
              ),
              const SizedBox(height: AppConfig.spacingLG),
              
              FormBuilderTextField(
                name: 'password',
                decoration: InputDecoration(
                  labelText: 'Password',
                  prefixIcon: const Icon(Icons.lock_outline),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _isPasswordVisible ? Icons.visibility_off : Icons.visibility,
                    ),
                    onPressed: () {
                      setState(() {
                        _isPasswordVisible = !_isPasswordVisible;
                      });
                    },
                  ),
                ),
                obscureText: !_isPasswordVisible,
                validator: FormBuilderValidators.compose([
                  FormBuilderValidators.required(),
                  FormBuilderValidators.minLength(6),
                ]),
              ),
              
              if (_isRegistering) ...[
                const SizedBox(height: AppConfig.spacingLG),
                FormBuilderDateTimePicker(
                  name: 'dateOfBirth',
                  inputType: InputType.date,
                  decoration: const InputDecoration(
                    labelText: 'Date of Birth (Optional)',
                    prefixIcon: Icon(Icons.calendar_today),
                  ),
                  lastDate: DateTime.now().subtract(const Duration(days: 365 * 13)), // Must be at least 13
                  firstDate: DateTime.now().subtract(const Duration(days: 365 * 120)), // Max 120 years
                ),
              ],
              
              const SizedBox(height: AppConfig.spacingXL),
              
              BlocBuilder<AuthBloc, AuthState>(
                builder: (context, state) {
                  final isLoading = state is AuthLoading;
                  
                  return ElevatedButton(
                    onPressed: isLoading ? null : _handleSubmit,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.all(AppConfig.spacingLG),
                    ),
                    child: isLoading
                        ? const Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(strokeWidth: 2),
                              ),
                              SizedBox(width: AppConfig.spacingMD),
                              Text('Please wait...'),
                            ],
                          )
                        : Text(
                            _isRegistering ? 'Create Account' : 'Sign In',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                  );
                },
              ),
              
              if (!_isRegistering) ...[
                const SizedBox(height: AppConfig.spacingLG),
                TextButton(
                  onPressed: () {
                    // TODO: Implement forgot password
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Password reset will be available soon'),
                        behavior: SnackBarBehavior.floating,
                      ),
                    );
                  },
                  child: const Text('Forgot Password?'),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildToggleAuthMode() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          _isRegistering 
              ? 'Already have an account? '
              : 'Don\'t have an account? ',
          style: Theme.of(context).textTheme.bodyMedium,
        ),
        TextButton(
          onPressed: () {
            setState(() {
              _isRegistering = !_isRegistering;
              _formKey.currentState?.reset();
            });
          },
          child: Text(
            _isRegistering ? 'Sign In' : 'Sign Up',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.primary,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildFeatures() {
    final features = [
      {'icon': Icons.trending_up, 'title': 'Track Progress', 'subtitle': 'Monitor your mood patterns'},
      {'icon': Icons.insights, 'title': 'AI Insights', 'subtitle': 'Get personalized recommendations'},
      {'icon': Icons.security, 'title': 'Private & Secure', 'subtitle': 'Your data stays safe'},
    ];

    return Column(
      children: [
        Text(
          'Why Choose MindBridge?',
          style: Theme.of(context).textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppConfig.spacingLG),
        ...features.map((feature) => Padding(
          padding: const EdgeInsets.only(bottom: AppConfig.spacingMD),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(AppConfig.spacingMD),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.primary.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(AppConfig.radiusMD),
                ),
                child: Icon(
                  feature['icon'] as IconData,
                  color: Theme.of(context).colorScheme.primary,
                  size: 24,
                ),
              ),
              const SizedBox(width: AppConfig.spacingMD),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      feature['title'] as String,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      feature['subtitle'] as String,
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        )),
      ],
    );
  }

  void _handleSubmit() {
    if (_formKey.currentState?.saveAndValidate() == true) {
      final formData = _formKey.currentState!.value;
      
      if (_isRegistering) {
        final userData = UserCreate(
          email: formData['email'],
          password: formData['password'],
          firstName: formData['firstName'],
          lastName: formData['lastName'],
          dateOfBirth: formData['dateOfBirth'],
        );
        
        context.read<AuthBloc>().add(AuthRegisterRequested(userData));
      } else {
        context.read<AuthBloc>().add(
          AuthLoginRequested(
            formData['email'],
            formData['password'],
          ),
        );
      }
    }
  }
} 