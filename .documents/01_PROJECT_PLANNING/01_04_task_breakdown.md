# Sentient Core - Task Breakdown

**Version:** 2.0 (Hierarchical Epic/Story Alignment)
**Date:** June 18, 2025
**Status:** In Progress

---

## Introduction

This document outlines the Epics and Stories for the Sentient Core project, including deliverables for the "Raise Your Hack" hackathon. It serves as a central index, linking to detailed action plans where appropriate.

### Task Organization Framework
- **Epic**: Large feature or capability (spans multiple sprints)
- **Story**: User-facing functionality (1-2 sprints)
- **Task**: Technical implementation work (1-5 days)
- **Subtask**: Granular development work (< 1 day)

### Agent Assignment (Illustrative)
- AGENT-ARCHITECT, AGENT-DEVOPS, AGENT-BACKEND, AGENT-FRONTEND, AGENT-KNOWLEDGE-SYNTHESIS, AGENT-STRATEGIC-EVANGELIST, etc.

---

## EPIC-VULTR: Deploy & Showcase Core Sentient Platform on Vultr
*Goal: Demonstrate Sentient Core as a robust, scalable enterprise-grade platform for developing and deploying agentic workflows, hosted on Vultr.*
*See detailed track plan: [Vultr Track Action Plan](../02_HACKATHON_CENTRAL/02_05_ACTION_PLANS_BY_TRACK/02_05_01_vultr_track_action_plan.md)*

-   **STORY-VULTR-1:** Configure Vultr Production Environment
    -   Description: Networking, Security, VM Sizing for Vultr deployment.
    -   Assigned: AGENT-DEVOPS
    -   Status: To Do
    -   Detailed Tasks: See linked Vultr Track Action Plan.
-   **STORY-VULTR-2:** Dockerize Sentient Core Application Suite
    -   Description: Containerize Frontend, Backend API, Agent Services.
    -   Assigned: AGENT-DEVOPS / AGENT-BACKEND
    -   Status: To Do
    -   Detailed Tasks: See linked Vultr Track Action Plan.
-   **STORY-VULTR-3:** Implement CI/CD Pipeline for Automated Vultr Deployments
    -   Description: GitHub Actions to Vultr.
    -   Assigned: AGENT-DEVOPS
    -   Status: To Do
    -   Detailed Tasks: See linked Vultr Track Action Plan.
-   **STORY-VULTR-4:** Develop "Enterprise Workflow Agent"
    -   Description: Demo agent for Vultr track (e.g., marketing content generation or sales lead qualification agent).
    -   Assigned: AGENT-ARCHITECT / AGENT-BACKEND
    -   Status: To Do
    -   Detailed Tasks: See linked Vultr Track Action Plan.
-   **STORY-VULTR-5:** Implement Monitoring & Logging for Sentient Core on Vultr
    -   Description: Setup observability for the platform on Vultr.
    -   Assigned: AGENT-DEVOPS
    -   Status: To Do
    -   Detailed Tasks: See linked Vultr Track Action Plan.
-   **STORY-VULTR-6:** Prepare Vultr Track Demo Script & Assets
    -   Description: Finalize demo flow and materials for Vultr presentation.
    -   Assigned: AGENT-STRATEGIC-EVANGELIST
    -   Status: To Do
    -   Detailed Tasks: See linked Vultr Track Action Plan.

## EPIC-PROSUS: Develop Agent-Powered E-Commerce Pack
*Goal: Showcase Sentient Core's ability to generate and manage sophisticated, personalized e-commerce experiences using AI agents.*
*See detailed track plan: [Prosus Track Action Plan](../02_HACKATHON_CENTRAL/02_05_ACTION_PLANS_BY_TRACK/02_05_02_prosus_track_action_plan.md)*

-   **STORY-PROSUS-1:** Design & Implement User Profile Knowledge Graph Service
    -   Description: Supabase backend, GraphQL/FastAPI endpoint for user profiles.
    -   Assigned: AGENT-BACKEND
    -   Status: To Do
    -   Detailed Tasks: See linked Prosus Track Action Plan.
