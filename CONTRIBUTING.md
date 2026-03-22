# Contributing to Pothole-iQ

Thank you for your interest in contributing to Pothole-iQ! We welcome contributions from the community.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Basic knowledge of computer vision and AI

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/pothole-.git
   cd pothole-
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**
   ```bash
   python -m pytest tests/
   ```

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Keep the first line under 50 characters
- Add detailed description if needed

Example:
```
Add fallback detection for low-light images

- Implement adaptive thresholding
- Add morphological operations
- Improve contour detection accuracy
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Improve detection accuracy for different road types
- [ ] Add support for video analysis
- [ ] Implement real-time camera feed processing
- [ ] Add more export formats (Excel, CSV)

### Medium Priority
- [ ] Enhance UI/UX design
- [ ] Add multi-language support
- [ ] Implement user authentication
- [ ] Add database integration

### Low Priority
- [ ] Mobile app development
- [ ] API development
- [ ] Cloud deployment guides
- [ ] Performance optimizations

## 🐛 Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Error messages/logs

## 💡 Feature Requests

For new features:
- Describe the problem you're solving
- Explain your proposed solution
- Consider implementation complexity
- Think about backward compatibility

## 📝 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests if applicable
   - Update documentation

3. **Test your changes**
   ```bash
   python main.py
   streamlit run structured_dashboard.py
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add your feature"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use a clear title and description
   - Reference any related issues
   - Add screenshots for UI changes

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_detection.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Adding Tests
- Write tests for new features
- Ensure good test coverage
- Use descriptive test names
- Mock external dependencies

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions
- Use Google-style docstrings
- Include parameter types and return values

Example:
```python
def detect_potholes(image_path: str, scale_factor: float = 0.5) -> dict:
    """
    Detect potholes in the given image.
    
    Args:
        image_path (str): Path to the input image
        scale_factor (float): Conversion factor from pixels to cm²
        
    Returns:
        dict: Analysis results containing detection data
        
    Raises:
        FileNotFoundError: If image file doesn't exist
    """
```

### README Updates
- Update README.md for new features
- Add usage examples
- Update installation instructions if needed

## 🏆 Recognition

Contributors will be:
- Listed in the README.md
- Mentioned in release notes
- Invited to join the core team (for significant contributions)

## 📞 Getting Help

- 💬 Discussions: Use GitHub Discussions for questions
- 🐛 Issues: Report bugs via GitHub Issues
- 📧 Email: Contact maintainers directly for sensitive issues

## 📋 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Unprofessional conduct

## 🎉 Thank You!

Every contribution, no matter how small, helps make Pothole-iQ better for everyone. We appreciate your time and effort!

---

**Happy Contributing! 🚧✨**