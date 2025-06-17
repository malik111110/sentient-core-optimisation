# Sentient Core - Technology Strategy

**Version:** 1.0
**Date:** June 18, 2025
**Status:** Initial Draft

---

## 1. Introduction

This document outlines the comprehensive technology strategy for the Sentient Core platform, specifically tailored to meet the objectives of the 'Raise Your Hack' competition. Our strategy is built on a foundation of modern, high-performance, and scalable technologies, chosen to effectively address the challenges of the Vultr, Prosus, and Qualcomm sponsor tracks.

## 2. Core Platform Technologies

### 2.1 Frontend: Next.js 15

*   **Rationale:** Next.js 15, with its underlying React 19 architecture, provides a robust framework for building a modern, responsive, and performant user interface. Its server-centric approach, combined with features like Server Actions and Turbopack, allows for rapid development and a seamless user experience.
*   **Key Components:** React 19, Shadcn/UI, Tailwind CSS.

### 2.2 Backend: FastAPI

*   **Rationale:** FastAPI is our choice for the backend due to its high performance, native asynchronous support, and automatic OpenAPI documentation generation. Its async capabilities are critical for orchestrating the complex, I/O-bound workflows of our multi-agent system.
*   **Key Components:** Python 3.12, Pydantic.

### 2.3 Database: Supabase (PostgreSQL)

*   **Rationale:** Supabase provides a powerful, scalable, and easy-to-use PostgreSQL database with a suite of backend-as-a-service features, including authentication and real-time capabilities. This allows us to focus on our core application logic while leveraging a robust and managed database solution.

## 3. AI & Agentic Technologies

### 3.1 LLM Provider: Groq API with Llama 3

*   **Rationale:** The Groq API, serving the Llama 3 model, is the cornerstone of our AI capabilities. Its incredibly low latency and high throughput are essential for providing the real-time reasoning and code generation required by our agentic workflows.

### 3.2 Agent Framework: Fetch.ai uAgents

*   **Rationale:** Fetch.ai's `uAgents` provide a decentralized framework for creating, registering, and discovering autonomous agents. This aligns perfectly with our vision of a modular, extensible multi-agent system and is a key requirement for the Vultr track.

### 3.3 Inter-Agent Communication: Coral Protocol

*   **Rationale:** Coral Protocol provides a robust, thread-style communication layer for our agents. This enables complex, stateful interactions and ensures reliable message passing, which is crucial for orchestrating sophisticated development tasks.

## 4. On-Device AI (Qualcomm Track)

### 4.1 Inference Runtime: ONNX Runtime

*   **Rationale:** For the Qualcomm track, we will leverage ONNX Runtime to execute AI models directly on-device. Its cross-platform compatibility and support for hardware acceleration make it the ideal choice for creating efficient, offline-first AI utilities.

### 4.2 Execution Provider: Qualcomm QNN Execution Provider

*   **Rationale:** By using the Qualcomm QNN Execution Provider, we can ensure that our on-device models are optimized for Snapdragon hardware, taking full advantage of the dedicated AI processing units for maximum performance and efficiency.

## 5. Deployment & Infrastructure (Vultr Track)

### 5.1 Cloud Provider: Vultr

*   **Rationale:** As a primary sponsor of the hackathon, Vultr provides the high-performance cloud infrastructure required to deploy and demonstrate the Sentient Core platform. We will leverage their virtual machines to host our FastAPI backend and Next.js frontend.

### 5.2 Containerization: Docker

*   **Rationale:** Docker will be used to containerize our application components, ensuring a consistent and reproducible deployment environment. This simplifies the deployment process and allows for easy scaling and management of our services on the Vultr platform.

## 6. Conclusion

Our technology stack is a carefully curated selection of best-in-class tools and frameworks, each chosen for its specific strengths and its ability to contribute to our overall vision. By combining the power of Next.js, FastAPI, Groq, Fetch.ai, Coral, and ONNX Runtime, we are confident in our ability to deliver a groundbreaking platform that meets and exceeds the expectations of the 'Raise Your Hack' competition.
