# Contributing to Mental Health Multi-Modal AI System

Thank you for your interest in contributing to this project! 🎉

## 🤝 How to Contribute

### Reporting Issues
- Check if the issue already exists in [GitHub Issues](https://github.com/aaroohhiiii/mentalHealth/issues)
- Use a clear and descriptive title
- Provide detailed steps to reproduce the issue
- Include system information (OS, Python version, Node version)
- Add screenshots if applicable

### Suggesting Enhancements
- Clearly describe the enhancement and its benefits
- Explain why this would be useful to most users
- Provide examples of how it would work

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/aaroohhiiii/mentalHealth.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Ensure backend tests pass
   - Test frontend functionality
   - Check for console errors

5. **Commit your changes**
   ```bash
   git commit -m "Add some amazing feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Use a clear title and description
   - Reference any related issues
   - Include screenshots for UI changes

## 📝 Code Style Guidelines

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and modular

```python
def analyze_text(text: str) -> dict:
    """
    Analyze text input for mental health indicators.
    
    Args:
        text: User input text to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    pass
```

### TypeScript/React (Frontend)
- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable

```typescript
interface FeedbackCardProps {
  feedback: LLMFeedback;
  type: 'text' | 'audio' | 'image';
}

const FeedbackCard: React.FC<FeedbackCardProps> = ({ feedback, type }) => {
  // Component logic
};
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🔒 Security

- **Never commit sensitive data** (.env files, API keys, passwords)
- Use environment variables for configuration
- Follow security best practices for authentication
- Report security vulnerabilities privately

## 📧 Contact

For questions or discussions:
- Open a GitHub Discussion
- Email: support@mentalhealth-ai.com

## 🙏 Thank You!

Your contributions help make mental health support more accessible. Every contribution, no matter how small, makes a difference! ❤️
