# Lesson 01: Introduction to Google Development Kit and Agents

## 🎯 Learning Objectives

By the end of this lesson, you will be able to:

- Understand the fundamentals of Google Development Kit (GDK) and agent-based systems
- Explain the core concepts of intelligent agents and their applications
- Set up your development environment for GDK agent development
- Create your first simple agent using the ADK Course framework

## 📚 Prerequisites

- Basic Python programming knowledge
- Understanding of object-oriented programming concepts
- Familiarity with command-line interfaces
- Google Cloud Platform account (free tier is sufficient)

## 🧠 What are Intelligent Agents?

### Definition

An **intelligent agent** is a software entity that:
- Perceives its environment through sensors
- Acts upon that environment through actuators
- Uses artificial intelligence to make decisions
- Works autonomously to achieve specific goals

### Key Characteristics

1. **Autonomy**: Agents operate without direct human intervention
2. **Reactivity**: Agents respond to changes in their environment
3. **Proactivity**: Agents take initiative to achieve their goals
4. **Social Ability**: Agents interact with other agents or humans

### Types of Agents

1. **Simple Reflex Agents**: React based on current percept
2. **Model-based Agents**: Maintain internal state
3. **Goal-based Agents**: Work towards specific objectives
4. **Utility-based Agents**: Optimize for best outcomes
5. **Learning Agents**: Improve performance over time

## 🌟 Google Development Kit (GDK) Overview

### What is GDK?

The Google Development Kit provides tools and APIs for building intelligent agents that integrate with Google's AI and cloud services. It offers:

- **Vertex AI Integration**: Access to Google's ML models
- **Natural Language Processing**: Advanced text understanding
- **Vision AI**: Image and video analysis capabilities
- **Speech Recognition**: Voice interaction support
- **Cloud Infrastructure**: Scalable deployment options

### Key Components

1. **Agent Framework**: Core structure for building agents
2. **Model APIs**: Access to pre-trained models
3. **Workflow Engine**: Orchestrate complex tasks
4. **Integration Tools**: Connect with external systems
5. **Monitoring & Analytics**: Track agent performance

### Use Cases

- **Customer Service Bots**: Automated support agents
- **Data Analysis Agents**: Intelligent data processing
- **Content Generation**: Automated content creation
- **Task Automation**: Workflow optimization
- **Decision Support Systems**: AI-powered recommendations

## 🛠️ Environment Setup

### 1. System Requirements

```bash
# Check Python version (3.9+ required)
python --version

# Check pip version
pip --version
```

### 2. Install ADK Course Framework

```bash
# Install the framework
pip install adk-course

# Verify installation
adk-course version
```

### 3. Google Cloud Setup

```bash
# Install Google Cloud CLI (if not already installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate with Google Cloud
gcloud auth login

# Set your default project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable language.googleapis.com
```

### 4. Environment Configuration

Create a `.env` file in your project directory:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
ADK_LOG_LEVEL=INFO
```

### 5. Validate Setup

```bash
# Run environment validation
adk-course validate
```

## 📝 Your First Agent

Let's create a simple "Hello World" agent to verify everything is working.

### Step 1: Initialize Agent

```bash
# Create a new agent
adk-course init hello-world-agent
```

This creates:
```
agents/hello-world-agent/
├── config.yaml          # Agent configuration
└── examples/
    └── hello-world-agent_example.py
```

### Step 2: Review Configuration

Open `agents/hello-world-agent/config.yaml`:

```yaml
name: hello-world-agent
description: Agent configuration for hello-world-agent
version: 1.0.0
project_id: your-google-cloud-project
location: us-central1
model_name: gemini-pro
temperature: 0.7
max_tokens: 1024
top_p: 0.9
top_k: 40
system_prompt: You are a helpful AI assistant.
max_retries: 3
timeout: 30.0
enable_safety: true
enable_logging: true
custom_parameters: {}
```

### Step 3: Test the Agent

```bash
# Test with a simple message
adk-course test --config agents/hello-world-agent/config.yaml --message "Hello, world!"

