# Advanced Agent Development Guide (PhD-Level)

## 1. Theoretical Foundations
### 1.1 Agent Architecture Principles
- Based on Google's Agent Builder Framework (Google Research, 2024)
- Implements ReAct paradigm (Yao et al., 2022)
- Combines LLM reasoning with tool execution

## 2. Implementation Methodology
### 2.1 Core Class Structure
```python
from google.adk.agents import LlmAgent
from google.adk.tools import tool
from pydantic import BaseModel

class AgentConfig(BaseModel):
    """Configuration following ADK v1.14.0 specs"""
    model: str = "gemini-2.0-flash"
    temperature: float = 0.7
    max_tokens: int = 1024

class ResearchAgent(LlmAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(
            name="research_agent",
            model=config.model,
            description="Academic research assistant",
            instruction="""
            You are a PhD-level research assistant. Verify all claims 
            with primary sources and maintain academic rigor.
            """
        )
```

### 2.2 Tool Development Protocol
1. Input Validation
2. Error Handling
3. Citations

```python
@tool
def search_scholar(query: str) -> dict:
    """
    Searches Google Scholar for academic papers.
    Args:
        query: Search terms (must contain at least 3 keywords)
    Returns:
        dict: {title: str, authors: str, year: int, citation: str}
    """
    if len(query.split()) < 3:
        raise ValueError("Query too broad - specify at least 3 keywords")
    
    # Implementation using Scholar API
    return results
```

## 3. Verification & Validation
### 3.1 Testing Framework
```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def agent_config():
    return AgentConfig()

@pytest.mark.asyncio
async def test_scholar_search(agent_config):
    agent = ResearchAgent(agent_config)
    results = await agent.search_scholar("LLM agent architecture 2024")
    assert len(results) > 0
    assert "citation" in results[0]
```

## 4. References
1. Google ADK Technical White Paper (2024)
2. ReAct: Synergizing Reasoning and Acting (Yao et al., 2022)
3. Gemini API Specifications v1.14.0
4. ADK Security Guidelines (Google Cloud, 2024)
