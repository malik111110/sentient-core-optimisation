# Sentient Core – 'Raise Your Hack' Competition: Overall Strategy

**Version:** 1.0
**Date:** June 18, 2025
**Status:** Consolidated Draft

---

## 1. Overarching Vision: The Agentic Nexus

Our project, **Sentient Core**, will be positioned as a comprehensive **Enterprise Agentic Workflow Platform**. This directly aligns with the **Vultr Track**, aiming to empower businesses and developers to rapidly design, build, deploy, and manage sophisticated AI agents and multi-agent systems. Our core platform, built with Python and leveraging the Archon framework, is designed for modularity and extensibility.

For the "Raise Your Hack" competition, Sentient Core will showcase its capabilities by addressing three sponsor tracks (Vultr, Prosus, Qualcomm) and integrating key technologies from Meta (via Groq), Groq, Fetch.ai, and Coral Protocol.

## 2. Core Platform & Technology Foundation

To meet the hackathon's foundational requirements and leverage powerful new technologies, Sentient Core's architecture is built upon the following:

### 2.1. Frontend: Next.js 15
*   **Rationale:** Next.js 15, with React 19, provides a robust framework for a modern, responsive, and performant UI. Server-centric features like Server Actions and Turbopack enable rapid development.
*   **Key Components:** React 19, Shadcn/UI, Tailwind CSS.

### 2.2. Backend: FastAPI
*   **Rationale:** FastAPI offers high performance, native async support, and automatic OpenAPI documentation, crucial for orchestrating complex, I/O-bound multi-agent workflows.
*   **Key Components:** Python 3.12, Pydantic.

### 2.3. Database: Supabase (PostgreSQL)
*   **Rationale:** Supabase provides a scalable PostgreSQL database with BaaS features (authentication, real-time), allowing focus on core application logic.

### 2.4. LLM Provider: Groq API with Llama 3
*   **Rationale:** The Groq API serving Llama 3 is key for its low latency and high throughput, essential for real-time reasoning and code generation in agentic workflows.

### 2.5. Agent Framework: Fetch.ai uAgents
*   **Rationale:** Fetch.ai uAgents will be used for agent registration, discovery, and decentralized communication, enhancing interoperability.

### 2.6. Inter-Agent Communication: Coral Protocol
*   **Rationale:** Coral Protocol provides a robust, thread-style communication layer for complex, stateful interactions and reliable message passing between agents.

### 2.7. Containerization: Docker
*   **Rationale:** Docker ensures consistent and reproducible deployment environments for our FastAPI backend and Next.js frontend on Vultr.

## 3. Track-Specific Strategies & Deliverables

### 3.1. Vultr Track: Enterprise Agentic Workflow Platform

*   **Deliverable:** The Sentient Core platform itself, deployed on **Vultr infrastructure**.
*   **Functionality:**
    *   A user-friendly interface (Next.js 15) for designing agentic workflows.
    *   A robust backend (FastAPI) to manage agent lifecycles, communication (Coral Protocol), and task execution.
    *   Integration with Groq/Llama 3 for advanced AI reasoning and task processing.
    *   Support for Fetch.ai uAgents for broader agent ecosystem participation.
*   **Addressing Constraints:** Demonstrates a scalable, enterprise-grade application on Vultr, leveraging its high-performance VMs.

### 3.2. Prosus Track: AI-Powered E-commerce Agent Pack

*   **Deliverable:** An **E-commerce Agent Pack** module within Sentient Core, designed to enhance online retail experiences.
*   **Functionality:**
    *   **Knowledge-Graph User Profiles:** Agents build dynamic user profiles based on browsing history, purchase data, and explicit preferences, stored and managed via Supabase.
    *   **Personalized Recommendation Agent:** Leverages user profiles and Llama 3 to provide highly relevant product recommendations.
    *   **Voice UI Interaction Agent:** Enables voice-based shopping and customer service interactions, using advanced speech-to-text and text-to-speech services integrated with Llama 3 for natural language understanding.
    *   **Tavily Search Integration Agent:** Provides intelligent product search and comparison capabilities by interfacing with the Tavily Search API for broader market insights.
*   **Addressing Constraints:** Showcases AI-driven e-commerce solutions, focusing on personalization and innovative user interaction.

### 3.3. Qualcomm Track: On-Device Edge AI Utility Generator

*   **Deliverable:** An innovative **Edge AI Utility Generator** module within the Sentient Core platform.
*   **Functionality:**
    *   Users define high-level requirements for simple utility apps (e.g., "offline photo sorter," "local document summarizer").
    *   Sentient Core, using Groq/Llama 3, automatically generates Python code for these utilities.
    *   Generated applications are packaged for deployment on **Snapdragon X Elite** devices.
*   **On-Device AI & Technology:**
    *   **Inference Runtime:** ONNX Runtime for executing AI models on-device.
    *   **Execution Provider:** Qualcomm QNN Execution Provider for Snapdragon optimization.
    *   **Offline Core Functionality:** The AI component of the generated utility (e.g., image categorization via a pre-trained ONNX model) runs **entirely on-device and offline**. Groq/Llama 3 is used only during the *generation phase* on the Sentient Core cloud platform.
*   **Addressing Constraints:** Delivers useful, offline-first AI applications for Qualcomm hardware, with development aided by cloud AI.

## 4. Unified Value Proposition

This integrated strategy showcases Sentient Core as a versatile platform. It meets Vultr's enterprise demands, spawns specialized e-commerce solutions for Prosus, and generates innovative on-device applications for Qualcomm. All functionalities are amplified by Meta/Groq's Llama 3, Fetch.ai's agent ecosystem, and Coral Protocol's collaboration infrastructure, presenting a forward-looking vision for agentic AI.