# Sentient Core: Hackathon Development Roadmap ('Raise Your Hack' MVP)
**Version:** 2.0 (Epic/Story Aligned)
**Date:** June 18, 2025
**Related Task Breakdown:** [../01_04_task_breakdown.md](README.md)

---

## Overall Timeline: 6 Sprints (1 week per sprint)

---

### Phase 1: Vultr Track & Foundational Platform (Sprints 1-2)
-   **Primary Epic:** EPIC-VULTR (Deploy & Showcase Core Sentient Platform on Vultr)
-   **Supporting Epics:** EPIC-CORE-PLATFORM, EPIC-UI
-   **Objective:** Deploy the core Sentient Core platform on Vultr, establish foundational backend/frontend services, and demonstrate an initial enterprise agentic workflow.
-   **Key Stories & Deliverables:**
    -   **STORY-VULTR-1:** Configure Vultr Production Environment.
        -   *Deliverable:* Secure Vultr instance, networking, DNS configured.
    -   **STORY-VULTR-2:** Dockerize Sentient Core Application Suite.
        -   *Deliverable:* Docker images for backend, frontend, and agent services.
    -   **STORY-CORE-PLATFORM-1:** Define Core API Endpoints & Data Models.
        -   *Deliverable:* OpenAPI spec for core services; Pydantic models.
    -   **STORY-CORE-PLATFORM-2:** Implement Core Agent Runtime Environment.
        -   *Deliverable:* Basic agent execution framework integrated with FastAPI.
    -   **STORY-UI-1:** Setup Next.js Project, TailwindCSS, Shadcn/UI, DaisyUI.
        -   *Deliverable:* Frontend project initialized with UI toolkit.
    -   **STORY-UI-2:** Implement Core UI Layout & Navigation.
        -   *Deliverable:* Main application shell, header, footer, navigation components.
    -   **STORY-VULTR-4 (Partial):** Develop "Enterprise Workflow Agent" (Initial Version).
        -   *Deliverable:* Basic version of the demo agent for Vultr, e.g., "Automated Market Research" agent using Groq/Llama 3, callable via API.
    -   **STORY-UI-3 (Partial):** Develop UI for Vultr "Enterprise Workflow Agent".
        -   *Deliverable:* Simple web interface to interact with the initial Vultr demo agent.

---

### Phase 2: Prosus Track & Platform Enhancement (Sprints 3-4)
-   **Primary Epic:** EPIC-PROSUS (Develop Agent-Powered E-commerce Pack)
-   **Supporting Epics:** EPIC-CORE-PLATFORM, EPIC-UI
-   **Objective:** Develop and integrate the agent-powered e-commerce solution, enhancing the platform with knowledge graph capabilities and voice UI.
-   **Key Stories & Deliverables:**
    -   **STORY-PROSUS-1:** Design & Implement User Knowledge Graph.
        -   *Deliverable:* Supabase schema and FastAPI service for KG management.
    -   **STORY-PROSUS-2:** Develop "Product Discovery Agent".
        -   *Deliverable:* Agent integrated with Tavily Search API, updates KG.
    -   **STORY-PROSUS-3:** Develop "Personal Shopper Agent".
        -   *Deliverable:* Agent providing personalized recommendations from KG.
    -   **STORY-PROSUS-4:** Implement Voice UI for E-commerce Interaction.
        -   *Deliverable:* Frontend with Web Speech API integration for STT/TTS.
    -   **STORY-PROSUS-5:** Build E-commerce Frontend Interface.
        -   *Deliverable:* UI for product display, search, recommendations, voice interaction.
    -   **STORY-CORE-PLATFORM-3:** Implement Agent-to-Agent Communication Layer (Fetch.ai/Coral).
        -   *Deliverable:* Adapters and handlers for Fetch.ai uAgents and Coral Protocol.
    -   **STORY-UI-4:** Develop UI for Core Platform Admin/Monitoring.
        -   *Deliverable:* Basic dashboard for observing agent activity or system health (if time permits).

---

### Phase 3: Qualcomm Track, CI/CD, & Final Polish (Sprints 5-6)
-   **Primary Epic:** EPIC-QUALCOMM (Develop On-Device Edge AI Utility Generator)
-   **Supporting Epics:** EPIC-CORE-PLATFORM, EPIC-UI
-   **Objective:** Implement the on-device AI utility, finalize CI/CD, complete all track demos, and prepare for final submission.
-   **Key Stories & Deliverables:**
    -   **STORY-QUALCOMM-1:** Research & Select On-Device AI Model.
        -   *Deliverable:* Chosen model and ONNX conversion strategy.
    -   **STORY-QUALCOMM-2:** Convert & Optimize Model for On-Device Inference.
        -   *Deliverable:* Quantized `.ort` model for QNN Execution Provider.
    -   **STORY-QUALCOMM-3:** Develop "Edge AI Utility" Application.
        -   *Deliverable:* Python application with ONNX Runtime, simple UI.
    -   **STORY-QUALCOMM-4:** Test & Benchmark Utility on Snapdragon Hardware (Simulated/Actual).
        -   *Deliverable:* Performance metrics and QNN EP validation.
    -   **STORY-VULTR-3:** Implement CI/CD Pipeline for Automated Vultr Deployments.
        -   *Deliverable:* GitHub Actions workflow for deploying to Vultr.
    -   **STORY-VULTR-5:** Implement Monitoring & Logging for Sentient Core on Vultr.
        -   *Deliverable:* Basic observability setup.
    -   **STORY-CORE-PLATFORM-4:** Implement Security Best Practices (API Auth, Data Sanitization).
        -   *Deliverable:* Security measures applied across the platform.
    -   **STORY-UI-5:** Finalize UI/UX Polish & Accessibility Review.
        -   *Deliverable:* Consistent and accessible UI across all features.
    -   **STORY-VULTR-6, STORY-PROSUS-6, STORY-QUALCOMM-5:** Prepare and Record Final Demo Scripts & Assets for all tracks.
        -   *Deliverable:* Comprehensive demo videos and presentation materials.
    -   **Overall:** Final integration, end-to-end testing, documentation polish, and submission package.
