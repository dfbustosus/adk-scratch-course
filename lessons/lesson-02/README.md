# Lesson 02: Setting Up Your Development Environment

## 🎯 Learning Objectives

By the end of this lesson, you will be able to:

- Set up a professional Python development environment for agent development
- Configure Google Cloud Platform services for GDK integration
- Understand project structure and organization best practices
- Use development tools for debugging, testing, and code quality
- Create reproducible development environments using Docker

## 📚 Prerequisites

- Completion of Lesson 01
- Google Cloud Platform account with billing enabled
- Basic understanding of command-line interfaces
- Familiarity with Git version control

## 🏗️ Professional Development Setup

### 1. Python Environment Management

#### Using pyenv for Python Version Management

```bash
# Install pyenv (macOS/Linux)
curl https://pyenv.run | bash

# Install specific Python version
pyenv install 3.11.7
pyenv global 3.11.7

# Verify installation
python --version
```

#### Virtual Environment Setup

```bash
# Create project directory
mkdir adk-agent-project
cd adk-agent-project

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip
```

### 2. IDE and Editor Configuration

#### Visual Studio Code Setup

Recommended extensions:
- Python (Microsoft)
- Pylance (Microsoft)
- Black Formatter (Microsoft)
- isort (Microsoft)
- autoDocstring (Nils Werner)
- GitLens (GitKraken)
- Docker (Microsoft)

#### VS Code Settings (`settings.json`)

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## ☁️ Google Cloud Platform Setup

### 1. Project Configuration

```bash
# Create new project
gcloud projects create adk-course-project --name="ADK Course Project"

# Set default project
gcloud config set project adk-course-project

# Enable billing (required for AI Platform)
gcloud billing projects link adk-course-project --billing-account=YOUR_BILLING_ACCOUNT
```

### 2. Enable Required APIs

```bash
# Enable essential APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable language.googleapis.com
gcloud services enable translate.googleapis.com
gcloud services enable speech.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable automl.googleapis.com
gcloud services enable dialogflow.googleapis.com
```

### 3. Service Account Setup

```bash
# Create service account
gcloud iam service-accounts create adk-agent-sa \
    --display-name="ADK Agent Service Account" \
    --description="Service account for ADK agent development"

# Grant necessary roles
gcloud projects add-iam-policy-binding adk-course-project \
    --member="serviceAccount:adk-agent-sa@adk-course-project.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding adk-course-project \
    --member="serviceAccount:adk-agent-sa@adk-course-project.iam.gserviceaccount.com" \
    --role="roles/ml.admin"

# Create and download key
gcloud iam service-accounts keys create ./credentials/service-account.json \
    --iam-account=adk-agent-sa@adk-course-project.iam.gserviceaccount.com
```

## 📁 Project Structure Best Practices

### Recommended Directory Layout

```
adk-agent-project/
├── agents/                 # Agent configurations
│   ├── production/        # Production agents
│   ├── development/       # Development agents
│   └── experimental/      # Experimental agents
├── src/                   # Source code
│   └── my_agents/        # Custom agent modules
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/              # End-to-end tests
├── docs/                  # Documentation
├── notebooks/             # Jupyter notebooks
├── data/                  # Data files
│   ├── raw/              # Raw data
│   ├── processed/        # Processed data
│   └── models/           # Saved models
├── scripts/               # Utility scripts
├── configs/               # Configuration files
├── credentials/           # Service account keys
├── logs/                  # Log files
├── .env                   # Environment variables
├── .env.template         # Environment template
├── .gitignore            # Git ignore rules
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── pyproject.toml        # Project configuration
├── Makefile              # Build automation
└── README.md             # Project documentation
```

### Initialize Project Structure

```bash
# Create directories
mkdir -p agents/{production,development,experimental}
mkdir -p src/my_agents
mkdir -p tests/{unit,integration,e2e}
mkdir -p docs notebooks data/{raw,processed,models}
mkdir -p scripts configs credentials logs

# Create initial files
touch .env.template
touch src/my_agents/__init__.py
touch tests/__init__.py
```

## 🛠️ Development Tools Configuration

### 1. Code Quality Tools

Create `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = "-v --tb=short --strict-markers"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
```

### 2. Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
EOF

# Install hooks
pre-commit install
```

### 3. Environment Variables

Create `.env.template`:

```env
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=./credentials/service-account.json

# ADK Configuration
ADK_LOG_LEVEL=INFO
ADK_LOG_FORMAT=json
ADK_DEBUG=false

# Development Configuration
PYTHONPATH=./src
ENVIRONMENT=development

# Optional: API Keys for third-party services
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

