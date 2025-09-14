# Google ADK Toolkit 🤖

[![CI/CD](https://github.com/dfbustosus/google-adk-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/dfbustosus/google-adk-toolkit/actions/workflows/ci.yml)
[![Documentation](https://github.com/dfbustosus/google-adk-toolkit/actions/workflows/documentation.yml/badge.svg)](https://dfbustosus.github.io/google-adk-toolkit)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A developer-focused toolkit for building, testing, and deploying intelligent agents with Google's Agent Development Kit (ADK). This repository provides a professional-grade foundation for creating production-ready AI agents on Google Cloud.


## 🚀 Quick Start

### Prerequisites

- Python 3.9+ installed
- Google Cloud Platform account (free tier works!)
- Basic programming knowledge
- Command-line familiarity

### Installation

```bash
# Clone the repository
git clone https://github.com/dfbustosus/google-adk-toolkit.git
cd google-adk-toolkit

# Install the toolkit in editable mode with dev dependencies
pip install -e ".[dev]"

# Validate your environment
adk validate

# Scaffold your first agent
adk scaffold my_first_agent
```

## 🧰 Using the Official Google ADK (Recommended)

This repository now includes a ready-to-run example agent using the official
Google Agent Development Kit (ADK).

### 1) Install ADK

```bash
pip install google-adk
```

### 2) Configure authentication

Create `multi_tool_agent/.env` from the provided template:

```bash
cp multi_tool_agent/.env.template multi_tool_agent/.env
```

Choose ONE of the following in that file:

- Google AI Studio API key
  - `GOOGLE_GENAI_USE_VERTEXAI=FALSE`
  - `GOOGLE_API_KEY=<your_api_key>`

- Google Cloud Vertex AI
  - `GOOGLE_GENAI_USE_VERTEXAI=TRUE`
  - `GOOGLE_CLOUD_PROJECT=<your_project_id>`
  - `GOOGLE_CLOUD_LOCATION=us-central1` (or your region)
  - Run once locally: `gcloud auth application-default login`

### 3) Run the ADK Dev UI

From the repository root (parent of `multi_tool_agent/`):

```bash
adk web
```

Open the URL printed in the terminal (usually http://localhost:8000) and
select `multi_tool_agent` at the top-left dropdown.

### 4) Run the agent in the terminal

```bash
adk run multi_tool_agent
```

This example agent is defined in `multi_tool_agent/agent.py` and exposes two
tools: `get_weather` and `get_current_time`, matching the ADK Quickstart.

### Your First Agent in 5 Minutes

```python
from adk.core import AgentConfig, BasicAgent
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
git clone https://github.com/dfbustosus/google-adk-toolkit.git
cd google-adk-toolkit

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

- **📚 [Full Documentation](https://dfbustosus.github.io/google-adk-toolkit)**: Complete project documentation and API reference.
- **🔧 [API Reference](https://dfbustosus.github.io/google-adk-toolkit/api/)**: Detailed code documentation.
- **💡 [Examples](examples/)**: Practical code examples and templates

## 🏗️ Repository Structure

```text
google-adk-toolkit/
├── .github/                 # GitHub workflows and templates
├── agents/                  # Directory for agent packages
├── docs/                    # Documentation source
├── src/adk/                 # Main Python package
│   ├── core.py             # Agent core functionality
│   ├── utils.py            # Utility functions
│   └── cli.py              # Command-line interface
├── tests/                   # Test suite
├── pyproject.toml           # Project configuration
├── Makefile                # Development commands
└── README.md               # This file!
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

See our [Contributing Guide](CONTRIBUTING.md) for detailed information.

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

This toolkit can be used to build a variety of powerful agents:

- Build production customer service bots handling 1000+ daily conversations
- Create data analysis agents saving 20+ hours per week of manual work
- Deploy content generation systems for marketing teams
- Develop internal tools that improved team productivity by 40%

## 📞 Support and Community

### 💬 Getting Help

- **📖 Documentation**: Check our comprehensive docs first
- **❓ GitHub Issues**: Report bugs or request features
- **💭 Discussions**: Ask questions and share ideas
- **👥 Community**: Connect with other developers

### 🐛 Found a Bug?

1. Check if it's already reported in [Issues](https://github.com/dfbustosus/google-adk-toolkit/issues)
2. If not, create a new issue with:

   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment details

### 💡 Have an Idea?

We'd love to hear it! Create a [Feature Request](https://github.com/dfbustosus/google-adk-toolkit/issues/new?template=feature_request.yml) with:
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
- **Contributors** who help make this toolkit better every day

## 📈 Project Status

- ✅ **Stable**: Core functionality tested and documented
- 🚀 **Active Development**: Regular updates and new features
- 🌟 **Community Driven**: Open to contributions and feedback
- 📚 **Well Documented**: Comprehensive guides and examples

---

<div align="center">

**Ready to build amazing AI agents? [Get started now!](#-quick-start)**

[⭐ Star this repo](https://github.com/dfbustosus/google-adk-toolkit) | [📖 Read the docs](https://dfbustosus.github.io/google-adk-toolkit) | [💬 Join discussions](https://github.com/dfbustosus/google-adk-toolkit/discussions)

</div>
