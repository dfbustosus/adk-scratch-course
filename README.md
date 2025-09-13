# ADK Scratch Course 🤖

[![CI/CD](https://github.com/dfbustosus/adk-scratch-course/actions/workflows/ci.yml/badge.svg)](https://github.com/dfbustosus/adk-scratch-course/actions/workflows/ci.yml)
[![Documentation](https://github.com/dfbustosus/adk-scratch-course/actions/workflows/documentation.yml/badge.svg)](https://dfbustosus.github.io/adk-scratch-course)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive course on Google Development Kit (GDK) for building intelligent agents. Learn to create, deploy, and manage AI-powered agents using Google Cloud Platform and modern Python development practices.

## 🎯 What You'll Learn

This hands-on course covers everything from basic agent concepts to production deployment:

- **🤖 Agent Fundamentals**: Understanding intelligent agents and their architecture
- **🛠️ Development Setup**: Professional Python and Google Cloud environment
- **🔧 Agent Building**: Creating agents with different behaviors and capabilities
- **🌐 Cloud Integration**: Leveraging Google Cloud AI services and APIs
- **🚀 Production Deployment**: Scaling, monitoring, and maintaining agent systems
- **🔒 Security & Best Practices**: Authentication, authorization, and secure development

## 📚 Course Structure

### 🎓 Learning Path

| Lesson | Topic | Duration | Level |
|--------|-------|----------|-------|
| [01](lessons/lesson-01/) | Introduction to GDK and Agents | 2-3 hours | Beginner |
| [02](lessons/lesson-02/) | Development Environment Setup | 3-4 hours | Intermediate |
| [03](lessons/lesson-03/) | Basic Agent Architecture | 2-3 hours | Intermediate |
| [04](lessons/lesson-04/) | Agent Communication Patterns | 3-4 hours | Intermediate |
| [05](lessons/lesson-05/) | Data Processing and Analysis | 4-5 hours | Intermediate |
| [06](lessons/lesson-06/) | Google Services Integration | 4-5 hours | Advanced |
| [07](lessons/lesson-07/) | Advanced Agent Behaviors | 5-6 hours | Advanced |
| [08](lessons/lesson-08/) | Testing and Debugging | 3-4 hours | Advanced |
| [09](lessons/lesson-09/) | Performance Optimization | 4-5 hours | Advanced |
| [10](lessons/lesson-10/) | Security and Authentication | 3-4 hours | Advanced |
| [11](lessons/lesson-11/) | Deployment and Monitoring | 4-5 hours | Expert |
| [12](lessons/lesson-12/) | Best Practices & Advanced Topics | 3-4 hours | Expert |

### 🎯 Learning Tracks

**🌱 Beginner Track** (Lessons 1-4)

- Perfect for newcomers to AI agents
- Focus on fundamentals and basic implementation
- Hands-on exercises with guided solutions

**🚀 Intermediate Track** (Lessons 5-8)  

- Build practical, real-world applications
- Integrate with Google Cloud services
- Learn testing and debugging techniques

**⚡ Advanced Track** (Lessons 9-12)

- Production-ready development practices
- Performance optimization and scaling
- Security, monitoring, and maintenance

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ installed
- Google Cloud Platform account (free tier works!)
- Basic programming knowledge
- Command-line familiarity

### Installation

```bash
# Install the ADK Course framework
pip install adk-course

# Validate your environment
adk-course validate

# Create your first agent
adk-course init my-first-agent

# Test the agent
adk-course test --config agents/my-first-agent/config.yaml
```

### Your First Agent in 5 Minutes

```python
from adk_course import AgentConfig, BasicAgent
import asyncio

async def main():
    # Configure your agent
    config = AgentConfig(
        name="hello-world-agent",
        project_id="your-gcp-project-id",
        system_prompt="You are a helpful assistant who explains AI concepts clearly."
    )
    
    # Create and use the agent
    agent = BasicAgent(config)
    response = await agent.process_message("What is machine learning?")
    print(f"Agent: {response}")

# Run the example
asyncio.run(main())
```

## 🛠️ Development Setup

### For Contributors

```bash
# Clone the repository
git clone https://github.com/dfbustosus/adk-scratch-course.git
cd adk-scratch-course

# Set up development environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
make test
```

### Environment Configuration

Create a `.env` file:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
ADK_LOG_LEVEL=INFO
```

## 🧪 Testing

The project includes comprehensive testing:

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test categories
make test-unit
make test-integration

# Lint and format code
make lint
make format
```

## 📖 Documentation

- **📚 [Full Documentation](https://dfbustosus.github.io/adk-scratch-course)**: Complete course materials and API reference
- **🎓 [Lesson Materials](lessons/)**: Structured learning content with exercises
- **🔧 [API Reference](https://dfbustosus.github.io/adk-scratch-course/api/)**: Detailed code documentation
- **💡 [Examples](examples/)**: Practical code examples and templates

## 🏗️ Repository Structure

```text
adk-scratch-course/
├── .github/                 # GitHub workflows and templates
├── docs/                    # Documentation source
├── lessons/                 # Course lessons (01-12)
├── src/adk_course/         # Main Python package
│   ├── core.py             # Agent core functionality
│   ├── utils.py            # Utility functions
│   ├── cli.py              # Command-line interface
│   └── exceptions.py       # Custom exceptions
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── examples/               # Example agents and code
├── scripts/                # Utility scripts
├── pyproject.toml          # Project configuration
├── requirements*.txt       # Dependencies
├── Makefile               # Development commands
└── README.md              # This file!
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **🍴 Fork the repository**
2. **🌟 Star it** (if you like what you see!)
3. **🔧 Create a feature branch**: `git checkout -b feature/amazing-feature`
4. **✨ Make your changes** following our coding standards
5. **🧪 Add tests** for new functionality
6. **📝 Update documentation** as needed
7. **✅ Run the full test suite**: `make check`
8. **📤 Submit a pull request**

See our [Contributing Guide](.github/CONTRIBUTING.md) for detailed information.

### Development Commands

```bash
# Quality checks
make lint          # Run linting
make format        # Format code
make check         # Run all quality checks

# Testing
make test          # Run tests
make test-cov      # Run with coverage

# Documentation
make docs          # Build documentation
make serve-docs    # Serve docs locally

# Build and release
make build         # Build package
make clean         # Clean build artifacts
```

## 🎯 Use Cases

This course prepares you to build various types of intelligent agents:

### 🤖 Customer Service Agents

- Automated support and FAQ handling
- Multi-language customer interactions
- Escalation to human agents when needed

### 📊 Data Analysis Agents  

- Automated report generation
- Real-time data monitoring
- Intelligent data visualization

### ✍️ Content Generation Agents

- Blog post and article writing
- Social media content creation
- Documentation generation

### 🔄 Workflow Automation Agents

- Business process automation
- Task orchestration and scheduling
- Integration with existing systems

### 🎯 Decision Support Agents

- Recommendation systems
- Risk assessment and analysis
- Strategic planning assistance

## 🌟 Features

### 🛠️ Developer Experience

- **CLI Tools**: Rich command-line interface for development
- **Hot Reloading**: Fast development iteration
- **Interactive Chat**: Test agents in real-time
- **Configuration Management**: YAML-based agent configuration

### ☁️ Google Cloud Integration

- **Vertex AI**: Access to Google's ML models
- **Natural Language**: Advanced text processing
- **Vision AI**: Image and video analysis
- **Speech Services**: Voice interaction capabilities

### 🔒 Production Ready

- **Security**: Built-in authentication and authorization
- **Monitoring**: Comprehensive logging and metrics
- **Scaling**: Cloud-native deployment patterns
- **Testing**: Extensive test coverage and CI/CD

### 📈 Performance

- **Async/Await**: Non-blocking operations
- **Caching**: Intelligent response caching
- **Load Balancing**: Horizontal scaling support
- **Optimization**: Performance monitoring and tuning

## 🏆 Success Stories

Students who have completed this course have gone on to:

- Build production customer service bots handling 1000+ daily conversations
- Create data analysis agents saving 20+ hours per week of manual work
- Deploy content generation systems for marketing teams
- Develop internal tools that improved team productivity by 40%

## 📞 Support and Community

### 💬 Getting Help

- **📖 Documentation**: Check our comprehensive docs first
- **❓ GitHub Issues**: Report bugs or request features
- **💭 Discussions**: Ask questions and share ideas
- **👥 Community**: Connect with other learners

### 🐛 Found a Bug?

1. Check if it's already reported in [Issues](https://github.com/dfbustosus/adk-scratch-course/issues)
2. If not, create a new issue with:

   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment details

### 💡 Have an Idea?

We'd love to hear it! Create a [Feature Request](https://github.com/dfbustosus/adk-scratch-course/issues/new?template=feature_request.yml) with:
- Description of the feature
- Use case and benefits
- Any implementation ideas

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Special thanks to:

- **Google Cloud Team** for the amazing AI Platform and services
- **Open Source Community** for the fantastic Python packages we use
- **Early Adopters** who provided valuable feedback and contributions
- **Contributors** who help make this course better every day

## 📈 Project Status

- ✅ **Stable**: Core functionality tested and documented
- 🚀 **Active Development**: Regular updates and new features
- 🌟 **Community Driven**: Open to contributions and feedback
- 📚 **Well Documented**: Comprehensive guides and examples

---

<div align="center">

**Ready to build amazing AI agents? [Start with Lesson 01!](lessons/lesson-01/)**

[⭐ Star this repo](https://github.com/dfbustosus/adk-scratch-course) | [📖 Read the docs](https://dfbustosus.github.io/adk-scratch-course) | [💬 Join discussions](https://github.com/dfbustosus/adk-scratch-course/discussions)

</div>