## 🐳 Docker Development Environment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK
RUN curl https://sdk.cloud.google.com | bash
ENV PATH="/root/google-cloud-sdk/bin:${PATH}"

# Copy requirements
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy source code
COPY . .

# Install package in development mode
RUN pip install -e .

# Set environment variables
ENV PYTHONPATH=/app/src
ENV GOOGLE_CLOUD_PROJECT=adk-course-project

# Expose ports
EXPOSE 8000 8080

# Default command
CMD ["bash"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  adk-dev:
    build: .
    container_name: adk-development
    volumes:
      - .:/app
      - ~/.config/gcloud:/root/.config/gcloud
    environment:
      - GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
      - GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account.json
    ports:
      - "8000:8000"
      - "8080:8080"
    command: tail -f /dev/null

  jupyter:
    build: .
    container_name: adk-jupyter
    volumes:
      - .:/app
    ports:
      - "8888:8888"
    command: jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

## 🧪 Testing Setup

### Test Structure

```python
# tests/conftest.py
import pytest
import os
from unittest.mock import Mock, patch

@pytest.fixture
def mock_gcp():
    """Mock Google Cloud Platform services."""
    with patch('google.cloud.aiplatform.init'):
        with patch('google.auth.default') as mock_auth:
            mock_auth.return_value = (Mock(), 'test-project')
            yield

@pytest.fixture
def test_config():
    """Provide test configuration."""
    return {
        'name': 'test-agent',
        'project_id': 'test-project',
        'location': 'us-central1'
    }
```

### Sample Test

```python
# tests/unit/test_agent.py
import pytest
from adk_course import AgentConfig, BasicAgent

def test_agent_creation(mock_gcp, test_config):
    """Test basic agent creation."""
    config = AgentConfig(**test_config)
    agent = BasicAgent(config)
    
    assert agent.config.name == 'test-agent'
    assert agent.id is not None
```

## 🔍 Debugging Tools

### Logging Configuration

```python
# src/my_agents/logging_config.py
import logging
import structlog
from pathlib import Path

def setup_logging(log_level="INFO", log_dir="logs"):
    """Configure structured logging."""
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    logging.basicConfig(
        filename=log_path / "agent.log",
        level=getattr(logging, log_level),
        format="%(message)s"
    )
```

### Debugging with pdb

```python
# Example debugging session
import pdb

async def process_message(self, message):
    pdb.set_trace()  # Debugger breakpoint
    response = await self.model.generate(message)
    return response
```

## 📊 Monitoring and Observability

### Health Check Endpoint

```python
# src/my_agents/health.py
from fastapi import FastAPI
import psutil
import time

app = FastAPI()

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "memory_usage": psutil.virtual_memory().percent,
        "cpu_usage": psutil.cpu_percent()
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes."""
    # Add checks for dependencies
    return {"status": "ready"}
```

## 🎯 Exercises

### Exercise 1: Environment Setup

1. Set up a complete development environment following this lesson
2. Create a new GCP project with all required APIs enabled
3. Configure VS Code with recommended extensions
4. Test the setup by creating and running a simple agent

### Exercise 2: Project Structure

1. Initialize a project using the recommended directory structure
2. Create appropriate `.gitignore` and `.env.template` files
3. Set up pre-commit hooks and run them on sample code
4. Create a simple `Makefile` with common development tasks

### Exercise 3: Docker Development

1. Create a Dockerfile for your development environment
2. Set up Docker Compose with development and Jupyter services
3. Test running agents inside containers
4. Configure volume mounting for live code reloading

### Exercise 4: Testing Infrastructure

1. Set up pytest with appropriate configuration
2. Create test fixtures for common testing scenarios
3. Write unit tests for a simple agent
4. Configure coverage reporting

## 📚 Additional Resources

### Development Tools
- [Visual Studio Code](https://code.visualstudio.com/)
- [PyCharm Professional](https://www.jetbrains.com/pycharm/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Google Cloud Documentation
- [AI Platform Documentation](https://cloud.google.com/ai-platform/docs)
- [Service Account Best Practices](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys)
- [Cloud SDK Installation](https://cloud.google.com/sdk/docs/install)

### Python Development
- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Documentation](https://pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)

## ✅ Lesson Checklist

- [ ] Professional Python environment configured
- [ ] Google Cloud Platform project set up with required APIs
- [ ] Development tools and IDE configured
- [ ] Project structure created following best practices
- [ ] Docker development environment working
- [ ] Testing infrastructure in place
- [ ] Code quality tools configured
- [ ] Exercises completed
- [ ] Ready for Lesson 03

---

**Estimated Time**: 3-4 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Lesson 01, Basic command-line skills
