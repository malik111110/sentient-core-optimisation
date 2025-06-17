# Project Roadmap: Sentient Core

**Document Version:** 1.0 (Initial Draft including Hackathon Adaptation)
**Date:** June 17, 2025

## 1. Overall Project Vision

Sentient Core is an advanced AI-driven development platform designed to transform natural language requirements into production-ready applications via intelligent multi-agent orchestration. The immediate focus of this roadmap is the 'Raise Your Hack' competition, which will serve as the launchpad for delivering the initial, tangible version of Sentient Core, showcasing its core capabilities and innovative potential by addressing specific sponsor challenges.

## 2. Original Project Phases (Conceptual Timeline)

*This is an estimated timeline for the broader project vision. The 'Raise Your Hack' competition deliverables will form the foundational MVP, which these subsequent phases will build upon and extend.*

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
*   **Goal:** Establish core platform infrastructure (Sentient Core) and integrate foundational hackathon technologies (Groq, Fetch.ai, Coral Protocol).
*   **Key Deliverables & Technologies:**
    *   **Platform Core:** Initial setup of Next.js 15 (React 19, Tailwind CSS v4, Shadcn/UI) frontend and FastAPI (Python) backend for Sentient Core.
    *   **Core Agent Tech:** Implement initial versions of backend clients for **Groq API (Llama 3)**, **Fetch.ai `uAgents`**, and **Coral Protocol** within `src/clients`.
    *   **Vultr Track:** Initial Vultr account setup; plan for deployment of the Sentient Core platform.
    *   **Prosus Track:** Design e-commerce agent pack architecture; define knowledge graph schema for user/product profiles; plan Tavily API integration.
    *   **Qualcomm Track:** Research on-device AI libraries (ONNX Runtime) and application packaging for Snapdragon X Elite; plan Edge AI Utility Generator module.

### Week 2: Core Feature Implementation (Track-Specific)
*   **Goal:** Develop core functionalities for each hackathon track, leveraging the integrated foundational technologies.
*   **Vultr Track (Enterprise Agentic Workflow Platform):**
    *   Implement core agentic workflow orchestration logic within Sentient Core, utilizing **Groq (Llama 3)** for intelligence, **Fetch.ai `uAgents`** for agent management, and **Coral Protocol** for inter-agent communication.
    *   Develop basic UI elements for defining and monitoring these workflows.
*   **Prosus Track (Agent-Powered E-commerce):**
    *   Develop `ECommerceAgentService` incorporating knowledge graph capabilities for user/product profiles.
    *   Integrate **Tavily API** for enhanced e-commerce search.
    *   Implement initial voice UI capabilities using the core LLM.
*   **Qualcomm Track (On-Device Edge AI Utility Generator):**
    *   Develop the `EdgeUtilityGeneratorService` within Sentient Core, using **Groq (Llama 3)** to generate Python code for utilities.
    *   Implement UI for users to specify utility requirements.
    *   Generate, package, and test a first simple on-device utility (e.g., offline image sorter or text summarizer) for Snapdragon X Elite, ensuring core AI runs offline.

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