-   **STORY-PROSUS-2:** Develop "Personal Shopper Agent"
    -   Description: Integrates with product catalog, user profile KG, and recommendation logic.
    -   Assigned: AGENT-BACKEND / AGENT-ARCHITECT
    -   Status: To Do
    -   Detailed Tasks: See linked Prosus Track Action Plan.
-   **STORY-PROSUS-3:** Develop "Product Research & Discovery Agent"
    -   Description: Integrates Tavily API for external product/trend research.
    -   Assigned: AGENT-BACKEND / AGENT-KNOWLEDGE-SYNTHESIS
    -   Status: To Do
    -   Detailed Tasks: See linked Prosus Track Action Plan.
-   **STORY-PROSUS-4:** Implement Voice-First UI for E-commerce Interactions
    -   Description: Using Web Speech API or chosen library, feeding into agent communication.
    -   Assigned: AGENT-FRONTEND
    -   Status: To Do
    -   Detailed Tasks: See linked Prosus Track Action Plan.
-   **STORY-PROSUS-5:** Build E-commerce UI Components for Prosus Demo
    -   Description: Next.js frontend for the mock storefront (Artisanal Coffee use case).
    -   Assigned: AGENT-FRONTEND
    -   Status: To Do
    -   Detailed Tasks: See linked Prosus Track Action Plan.
-   **STORY-PROSUS-6:** Integrate E-commerce Agents with Core Sentient Platform
    -   Description: Messaging, state management.
    -   Assigned: AGENT-BACKEND / AGENT-ARCHITECT
    -   Status: To Do
    -   Detailed Tasks: See linked Prosus Track Action Plan.
-   **STORY-PROSUS-7:** Prepare Prosus Track Demo Script & Assets
    -   Description: Focus on the "Artisanal Coffee" use case.
    -   Assigned: AGENT-STRATEGIC-EVANGELIST
    -   Status: To Do
    -   Detailed Tasks: See linked Prosus Track Action Plan.

## EPIC-QUALCOMM: Develop Edge AI Utility Generator & Demo Utility
*Goal: Demonstrate Sentient Core's capability to generate and deploy functional AI utilities for on-device execution, targeting Snapdragon X Elite.*
*See detailed track plan: [Qualcomm Track Action Plan](../02_HACKATHON_CENTRAL/02_05_ACTION_PLANS_BY_TRACK/02_05_03_qualcomm_track_action_plan.md)*

-   **STORY-QUALCOMM-1:** Design "Edge Utility Specification Interface" within Sentient Core
    -   Description: UI for defining utility requirements (model type, inputs, outputs, target device features).
    -   Assigned: AGENT-FRONTEND / AGENT-ARCHITECT
    -   Status: To Do
    -   Detailed Tasks: See linked Qualcomm Track Action Plan (also linked to STORY-UI-5).
-   **STORY-QUALCOMM-2:** Implement Python Code Generation Engine for Basic Edge Utilities
    -   Description: Scaffolding, input/output handling, ONNX model loading boilerplate.
    -   Assigned: AGENT-BACKEND
    -   Status: To Do
    -   Detailed Tasks: See linked Qualcomm Track Action Plan.
-   **STORY-QUALCOMM-3:** Integrate ONNX Model Conversion & Packaging Workflow
    -   Description: Python script using `tf2onnx`/`onnx` tools, quantization options.
    -   Assigned: AGENT-BACKEND / AGENT-KNOWLEDGE-SYNTHESIS
    -   Status: To Do
    -   Detailed Tasks: See linked Qualcomm Track Action Plan.
-   **STORY-QUALCOMM-4:** Implement QNN Execution Provider Configuration for Generated Utilities
    -   Description: Ensure generated code can leverage QNN EP on Snapdragon.
    -   Assigned: AGENT-BACKEND
    -   Status: To Do
    -   Detailed Tasks: See linked Qualcomm Track Action Plan.
-   **STORY-QUALCOMM-5:** Develop "Coffee Aroma Analyzer" Demo Utility
    -   Description: Python, ONNX model, simple UI for device.
    -   Assigned: AGENT-BACKEND / AGENT-FRONTEND
    -   Status: To Do
    -   Detailed Tasks: See linked Qualcomm Track Action Plan.
