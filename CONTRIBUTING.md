# Contributing to PolicyRadar 🤝

Thank you for your interest in contributing to PolicyRadar! This document provides guidelines and information for contributors.

## 🎯 Project Overview

PolicyRadar is an enterprise-grade economic policy impact assessment system designed to help Fortune 500 companies anticipate regulatory changes and quantify their financial implications.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+
- Git

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/PolicyRadar.git
   cd PolicyRadar
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   python scripts/setup_database.py
   python scripts/generate_synthetic_data.py
   ```

4. **Run the application**
   ```bash
   # Terminal 1: Start API
   uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2: Start Dashboard
   streamlit run app/dashboard/main.py --server.port 8501
   ```

## 📋 Contribution Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all functions and classes
- Keep functions small and focused on a single responsibility

### Commit Messages

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(api): add new policy prediction endpoint
fix(dashboard): resolve API connection issue
docs(readme): update installation instructions
```

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests**
   ```bash
   python -m pytest tests/ -v
   python -m pytest tests/ --cov=app --cov=data
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description of the changes
   - Include any relevant issue numbers
   - Add screenshots for UI changes

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app --cov=data --cov-report=html

# Run specific test file
python -m pytest tests/test_specific.py -v

# Run tests in Docker
docker exec policyradar_api python -m pytest tests/ -v
```

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies
- Test both success and failure cases

### Test Structure
```
tests/
├── test_basic.py          # Basic functionality tests
├── test_synthetic_data.py # Data generation tests
├── test_api/              # API endpoint tests
├── test_models/           # Data model tests
└── test_integration/      # Integration tests
```

## 📚 Documentation

### Code Documentation
- Use docstrings for all functions and classes
- Follow Google docstring format
- Include type hints
- Document complex algorithms and business logic

### API Documentation
- Update API documentation when adding new endpoints
- Include request/response examples
- Document error codes and responses

### User Documentation
- Update README.md for user-facing changes
- Add new sections to docs/ as needed
- Include screenshots for UI changes

## 🏗️ Architecture Guidelines

### Project Structure
```
PolicyRadar/
├── app/                    # Main application
│   ├── api/               # FastAPI backend
│   ├── dashboard/         # Streamlit frontend
│   └── core/              # Core functionality
├── data/                  # Data models and generators
├── config/                # Configuration
├── scripts/               # Utility scripts
├── tests/                 # Test suite
└── docs/                  # Documentation
```

### Design Principles
- **Separation of Concerns**: Keep business logic separate from presentation
- **Dependency Injection**: Use dependency injection for external services
- **Error Handling**: Implement proper error handling and logging
- **Configuration**: Use environment variables for configuration
- **Security**: Follow security best practices

## 🔧 Development Workflow

### Feature Development
1. Create an issue describing the feature
2. Fork the repository
3. Create a feature branch
4. Implement the feature with tests
5. Update documentation
6. Create a pull request

### Bug Fixes
1. Create an issue describing the bug
2. Fork the repository
3. Create a bug fix branch
4. Implement the fix with tests
5. Create a pull request

### Code Review Process
1. All pull requests require review
2. Address review comments
3. Ensure all tests pass
4. Update documentation if needed
5. Merge after approval

## 🚨 Reporting Issues

### Bug Reports
When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and stack traces

### Feature Requests
When requesting features, please include:
- Clear description of the feature
- Use case and benefits
- Mockups or examples if applicable
- Priority level

## 📞 Getting Help

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Search existing [GitHub Issues](https://github.com/deluair/PolicyRadar/issues)
- **Discussions**: Use [GitHub Discussions](https://github.com/deluair/PolicyRadar/discussions)

## 🏆 Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributor hall of fame

## 📄 License

By contributing to PolicyRadar, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to PolicyRadar! 🎉 