# Prosus Track Action Plan: The Agentic Factory in Production

**Version:** 3.0 (Strategic Pivot)
**Date:** June 19, 2025
**Status:** Active
**Parent Epic:** EPIC-PROSUS-FACTORY (Build and Demonstrate the Sentient-Core Agentic Factory)

---

## 1. Objective

This document outlines the master plan for the RAISE Hackathon. Our primary objective is to win the **Prosus "Agentic Economy in Production" Track** by demonstrating **Sentient-Core** as a revolutionary **"agentic factory."** We will showcase a live, end-to-end process where a high-level command initiates an economy of specialized AI agents who collaborate to build, test, and prepare for deployment a high-value corporate application: the **"PharmaPulse" Competitive Intelligence Dashboard**.

## 2. Stories & Detailed Tasks

### STORY-PROSUS-1: Develop the Core Agentic Orchestrator (The Factory)
*   **Description:** Build the foundational hierarchical agent system that manages the entire workflow.
*   **Assigned:** AGENT-ARCHITECT
*   **Tasks:**
    *   **Task-1.1:** Implement the top-level 'C-Suite' planning agent using CrewAI to break down the initial prompt into a structured project plan.
    *   **Task-1.2:** Implement the mid-level 'Departmental' execution agents using LangGraph to manage the research, development, and data analysis workflows.
    *   **Task-1.3:** Define the state management and communication protocols between agent tiers.

### STORY-PROSUS-2: Develop the Specialized Agents (The Workers)
*   **Description:** Create the individual agents who will perform the core tasks of building the application.
*   **Assigned:** AGENT-BACKEND, AGENT-FRONTEND
*   **Tasks:**
    *   **Task-2.1:** Build the 'ResearchAgent' to use Tavily and Exa for gathering data on clinical trials and market sentiment.
    *   **Task-2.2:** Build the 'DataAgent' to process and structure the researched data using Pydantic models.
    *   **Task-2.3:** Build the 'BackendDeveloperAgent' to write FastAPI endpoints for the PharmaPulse dashboard.
    *   **Task-2.4:** Build the 'FrontendDeveloperAgent' to create the Next.js and DaisyUI components for the dashboard.
    *   **Task-2.5:** Integrate the 'sherpa-onnx' model for the voice command interface.
    *   **Task-2.6:** Integrate the 'Phi-3' model for the summarization and Q&A features of the final dashboard.

### STORY-PROSUS-3: Develop the Demo & Visualization Layer
*   **Description:** Create the user-facing components for the demo to make the factory's process clear and impressive.
*   **Assigned:** AGENT-FRONTEND, AGENT-STRATEGIC-EVANGELIST
*   **Tasks:**
    *   **Task-3.1:** Design a compelling UI to visualize the agent hierarchy and live task delegation.
    *   **Task-3.2:** Integrate a Stackblitz WebContainer to show the "PharmaPulse" application being built in real-time.
    *   **Task-3.3:** Develop the voice-command interface for initiating the build process.
    *   **Task-3.4:** Write the final demo script and storyboard.

## 3. Success Criteria

*   A single voice command successfully initiates the entire agentic factory workflow.
*   The agent economy successfully builds a functional, multi-component "PharmaPulse" dashboard.
*   The demo visualization clearly and effectively communicates the power and process of the Sentient-Core platform.
*   The final application is successfully handed off for deployment (as per the Vultr action plan).