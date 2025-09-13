# ADK Agent Quickstart (v1.14.0)

## 1. Minimal Viable Agent
```python
# my_agent/agent.py
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="minimal_agent",
    model="gemini-2.0-flash",
    description="Basic agent template",
    instruction="Respond to user queries"
)
```

## 2. Essential Configurations

### 2.1 Environment Setup
```bash
# .env
API_KEY="your_ai_studio_key"  # Required for AI Studio
# OR
PROJECT_ID="your-project"     # Required for Vertex AI
LOCATION="us-central1"
```

### 2.2 Runtime Parameters
```yaml
# config.yaml
model_parameters:
  temperature: 0.7
  max_output_tokens: 1024
safety_settings:
  harassment: "block_none"
  medical: "block_high"
```

## 3. Core Development Workflow

1. Scaffold agent:
   ```bash
   adk scaffold research_agent
   ```
2. Implement tools:
   ```python
   @tool
def academic_search(query: str) -> list:
    """Verified academic search (minimum 3 keywords)"""
    if len(query.split()) < 3:
        raise ValueError("Academic queries require ≥3 keywords")
    return scholar_search(query)
   ```
3. Validate:
   ```bash
   adk validate
   pytest tests/
   ```
4. Run:
   ```bash
   adk web  # Interactive development
   adk run research_agent  # CLI execution
   ```

## 4. Next Steps
- Add monitoring with `adk.monitoring`
- Implement evaluation benchmarks
- Containerize for deployment

For detailed explanations, see:
- `agent_development.md` (Practical guide)
- `agent_development_advanced.md` (PhD-level concepts)
