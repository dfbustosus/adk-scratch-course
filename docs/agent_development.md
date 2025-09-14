# Agent Development Guide (ADK v1.14.0)

## 1. Prerequisites

### 1.1 System Requirements
- Python 3.11+ (verified with 3.11.6)
- Google ADK 1.14.0+ (`pip install google-adk`)
- Valid authentication:
  - AI Studio: API key
  - Vertex AI: Project ID + Service Account

### 1.2 Development Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
```

## 2. Agent Architecture

### 2.1 Core Components
1. **Agent Class**: Inherits from `google.adk.agents.LlmAgent`
2. **Tools**: Modular functions for specific capabilities
3. **Configuration**: `.env` for credentials, `config.yaml` for settings

### 2.2 Scaffolding
```bash
adk scaffold <agent_name>
```

Requirements:
- Name must be valid Python identifier (letters, numbers, underscores)
- Directory structure:
  ```
  agent_name/
    ├── __init__.py
    ├── agent.py
    ├── .env.template
    └── config.yaml
  ```

## 3. Implementation

### 3.1 Basic Agent Template
```python
from google.adk.agents import LlmAgent

class MyAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            name="my_agent",
            model="gemini-2.0-flash",
            description="Agent description",
            instruction="System prompt"
        )

root_agent = MyAgent()
```

### 3.2 Adding Tools
```python
from google.adk.tools import tool

@tool
def get_weather(location: str) -> str:
    """Returns weather for given location"""
    # Implementation
    return weather_data
```

## 4. Configuration

### 4.1 Environment Variables
```bash
# .env file
API_KEY=your_ai_studio_key  # For AI Studio
# OR
PROJECT_ID=your-project     # For Vertex AI
LOCATION=us-central1
```

### 4.2 Runtime Configuration
```yaml
# config.yaml
model: gemini-2.0-flash
temperature: 0.7
max_tokens: 1024
```

## 5. Deployment

### 5.1 Local Testing
```bash
# Run in development mode
adk web

# CLI execution
adk run <agent_name>
```

### 5.2 Production Deployment
1. Containerize using provided Dockerfile
2. Deploy to:
   - Google Cloud Run
   - Vertex AI Prediction

## 6. Best Practices

### 6.1 Error Handling
- Implement retry logic for API calls
- Validate all tool inputs/outputs
- Use structured logging

### 6.2 Testing
- Unit tests for all tools
- Integration tests for agent flows
- Load testing for production

## References
1. [Google ADK Official Documentation](https://cloud.google.com/agent-builder-sdk/docs)
2. [ADK Python API Reference](https://googleapis.dev/python/adk/latest)
3. [Gemini API Best Practices](https://ai.google.dev/docs/gemini_api_best_practices)
