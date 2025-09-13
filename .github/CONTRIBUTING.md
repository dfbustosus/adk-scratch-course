# Contributing to ADK Scratch Course

Thank you for your interest in contributing to the ADK Scratch Course! This document provides guidelines and instructions for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Lesson Content Guidelines](#lesson-content-guidelines)
- [Issue Guidelines](#issue-guidelines)
- [Pull Request Guidelines](#pull-request-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Exact steps to reproduce the problem
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error logs if applicable

### 💡 Suggesting Features

Feature suggestions are welcome! Please:

- Check if the feature already exists or has been requested
- Explain the problem your feature would solve
- Describe the proposed solution in detail
- Consider how it fits with the project's goals

### 📝 Improving Documentation

Documentation improvements are always appreciated:

- Fix typos, grammar, or unclear explanations
- Add missing information
- Improve code examples
- Update outdated content

### 🏗️ Contributing Code

Code contributions can include:

- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test improvements

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- A text editor or IDE

### Local Development Environment

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/your-username/adk-scratch-course.git
   cd adk-scratch-course
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

5. **Verify Setup**
   ```bash
   python -m pytest
   make lint
   ```

## Coding Standards

### Python Code Style

We follow PEP 8 with some modifications:

- **Line Length**: Maximum 88 characters (Black formatter default)
- **Import Sorting**: Use isort
- **Type Hints**: Required for all public functions and methods
- **Docstrings**: Google-style docstrings for all public APIs

### Code Quality Tools

The following tools are used to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing
- **pre-commit**: Git hooks

### Running Quality Checks

```bash
# Format code
make format

# Run all linting
make lint

# Run tests
make test

# Run all checks
make check
```

## Submitting Changes

### Branch Naming Convention

Use descriptive branch names with prefixes:

- `feature/add-new-lesson-content`
- `bugfix/fix-import-error`
- `docs/update-readme`
- `refactor/improve-agent-class`

### Commit Message Guidelines

Follow the conventional commits specification:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Maintenance tasks

**Examples:**
```
feat(lessons): add lesson 13 on advanced debugging
fix(examples): correct import paths in lesson 5
docs(readme): update installation instructions
```

### Pull Request Process

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   make test
   make lint
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Fill Out PR Template**
   - Use the provided PR template
   - Link to related issues
   - Describe changes made
   - Include testing information

## Lesson Content Guidelines

### Structure

Each lesson should follow this structure:

```
lessons/
├── lesson-XX-topic-name/
│   ├── README.md          # Main lesson content
│   ├── examples/          # Code examples
│   ├── exercises/         # Practice exercises
│   ├── solutions/         # Exercise solutions
│   └── resources/         # Additional resources
```

### Content Standards

- **Clear Learning Objectives**: Each lesson must have explicit learning goals
- **Progressive Difficulty**: Build upon previous lessons
- **Practical Examples**: Include working code examples
- **Hands-on Exercises**: Provide practice opportunities
- **Resources**: Link to relevant documentation and materials

### Writing Style

- Use clear, concise language
- Explain complex concepts step-by-step
- Include code comments for clarity
- Provide context for why something is important
- Use consistent terminology throughout

## Issue Guidelines

### Before Creating an Issue

- Search existing issues to avoid duplicates
- Check if it's already documented as a known limitation
- Ensure you're using the latest version

### Writing Good Issues

- Use descriptive titles
- Provide detailed descriptions
- Include reproduction steps for bugs
- Add environment information
- Use appropriate labels and templates

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)
- [ ] PR description is complete

### Review Process

1. **Automated Checks**: CI must pass
2. **Code Review**: At least one maintainer review required
3. **Testing**: Manual testing for significant changes
4. **Documentation**: Ensure docs are accurate and complete

### After Approval

- Squash commits if requested
- Ensure commit message follows conventions
- Maintainer will merge when ready

## Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/dfbustosus/adk-scratch-course.git
cd adk-scratch-course

# Set up Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run initial checks
make check
```

### Making Changes

1. Create feature branch
2. Make changes
3. Add tests
4. Update documentation
5. Run quality checks
6. Commit and push
7. Create pull request

### Testing

- Write unit tests for all new code
- Ensure integration tests pass
- Test documentation examples
- Verify cross-platform compatibility

## Questions and Support

If you have questions about contributing:

- Check the documentation
- Search existing issues
- Create a question issue using the template
- Join our community discussions

Thank you for contributing to the ADK Scratch Course! 🎉