# Start interactive chat
adk-course chat --config agents/hello-world-agent/config.yaml
```

### Step 4: Customize Your Agent

Edit the configuration to personalize your agent:

```yaml
name: my-first-agent
description: My first intelligent agent for learning GDK
system_prompt: |
  You are a friendly learning assistant helping students understand 
  Google Development Kit and intelligent agents. Always be encouraging 
  and provide clear, helpful explanations.
temperature: 0.8
```

## 🔧 Understanding the Code

Let's examine how the basic agent works:

```python
from adk_course import AgentConfig, BasicAgent
import asyncio

async def main():
    # Create agent configuration
    config = AgentConfig(
        name="learning-assistant",
        project_id="your-project-id",
        system_prompt="You are a helpful learning assistant."
    )
    
    # Initialize the agent
    agent = BasicAgent(config)
    
    # Process a message
    response = await agent.process_message("What is artificial intelligence?")
    print(f"Agent: {response}")
    
    # Check agent status
    status = agent.get_status()
    print(f"Messages processed: {status['message_count']}")

# Run the example
asyncio.run(main())
```

### Key Components Explained

1. **AgentConfig**: Defines agent behavior and settings
2. **BasicAgent**: Implements core agent functionality
3. **process_message()**: Handles input and generates responses
4. **Session History**: Maintains conversation context

## 🎯 Exercises

### Exercise 1: Agent Personality

Create an agent with a specific personality:

1. Modify the `system_prompt` to give your agent a unique personality
2. Test different temperature values (0.1 to 2.0)
3. Observe how the responses change

**Example personalities to try:**
- Professional business assistant
- Creative writing helper
- Scientific researcher
- Friendly teacher

### Exercise 2: Configuration Exploration

Experiment with different configuration parameters:

1. Change `max_tokens` (try 100, 500, 2000)
2. Modify `top_p` and `top_k` values
3. Test different `timeout` settings
4. Document how each change affects the agent's behavior

### Exercise 3: Conversation Analysis

Create a longer conversation and analyze:

1. Use the chat interface for a 10-message conversation
2. Use the `history` command to review the conversation
3. Check the agent status to see message counts
4. Clear history and start fresh

## 🔍 Key Concepts Review

### Agent Architecture
- **Configuration**: Settings that define agent behavior
- **Message Processing**: How agents understand and respond
- **Session Management**: Maintaining conversation context
- **Status Monitoring**: Tracking agent performance

### GDK Integration
- **Cloud Services**: Leveraging Google's AI infrastructure
- **Model Selection**: Choosing appropriate AI models
- **Safety Features**: Built-in content filtering
- **Scalability**: Cloud-based deployment options

## 🚀 Next Steps

In the next lesson, we'll dive deeper into:
- Setting up a professional development environment
- Understanding agent architecture patterns
- Implementing custom agent behaviors
- Working with different AI models

## 📚 Additional Resources

### Documentation
- [Google Cloud AI Platform](https://cloud.google.com/ai-platform)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [ADK Course Documentation](https://dfbustosus.github.io/adk-scratch-course)

### Tutorials
- [Google AI for Developers](https://developers.google.com/ai)
- [Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course)

### Community
- [ADK Course GitHub Discussions](https://github.com/dfbustosus/adk-scratch-course/discussions)
- [Google AI Community](https://developers.google.com/community)

## ✅ Lesson Checklist

- [ ] Environment setup completed
- [ ] First agent created and tested
- [ ] Configuration customization explored
- [ ] Basic concepts understood
- [ ] Exercises completed
- [ ] Ready for Lesson 02

---

**Estimated Time**: 2-3 hours  
**Difficulty**: Beginner  
**Prerequisites**: Python basics, Google Cloud account