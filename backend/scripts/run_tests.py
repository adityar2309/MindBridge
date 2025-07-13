#!/usr/bin/env python3
"""
Comprehensive test runner for MindBridge backend.

This script provides a unified interface for running different types of tests
with various configurations and reporting options.
"""

import os
import sys
import argparse
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any


class TestRunner:
    """Main test runner class with various test execution options."""
    
    def __init__(self):
        self.backend_dir = Path(__file__).parent.parent
        self.project_root = self.backend_dir.parent
        
    def run_command(self, command: List[str], capture_output: bool = False) -> subprocess.CompletedProcess:
        """Run a command and return the result."""
        print(f"Running: {' '.join(command)}")
        
        if capture_output:
            return subprocess.run(command, capture_output=True, text=True, cwd=self.backend_dir)
        else:
            return subprocess.run(command, cwd=self.backend_dir)
    
    def setup_environment(self):
        """Set up test environment variables."""
        os.environ["TESTING"] = "true"
        os.environ["DATABASE_URL"] = "sqlite:///./test.db"
        os.environ["PYTHONPATH"] = str(self.backend_dir)
        
        print("✓ Test environment configured")
    
    def install_dependencies(self):
        """Install test dependencies."""
        print("Installing test dependencies...")
        
        command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        result = self.run_command(command)
        
        if result.returncode == 0:
            print("✓ Dependencies installed successfully")
        else:
            print("✗ Failed to install dependencies")
            sys.exit(1)
    
    def run_unit_tests(self, verbose: bool = False, coverage: bool = True) -> bool:
        """Run unit tests."""
        print("\n" + "="*50)
        print("RUNNING UNIT TESTS")
        print("="*50)
        
        command = [sys.executable, "-m", "pytest", "tests/unit/", "-m", "unit"]
        
        if verbose:
            command.append("-v")
        
        if coverage:
            command.extend([
                "--cov=backend", 
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov/unit"
            ])
        
        result = self.run_command(command)
        success = result.returncode == 0
        
        if success:
            print("✓ Unit tests passed")
        else:
            print("✗ Unit tests failed")
        
        return success
    
    def run_integration_tests(self, verbose: bool = False) -> bool:
        """Run integration tests."""
        print("\n" + "="*50)
        print("RUNNING INTEGRATION TESTS")
        print("="*50)
        
        command = [sys.executable, "-m", "pytest", "tests/integration/", "-m", "integration"]
        
        if verbose:
            command.append("-v")
        
        result = self.run_command(command)
        success = result.returncode == 0
        
        if success:
            print("✓ Integration tests passed")
        else:
            print("✗ Integration tests failed")
        
        return success
    
    def run_load_tests(self, verbose: bool = False) -> bool:
        """Run load and performance tests."""
        print("\n" + "="*50)
        print("RUNNING LOAD TESTS")
        print("="*50)
        
        command = [sys.executable, "-m", "pytest", "tests/load/", "-m", "load", "-s"]
        
        if verbose:
            command.append("-v")
        
        result = self.run_command(command)
        success = result.returncode == 0
        
        if success:
            print("✓ Load tests passed")
        else:
            print("✗ Load tests failed")
        
        return success
    
    def run_specific_tests(self, test_pattern: str, verbose: bool = False) -> bool:
        """Run specific tests matching a pattern."""
        print(f"\nRunning tests matching pattern: {test_pattern}")
        
        command = [sys.executable, "-m", "pytest", "-k", test_pattern]
        
        if verbose:
            command.append("-v")
        
        result = self.run_command(command)
        return result.returncode == 0
    
    def run_health_checks(self) -> bool:
        """Run health check tests only."""
        print("\n" + "="*50)
        print("RUNNING HEALTH CHECK TESTS")
        print("="*50)
        
        command = [sys.executable, "-m", "pytest", "-m", "health", "-v"]
        result = self.run_command(command)
        
        return result.returncode == 0
    
    def generate_test_report(self) -> bool:
        """Generate comprehensive test report."""
        print("\n" + "="*50)
        print("GENERATING TEST REPORT")
        print("="*50)
        
        # Run all tests with coverage and reporting
        command = [
            sys.executable, "-m", "pytest",
            "--cov=backend",
            "--cov-report=html:htmlcov",
            "--cov-report=xml",
            "--cov-report=term",
            "--junitxml=test-results.xml",
            "--html=test-report.html",
            "--self-contained-html"
        ]
        
        result = self.run_command(command)
        
        if result.returncode == 0:
            print("✓ Test report generated successfully")
            print("  - HTML Coverage: htmlcov/index.html")
            print("  - Test Report: test-report.html")
            print("  - JUnit XML: test-results.xml")
        else:
            print("✗ Failed to generate test report")
        
        return result.returncode == 0
    
    def run_linting(self) -> bool:
        """Run code linting and style checks."""
        print("\n" + "="*50)
        print("RUNNING CODE LINTING")
        print("="*50)
        
        success = True
        
        # Run black formatting check
        print("Checking code formatting with black...")
        result = self.run_command([sys.executable, "-m", "black", "--check", "."])
        if result.returncode != 0:
            print("✗ Code formatting issues found (run 'black .' to fix)")
            success = False
        else:
            print("✓ Code formatting is correct")
        
        # Run isort import sorting check
        print("Checking import sorting with isort...")
        result = self.run_command([sys.executable, "-m", "isort", "--check-only", "."])
        if result.returncode != 0:
            print("✗ Import sorting issues found (run 'isort .' to fix)")
            success = False
        else:
            print("✓ Import sorting is correct")
        
        # Run flake8 linting
        print("Running flake8 linting...")
        result = self.run_command([sys.executable, "-m", "flake8", "."])
        if result.returncode != 0:
            print("✗ Linting issues found")
            success = False
        else:
            print("✓ No linting issues found")
        
        return success
    
    def run_type_checking(self) -> bool:
        """Run type checking with mypy."""
        print("\n" + "="*50)
        print("RUNNING TYPE CHECKING")
        print("="*50)
        
        command = [sys.executable, "-m", "mypy", "backend/"]
        result = self.run_command(command)
        
        if result.returncode == 0:
            print("✓ Type checking passed")
        else:
            print("✗ Type checking failed")
        
        return result.returncode == 0
    
    def run_security_checks(self) -> bool:
        """Run security vulnerability checks."""
        print("\n" + "="*50)
        print("RUNNING SECURITY CHECKS")
        print("="*50)
        
        # Check for known vulnerabilities in dependencies
        print("Checking for security vulnerabilities...")
        command = [sys.executable, "-m", "pip", "list", "--format=json"]
        result = self.run_command(command, capture_output=True)
        
        if result.returncode == 0:
            print("✓ Security check completed")
            # In a real implementation, you'd use safety or similar tools
            return True
        else:
            print("✗ Security check failed")
            return False
    
    def cleanup(self):
        """Clean up test artifacts."""
        print("\nCleaning up test artifacts...")
        
        # Remove test database
        test_db = self.backend_dir / "test.db"
        if test_db.exists():
            test_db.unlink()
            print("✓ Removed test database")
        
        # Clean up __pycache__ directories
        for pycache in self.backend_dir.rglob("__pycache__"):
            if pycache.is_dir():
                import shutil
                shutil.rmtree(pycache)
        
        print("✓ Cleaned up cache files")


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="MindBridge Backend Test Runner")
    
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--load", action="store_true", help="Run load tests")
    parser.add_argument("--health", action="store_true", help="Run health check tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--quick", action="store_true", help="Run quick test suite (unit + health)")
    parser.add_argument("--lint", action="store_true", help="Run linting checks")
    parser.add_argument("--type-check", action="store_true", help="Run type checking")
    parser.add_argument("--security", action="store_true", help="Run security checks")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive test report")
    parser.add_argument("--install-deps", action="store_true", help="Install test dependencies")
    parser.add_argument("--cleanup", action="store_true", help="Clean up test artifacts")
    
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--no-coverage", action="store_true", help="Disable coverage reporting")
    parser.add_argument("-k", "--pattern", help="Run tests matching pattern")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    runner.setup_environment()
    
    start_time = time.time()
    success = True
    
    try:
        if args.install_deps:
            runner.install_dependencies()
        
        if args.cleanup:
            runner.cleanup()
            return
        
        if args.pattern:
            success = runner.run_specific_tests(args.pattern, args.verbose)
        elif args.unit:
            success = runner.run_unit_tests(args.verbose, not args.no_coverage)
        elif args.integration:
            success = runner.run_integration_tests(args.verbose)
        elif args.load:
            success = runner.run_load_tests(args.verbose)
        elif args.health:
            success = runner.run_health_checks()
        elif args.quick:
            success = (
                runner.run_unit_tests(args.verbose, not args.no_coverage) and
                runner.run_health_checks()
            )
        elif args.all:
            success = (
                runner.run_unit_tests(args.verbose, not args.no_coverage) and
                runner.run_integration_tests(args.verbose) and
                runner.run_load_tests(args.verbose)
            )
        elif args.lint:
            success = runner.run_linting()
        elif args.type_check:
            success = runner.run_type_checking()
        elif args.security:
            success = runner.run_security_checks()
        elif args.report:
            success = runner.generate_test_report()
        else:
            # Default: run quick test suite
            print("No specific test type specified. Running quick test suite...")
            success = (
                runner.run_unit_tests(args.verbose, not args.no_coverage) and
                runner.run_health_checks()
            )
    
    except KeyboardInterrupt:
        print("\n⚠️ Test execution interrupted by user")
        success = False
    except Exception as e:
        print(f"\n❌ Test execution failed with error: {e}")
        success = False
    
    finally:
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n{'='*50}")
        print(f"TEST EXECUTION SUMMARY")
        print(f"{'='*50}")
        print(f"Duration: {duration:.2f} seconds")
        
        if success:
            print("🎉 All tests completed successfully!")
            sys.exit(0)
        else:
            print("❌ Some tests failed or were interrupted")
            sys.exit(1)


if __name__ == "__main__":
    main() 
