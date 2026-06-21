# 🌿 SafeSpace: An AI Agent Built to Listen, Not Advise
**Track:** Concierge Agents

## 📖 The Problem
In a world full of AI assistants rushing to give advice, people experiencing overwhelming life pressures often just want to be heard. Unprompted advice can feel dismissive. SafeSpace solves this by being an AI built explicitly to listen, validate, and track emotional patterns without ever offering solutions.

## 🏗️ Architecture & Key Concepts Used
This project implements a secure, Multi-Agent workflow using the following core course concepts:

1. **Security Features (Privacy Scrubbing):** User input passes through a security regex layer to redact sensitive data (like account numbers) before reaching the LLMs. 
2. **Multi-Agent System (ADK):** The workload is split between two distinct entities:
   * **Agent 1 (The Front-End Listener):** A strictly prompted Gemini agent that mirrors emotional pacing without giving advice. 
   * **Agent 2 (The Back-End Analyst):** A silent background agent that analyzes the text to determine the core emotional vector and topic cluster. 
3. **MCP Server & Agent Skills:** Agent 2 autonomously triggers the `SafeSpaceMCPServer` mapping to silently append trends to a local `journal.txt` file.

### Architecture Flowchart
```mermaid
graph TD
    A[User] -->|Types Message| B(Streamlit Web UI)
    B --> C{🛡️ Security Privacy Scrub}
    C -->|Clean Text| D[Agent 1: Front-End Listener]
    C -->|Clean Text| E[Agent 2: Back-End Analyst]
    D -->|Empathetic Reply| B
    E -->|Emotion & Topic| F((MCP Server Tool))
    F -->|Silently Logs Trend| G[(journal.txt)]
