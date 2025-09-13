# Changelog

All notable changes to the ADK Scratch Course project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project structure and framework
- Comprehensive course materials (12 lessons)
- Core agent functionality with Google Cloud integration
- CLI tools for agent development and testing
- Complete CI/CD pipeline with GitHub Actions
- Documentation site with Sphinx
- Testing infrastructure with pytest
- Code quality tools (black, isort, flake8, mypy)
- Docker development environment
- Pre-commit hooks for code quality
- Issue and PR templates
- Contributing guidelines and security policy

### Features
- `AgentConfig` class for flexible agent configuration
- `BasicAgent` implementation for quick prototyping
- CLI commands: `init`, `test`, `chat`, `validate`
- Environment validation and setup utilities
- Structured logging with configurable output formats
- Configuration file management (YAML support)
- Error handling with custom exception classes

### Documentation
- Complete course materials covering beginner to expert levels
- API documentation with examples
- Installation and setup guides
- Contributing guidelines
- Security policy
- Code of conduct (planned)

### Development
- Modern Python packaging with `pyproject.toml`
- GitHub Actions workflows for CI/CD
- Pre-commit hooks for automated quality checks
- Docker support for consistent development environments
- Makefile with common development tasks
- Comprehensive test suite with mocking

## [1.0.0] - 2024-01-XX (Planned)

### Added
- First stable release
- All 12 lessons complete with exercises
- Production-ready agent examples
- Integration with Google Cloud services
- Performance optimization features
- Security hardening
- Monitoring and observability tools

### Changed
- API stabilization
- Documentation improvements
- Enhanced error messages
- Better CLI experience

### Fixed
- Cross-platform compatibility issues
- Memory optimization
- Error handling improvements

---

## Release Notes Template

### [Version] - YYYY-MM-DD

#### Added
- New features and capabilities

#### Changed
- Changes in existing functionality

#### Deprecated
- Soon-to-be removed features

#### Removed
- Now removed features

#### Fixed
- Bug fixes

#### Security
- Security improvements and fixes

---

## Contributing to the Changelog

When contributing to this project, please:

1. Add your changes to the `[Unreleased]` section
2. Follow the format: `- Description of change (#PR-number) @username`
3. Use the appropriate category (Added, Changed, Deprecated, Removed, Fixed, Security)
4. Keep entries concise but descriptive
5. Link to relevant issues or PRs when applicable

Example:
```
### Added
- New agent template for customer service bots (#123) @username
- Support for custom model endpoints (#124) @username

### Fixed
- Memory leak in conversation history (#125) @username
- CLI crash on invalid configuration (#126) @username
```