-   **STORY-QUALCOMM-6:** Prepare Qualcomm Track Demo Script & Assets
    -   Description: Showing generation and on-device execution.
    -   Assigned: AGENT-STRATEGIC-EVANGELIST
    -   Status: To Do
    -   Detailed Tasks: See linked Qualcomm Track Action Plan.

## EPIC-CORE-PLATFORM: Foundational Sentient Core Enhancements
*Goal: Improve the underlying agentic engine of Sentient Core to support the hackathon deliverables and future scalability.*

-   **STORY-CORE-1:** Enhance Intent Parsing & Workflow Generation Engine
    -   Description: Utilize Llama 3 via Groq API for more nuanced understanding of user intent and dynamic workflow generation.
    -   Assigned: AGENT-BACKEND / AGENT-ARCHITECT
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-Core-1.1: Design prompt strategies for Llama 3 for intent classification and workflow mapping.
        -   Task-Core-1.2: Integrate Groq API client (`src/clients/groq_client.py`) into the core intent processing pipeline.
        -   Task-Core-1.3: Develop logic to translate Llama 3 output into actionable workflow steps for LangGraph.
        -   Task-Core-1.4: Implement error handling and fallback mechanisms for intent parsing.
        -   Task-Core-1.5: Unit test intent parsing with various complex user requests.
        -   References: `02_06_01_groq_api_guide.md`, `02_06_02_llama3_model_guide.md`
-   **STORY-CORE-2:** Implement Coral Protocol for Inter-Agent Communication & Discovery
    -   Description: Initial integration of Coral Protocol for selected agents to enhance decentralized communication and discovery.
    -   Assigned: AGENT-BACKEND / AGENT-ARCHITECT
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-Core-2.1: Setup local Coral Server instance for development.
        -   Task-Core-2.2: "Coralize" two key agents (e.g., Personal Shopper Agent and Product Research Agent) by implementing `CoralAgent` interface.
        -   Task-Core-2.3: Define DIDs and capabilities for these agents.
        -   Task-Core-2.4: Implement message handling via Coral Threads for a specific interaction between the two agents.
        -   Task-Core-2.5: Test agent discovery and communication through Coral Server.
        -   References: `02_06_04_coral_protocol_guide.md`, `src/clients/coral_message_handler.py`
-   **STORY-CORE-3:** Integrate Fetch.ai uAgent Concepts for Specialized Tasks
    -   Description: Utilize Fetch.ai uAgent patterns for agents requiring autonomous operation or specific protocol interactions (e.g., Product Research Agent).
    -   Assigned: AGENT-BACKEND / AGENT-KNOWLEDGE-SYNTHESIS
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-Core-3.1: Define a Fetch.ai uAgent `Model` for requests/responses for the Product Research Agent.
        -   Task-Core-3.2: Implement the Product Research Agent using the `Agent` class from `uagents`.
        -   Task-Core-3.3: Utilize `ctx.send()` or `ctx.ask()` for communication with other services (e.g., Tavily client).
        -   Task-Core-3.4: Register and run the agent within a local `Bureau` for testing.
        -   Task-Core-3.5: Explore Agentverse registration for the agent (optional for hackathon).
        -   References: `02_06_03_fetchai_uagent_guide.md`, `src/clients/fetchai_adapter.py`
-   **STORY-CORE-4:** Refine `BaseAgent` Class and Tooling Abstractions
    -   Description: Enhance the core `BaseAgent` class for better state management, tool usage, and error handling.
    -   Assigned: AGENT-ARCHITECT / AGENT-BACKEND
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-Core-4.1: Review existing `BaseAgent` (if any) or define a new one based on LangGraph principles.
        -   Task-Core-4.2: Standardize tool definition and registration mechanism for agents.
        -   Task-Core-4.3: Improve error propagation and retry logic within agent workflows.
        -   Task-Core-4.4: Ensure compatibility with chosen LLM observability solution.
        -   References: `03_01_multi_agent_architecture.md`
