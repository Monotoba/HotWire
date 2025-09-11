# Contributing to Wire Temperature Calculator

Thank you for your interest in contributing to the Wire Temperature Calculator! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use issue templates** when available
3. **Provide complete information**:
   - Operating system and version
   - Python version
   - Application version
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if relevant

### Suggesting Features

1. **Check if feature exists** in current version
2. **Explain the use case** clearly
3. **Describe proposed solution**
4. **Consider implementation complexity**

### Submitting Code Changes

#### Development Setup

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/wire-temperature-calculator.git
   cd wire-temperature-calculator
   ```

3. **Set up development environment**:
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Code Standards

**Style Guidelines:**
- Follow PEP 8 style guide
- Use Black formatter: `black src/`
- Maximum line length: 127 characters
- Use meaningful variable names
- Add docstrings to functions and classes

**Quality Requirements:**
- All tests must pass: `pytest tests/`
- Code coverage > 80%
- No linting errors: `flake8 src/`
- Type hints where appropriate: `mypy src/`

**Documentation:**
- Update docstrings for new functions
- Update user guide for new features
- Add examples for complex functionality

#### Testing

**Run all tests:**
```bash
pytest tests/ --cov=src/wire_temp_calc --cov-report=term
```

**Run specific test:**
```bash
pytest tests/test_wire_calculator.py::test_temperature_calculation
```

**Add new tests:**
- Place in appropriate test file
- Follow existing test patterns
- Test both success and failure cases
- Include edge cases

#### Commit Guidelines

**Commit Message Format:**
```
type(scope): brief description

Detailed explanation of changes
- What was changed
- Why it was changed
- Any breaking changes

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

**Examples:**
```
feat(foam-cutting): add EPP foam support

- Added EPP foam type with 220-260°C range
- Updated safety monitoring for EPP
- Added visual indicators for EPP cutting zone

Closes #45
```

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** if applicable
5. **Submit pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots for UI changes
   - Test results summary

#### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated

## Related Issues
Fixes #123
Closes #456
```

## Development Guidelines

### Architecture Principles

1. **Modularity**: Keep components separate and reusable
2. **Extensibility**: Design for future enhancements
3. **Safety First**: Always prioritize user safety
4. **Performance**: Optimize for responsiveness
5. **Accessibility**: Support diverse user needs

### Code Organization

```
src/wire_temp_calc/
├── __init__.py          # Package initialization
├── wire_temp_calculator.py  # Core calculator
├── foam_cutting.py      # Foam cutting module
├── unit_conversions.py  # Unit conversion utilities
├── main_window.py       # GUI implementation
├── cli.py              # Command line interface
└── resources/          # Icons, images, etc.
```

### Adding New Features

1. **Design Phase**:
   - Create issue with detailed specification
   - Discuss approach with maintainers
   - Consider backward compatibility
   - Plan for testing and documentation

2. **Implementation Phase**:
   - Follow existing code patterns
   - Add comprehensive tests
   - Update documentation
   - Consider edge cases

3. **Review Phase**:
   - Address reviewer feedback
   - Update based on testing
   - Final documentation review

### Performance Considerations

- **Temperature calculations**: Optimize for <1ms response time
- **GUI responsiveness**: Maintain 60 FPS for smooth interaction
- **Memory usage**: Minimize memory footprint
- **Battery life**: Efficient for laptop use

## Release Process

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. **Update version numbers** in `__init__.py`
2. **Update CHANGELOG.md** with release notes
3. **Test on all platforms** (Windows, macOS, Linux)
4. **Update documentation** for new features
5. **Create release notes** with highlights
6. **Tag release** in git
7. **Build distribution packages**
8. **Publish to PyPI** (if applicable)

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Email**: support@wiretempcalc.com for security issues

### Recognition

Contributors are recognized in:
- **CHANGELOG.md**: For significant contributions
- **GitHub Contributors**: Automatic recognition
- **Release notes**: For major features

## Questions?

If you have questions about contributing:

1. Check existing documentation
2. Search GitHub issues/discussions
3. Create new discussion for general questions
4. Email maintainers for sensitive topics

Thank you for contributing to the Wire Temperature Calculator project!