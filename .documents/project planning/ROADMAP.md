# Project Roadmap: Sentient Core

**Document Version:** 1.0 (Initial Draft including Hackathon Adaptation)
**Date:** June 17, 2025

## 1. Overall Project Vision

Sentient Core aims to be an advanced AI-driven development platform that transforms natural language requirements into production-ready applications through intelligent multi-agent orchestration. This roadmap outlines the planned development phases, including a focused sprint for the 'Raise Your Hack' competition.

## 2. Original Project Phases (Conceptual Timeline)

*This is an estimated timeline for the broader project vision, which will run in parallel and extend beyond the hackathon sprint.*

*   **Phase 1: Foundation & Core Intelligence (Estimated Weeks 1-4 of project start)**
    *   Multi-Agent Infrastructure Setup (AutoGen/AG2, LangGraph).
    *   Core Agent Development Environment.
    *   Initial LLM Integration (Pre-Groq).
    *   Semantic Memory System (ChromaDB).
*   **Phase 2: Core Feature Development (Estimated Weeks 5-8)**
    *   Requirements Intelligence Agent.
    *   Architecture Planning Agent.
    *   Basic Frontend & Backend Code Generation Agents.
    *   Initial Database Design Agent.
*   **Phase 3: Advanced Features & MVP Polish (Estimated Weeks 9-12)**
    *   Advanced Code Generation Capabilities (error handling, patterns).
    *   Automated QA & Testing Agent Integration.
    *   Basic Deployment Automation (Pre-Vultr specific).
    *   User Interface for project definition and monitoring.
*   **Post-MVP: Continuous Enhancement**
    *   Expanded framework/language support.
    *   Advanced security features.
    *   Enterprise integrations.
    *   Community features & model fine-tuning.

## 3. 'Raise Your Hack' Competition Sprint (Focused Timeline: Next ~3-4 Weeks)

*This sprint focuses on delivering the requirements for the Vultr, Prosus, and Qualcomm tracks, integrating specified sponsor technologies.*

### Week 1: Hackathon Preparation & Foundational Tech Integration
*   **Goal:** Establish core technology integrations and begin track-specific foundational work.
*   **Core Tech (Parallel):**
    *   **Groq API & Llama 3:** Implement `GroqService`, test basic LLM calls (T8.1.1.1, T8.1.1.3).
    *   **Fetch.ai:** Initial research and `FetchAIAdapter` stub (T8.1.2.1, part of T8.1.2.2).
    *   **Coral Protocol:** Initial research and `CoralMessageHandler` stub (T8.1.3.1, part of T8.1.3.2).
*   **Vultr Track:**
    *   Dockerize backend and frontend applications (T8.2.1.1, T8.2.1.2).
    *   Initial Vultr account setup and familiarization.
*   **Prosus Track:**
    *   Design Knowledge Graph schema for user profiles (T8.3.1.1).
    *   Stub `KnowledgeGraphService` and `TavilyService` (part of T8.3.1.2, T8.3.2.1).
*   **Qualcomm Track:**
    *   Research on-device inference libraries (ONNX Runtime) and Python app packaging (T8.4.1.4, T8.4.1.5).
    *   Design Edge Utility Generator module architecture (T8.4.1.1).

### Week 2: Hackathon Build Sprint - MVP Development
*   **Goal:** Develop Minimum Viable Product (MVP) functionality for all three tracks.
*   **Core Tech (Parallel):**
    *   **Groq API & Llama 3:** Full integration into agent workflows (T8.1.1.2).
    *   **Fetch.ai:** Complete `FetchAIAdapter` and test agent registration/discovery (T8.1.2.2, T8.1.2.3, T8.1.2.4).
    *   **Coral Protocol:** Complete `CoralMessageHandler` and test basic collaborative task (T8.1.3.2, T8.1.3.3, T8.1.3.4).
*   **Vultr Track:**
    *   Deploy Snoob-Dev to Vultr (T8.2.1.3, T8.2.1.5).
    *   Develop MVP of Enterprise Agent Demo (e.g., Market Research Agent) (T8.2.2.1, T8.2.2.2, T8.2.2.3).
*   **Prosus Track:**
    *   Implement `KnowledgeGraphService` and `TavilyService` (T8.3.1.2, T8.3.1.3, T8.3.2.1, T8.3.2.2).
    *   Develop MVP of E-commerce Agent (T8.3.3.1, T8.3.3.2, T8.3.3.3).
*   **Qualcomm Track:**
    *   Implement `EdgeUtilityGeneratorService` and UI for requirements (T8.4.1.2, T8.4.1.3).
    *   Generate and test first on-device utility (T8.4.2.1, T8.4.2.2, T8.4.2.3).

### Week 3: Hackathon Refinement, Testing & Demo Preparation
*   **Goal:** Stabilize features, conduct thorough testing, and prepare all demonstration materials.
*   **All Tracks:**
    *   Intensive testing and bug fixing for all implemented features.
    *   Refine UI/UX for demonstrated workflows.
    *   Develop clear demonstration scripts for each track.
    *   Prepare pitch deck slides outlining the solution for each track and the overall platform.
*   **Vultr Track:**
    *   Finalize CI/CD pipeline for Vultr (T8.2.1.4).
    *   Stress test Vultr deployment if feasible.
*   **Qualcomm Track:**
    *   Finalize packaging and setup instructions for the generated utility (T8.4.2.4).

### Week 4 (Optional, if timeline permits): Submission & Polish
*   **Goal:** Final polish, submission, and internal review.
*   **All Tracks:**
    *   Final review of all deliverables against hackathon requirements.
    *   Submit project.
    *   (Internal) Conduct a post-hackathon review: lessons learned, potential for future development.

## 4. Dependencies and Risks

*   **Hardware Access (Qualcomm):** Timely receipt and setup of Snapdragon X Elite loaner device is critical. Mitigation: Develop with robust simulation and emulation where possible.
*   **API Stability/Access:** Reliance on external APIs (Groq, Fetch.ai, Coral, Tavily). Mitigation: Stub services early, handle API errors gracefully.
*   **Learning Curve:** New technologies (Fetch.ai, Coral Protocol, Groq specifics, Qualcomm SDKs) require rapid learning. Mitigation: Focused research tasks, pair programming.
*   **Integration Complexity:** Integrating multiple new systems simultaneously. Mitigation: Incremental integration, frequent testing, clear interface definitions.

This roadmap will be a living document and reviewed weekly or as major milestones are reached/adjusted.