-   **STORY-CORE-5:** Improve Centralized Logging & Observability for Agent Interactions
    -   Description: Implement structured logging and integrate with an observability tool/pattern for tracing agent interactions.
    -   Assigned: AGENT-DEVOPS / AGENT-BACKEND
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-Core-5.1: Define a structured log format for all agent events and LLM calls.
        -   Task-Core-5.2: Ensure all agents and services adhere to this logging format.
        -   Task-Core-5.3: Evaluate and select a lightweight observability approach for the hackathon (e.g., Langfuse, Helicone, or custom logging to Supabase).
        -   Task-Core-5.4: Implement basic tracing for a multi-step agent workflow.
        -   References: `03_05_llm_observability_management.md`

## EPIC-UI: Sentient Core Main Dashboard & "Wow" Demo UI
*Goal: Create a compelling user interface for Sentient Core and the integrated "Wow" demo flow, ensuring a cohesive and professional presentation.*

-   **STORY-UI-1:** Design & Implement Main Sentient Core Dashboard
    -   Description: Develop the primary interface for users to interact with Sentient Core, input intents, and view project statuses.
    -   Assigned: AGENT-FRONTEND
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-UI-1.1: Wireframe key dashboard views (Project Overview, Intent Input, Agent Configuration, Deployment Status).
        -   Task-UI-1.2: Setup Next.js 15 project with Tailwind CSS, Shadcn/UI, and DaisyUI.
        -   Task-UI-1.3: Implement responsive layout and navigation.
        -   Task-UI-1.4: Develop core components (e.g., project cards, intent input form, status indicators).
        -   Task-UI-1.5: Integrate with backend API for displaying dynamic data.
        -   References: `02_06_07_nextjs_15_guide.md`, Branding Guidelines.
-   **STORY-UI-2:** Develop UI for Intent Input & Project Initialization (Vultr Scene 1)
    -   Description: Create the specific UI elements for the first scene of the "Wow" demo.
    -   Assigned: AGENT-FRONTEND
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-UI-2.1: Design a clear and intuitive text area for high-level intent input.
        -   Task-UI-2.2: Implement frontend logic to send intent to backend.
        -   Task-UI-2.3: Display feedback/confirmation of project initialization.
-   **STORY-UI-3:** Create Mock E-commerce Storefront UI (Prosus Scene 2)
    -   Description: Build the visual elements for the "Artisanal Coffee" e-commerce demo.
    -   Assigned: AGENT-FRONTEND
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-UI-3.1: Design product display, cart, and voice input elements.
        -   Task-UI-3.2: Implement UI to interact with e-commerce agents (displaying recommendations, order status).
        -   Task-UI-3.3: Integrate Web Speech API for voice input.
-   **STORY-UI-4:** Develop Simple UI for "Coffee Aroma Analyzer" (Qualcomm Scene 3)
    -   Description: Create the interface for the on-device demo utility.
    -   Assigned: AGENT-FRONTEND (or Python GUI if simpler for on-device)
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-UI-4.1: Design a minimal UI: "scan" button, image display area, text output for tasting notes.
        -   Task-UI-4.2: Implement using appropriate tech (could be a simple web view if Python utility runs a local server, or a native-like Python GUI e.g. Kivy/PyQt if time allows and fits edge constraints).
-   **STORY-UI-5:** Implement UI for "Edge Utility Specification" (linked to STORY-QUALCOMM-1)
    -   Description: Frontend for users to define requirements for new edge utilities within Sentient Core.
    -   Assigned: AGENT-FRONTEND
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-UI-5.1: Design form elements for specifying utility name, function, model type, input/output parameters.
        -   Task-UI-5.2: Integrate with backend to submit these specifications.
-   **STORY-UI-6:** Ensure Consistent Branding & Theming (Light/Dark) Across All UIs
    -   Description: Apply Sentient Core branding, typography, color schemes consistently. Implement light and dark themes.
    -   Assigned: AGENT-FRONTEND
    -   Status: To Do
    -   Detailed Tasks:
        -   Task-UI-6.1: Finalize color palette and typography based on `BRANDING_GUIDELINES.md`.
        -   Task-UI-6.2: Implement theme switching mechanism (e.g., using Tailwind dark mode utility or DaisyUI theme controller).
        -   Task-UI-6.3: Audit all UI components for consistency.

---
This structure provides a comprehensive overview and allows for detailed task management within each story.
