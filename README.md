# 🌿 SafeSpace: An AI Agent Built to Listen, Not Advise
**Track:** Concierge Agents

## 📖 The Problem
In a world full of AI assistants rushing to give advice, people experiencing overwhelming life pressures often just want to be heard. Unprompted advice can feel dismissive. SafeSpace solves this by being an AI built explicitly to listen, validate, and track emotional patterns without ever offering solutions.

## 🏗️ Architecture & Key Concepts Used
This project implements a secure, Multi-Agent workflow:
1. **Security Privacy Scrub:** User input passes through a security layer to redact sensitive data before reaching the LLMs. 
2. **Agent 1 (The Front-End Listener):** A strictly prompted Gemini agent that mirrors emotional pacing without giving advice. 
3. **Agent 2 (The Back-End Analyst):** A silent background agent that analyzes the text to determine the core emotional vector. 
4. **MCP Server & Agent Skills:** Agent 2 uses `SafeSpaceMCPServer` to silently append trends to a local `journal.txt` file.
