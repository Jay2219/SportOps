# SportOps: AI-Powered Sports Analysis System

> An intelligent multi-agent framework for comprehensive sports analysis using AI, video analysis, statistical research, and medical insights.

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/5672ddf8-f779-4a69-896b-f55c66e5a30e" />

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [System Architecture](#system-architecture)
- [Agent Framework](#agent-framework)
- [Setup & Installation](#setup--installation)
- [Project Structure](#project-structure)
- [Technologies](#technologies)

---

## Problem Statement

Modern sports analysis requires synthesizing multiple data sources - video footage, statistical data, research articles, medical records, and performance metrics - into actionable insights. This traditionally requires multiple specialists working across different domains.

**Key Challenges:**
- **Fragmented Data Sources** - Videos, statistics, medical records, research articles scattered across platforms
- **Time-Consuming Manual Analysis** - Domain expertise required across multiple disciplines (biomechanics, medicine, statistics, video analysis)
- **Interdisciplinary Perspective** - Need for coordinated insights from video analysis, tactical analysis, medical history, and performance metrics
- **Scalability Issues** - Difficult to scale analysis to handle large datasets and multiple athletes
- **Consistency & Quality** - Maintaining consistent analysis quality across different specialists and time periods

---

## Solution Overview

**SportOps** is an AI-powered multi-agent system that orchestrates specialized AI agents to collaboratively analyze sports performance from multiple angles. The system leverages:

- **Google Gemini AI** for intelligent reasoning and analysis
- **Multi-Agent Orchestration** (Google ADK A2A) for coordinated analysis workflows
- **Specialized Sub-Agents** for domain-specific expertise (video analysis, data research, medical analysis, etc.)
- **Stateful Session Management** to maintain context across analysis phases

### Key Benefits

✅ **Comprehensive Multi-Perspective Analysis** - Combines video, statistics, medical, tactical, and biomechanical insights  
✅ **Intelligent Orchestration** - Agents work sequentially and in parallel based on analysis requirements  
✅ **Scalable Architecture** - Modular design enables easy addition of new specialized agents  
✅ **Context-Aware Processing** - Session state tracking maintains continuity across analysis phases  
✅ **Extensible Integration** - Simple API for connecting external data sources and analysis tools  

---

## System Architecture

### High-Level System Architecture
![SportOps Agentic System Architecture](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F10387611%2F806026fa972cd7bc91deaefab379b344%2FSportOps.png?generation=1764610951031405&alt=media)

---

## Agent Framework

### Agent Hierarchy

```
Root Agent (Sequential Orchestrator)
│
├─ Data Researcher Agent
│  ├─ Stats Researcher Agent (Google Search for statistics)
│  └─ Information Researcher Agent (Web articles, interviews)
│
├─ Performance Analyst Agent
│  ├─ Tactical Analyst Agent (Game strategy analysis)
│  ├─ Performance Analyst Agent (KPI and metrics evaluation)
│  └─ Physio Agent (Physical conditioning analysis)
│
├─ Medical Analyst Agent
│  ├─ Medical Analyst Agent (Medical history & conditions)
│  ├─ Medical Historian Agent (Historical medical background)
│  └─ Biomechanics Agent (Movement & injury analysis)
│
└─ Head Analyst Agent (Synthesis & Reporting)
```

### Agent Responsibilities

| Agent | Purpose | Input Sources | Output |
|-------|---------|---|---|
| **Data Researcher** | Gather contextual information and statistics | Web search, APIs, databases | Research summaries, statistical context |
| **Performance Analyst** | Evaluate athletic performance metrics | Video, statistics, fitness data | Performance insights, KPI analysis |
| **Medical Analyst** | Assess medical history and health factors | Medical records, injury history | Medical assessment, health recommendations |
| **Head Analyst** | Synthesize all inputs into final report | All previous agent outputs | Comprehensive analysis report |
| **Video Analyst** | Analyze video for technique and tactics | Video files | Frame-by-frame analysis, tactical breakdown |
| **Tactical Analyst** | Evaluate game strategy and positioning | Video, game stats | Tactical insights, strategy assessment |
| **Biomechanics Agent** | Analyze movement patterns | Video, motion data | Biomechanical analysis, injury risk |

---

## Setup & Installation

### Prerequisites

### 1. Python
- [Download Python](https://www.python.org/downloads/)

### 2. UV (Astral Framework)
- [UV Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

### 3. Gemini API 
- [Gemini API Key Generation Guide](https://aistudio.google.com/app/apikey)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Jay2219/SportOps.git
cd SportOps
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
uv -m venv .venv

# Activate on Windows
.\.venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install project with all dependencies
uv sync
```

### Step 4: Configure Google AI Access

```bash
# Option 1: Using service account credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Option 2: Using API Key
export GEMINI_API_KEY="your-api-key-here"

# Option 3: Using gcloud CLI
gcloud auth application-default login
```

### Step 5: Run the Application

```bash
# Run main application
uv run adk web
```

---

## Project Structure

```
SprtOps/
│
├── main.py                          # Application entry point
├── pyproject.toml                   # Project metadata & dependencies
├── README.md                        # This documentation
├── LICENSE                          # MIT License
│
├── sports_analyst/                  # Main agent framework
│   ├── agent.py                     # Root agent orchestration & runner setup
│   ├── config.py                    # Agent configuration & settings
│   ├── callback_config.py           # Callback handlers for agent lifecycle
│   ├── __init__.py                  # Package initialization
│   │
│   ├── sub_agents/                  # Primary analysis agents
│   │   ├── __init__.py
│   │   ├── data_researcher_agent.py          # Research coordination
│   │   ├── performance_analyst_agent.py      # Performance evaluation
│   │   ├── medical_analyst_agent.py          # Medical assessment
│   │   ├── head_analyst_agent.py             # Synthesis & reporting
│   │   ├── video_analyst_agent.py            # Video analysis
│   │   ├── tactical_analyst_agent.py         # Tactical strategy
│   │   ├── biomechanics_agent.py             # Biomechanical analysis
│   │   ├── stats_researcher_agent.py         # Statistical research
│   │   ├── information_researcher_agent.py   # Information gathering
│   │   ├── medical_historian_agent.py        # Medical history
│   │   ├── physio_agent.py                   # Physiology analysis
│   │   └──
│   └──
│
└── [Additional configuration and cache files]
```

### Key File Descriptions

- **`agent.py`** - Defines the root agent as a SequentialAgent that orchestrates all sub-agents with proper callback configuration
- **`config.py`** - Contains AgentConfig class with retry policies and conditional execution callbacks
- **`custom_tools.py`** - Implements custom tools for the agents (API calls, external integrations)
- **`callback_config.py`** - Defines callback handlers for agent lifecycle events
- **`sub_agents/`** - Directory containing all specialized analysis agents

---

## Technologies

### Core Framework & AI

- **Google Gemini API** - Large Language Model for reasoning and analysis
- **Google ADK (Agent Development Kit)** - Multi-agent orchestration framework

### Data Processing & Storage

- **Python 3.10+** - Primary programming language
- **SQLite** - Lightweight embedded database (development)
