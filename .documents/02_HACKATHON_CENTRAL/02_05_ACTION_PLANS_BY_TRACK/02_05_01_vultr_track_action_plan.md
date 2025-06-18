# Vultr Track Action Plan: Enterprise Agentic Workflow Platform

**Version:** 2.0 (Epic/Story Aligned)
**Date:** June 18, 2025
**Status:** In Refactoring
**Parent Epic:** EPIC-VULTR (Deploy & Showcase Core Sentient Platform on Vultr)
**Related Task Breakdown:** [../../../01_PROJECT_PLANNING/01_04_task_breakdown.md#EPIC-VULTR](README.md) 

---

## 1. Objective

To deploy the Sentient Core platform on Vultr's cloud infrastructure, establishing a robust backend and operational environment. While our primary hackathon showcase will focus on the Qualcomm track (on-device AI), this Vultr deployment serves as a critical foundation. It will demonstrate:
*   The core infrastructure required to support the Sentient Core ecosystem.
*   A platform capable of developing, managing, and potentially orchestrating sophisticated AI agents, including those designed for edge deployment.
*   An example of an enterprise-grade agentic workflow, showcasing the broader capabilities of Sentient Core beyond the immediate on-device demo.

This plan details the technical steps for this foundational Vultr deployment, aligning with EPIC-VULTR and supporting the overall 'Raise Your Hack' competition goals.

## 2. Stories & Detailed Tasks

### STORY-VULTR-1: Configure Vultr Production Environment
-   **Description:** Networking, Security, VM Sizing for Vultr deployment.
-   **Assigned:** AGENT-DEVOPS
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Vultr-1.1:** Provision Vultr cloud compute instance (e.g., High Frequency Compute, select appropriate region and size based on anticipated load).
        -   *Acceptance Criteria:* Vultr instance is active and accessible.
    -   **Task-Vultr-1.2:** Configure base OS (e.g., Ubuntu 22.04 LTS) with security hardening (ufw, fail2ban).
        -   *Acceptance Criteria:* OS is updated, basic security measures are in place.
    -   **Task-Vultr-1.3:** Set up Vultr networking: Static IP, DNS records (e.g., `sentientcore.vultr.example.com`) pointing to the instance.
        -   *Acceptance Criteria:* Instance is reachable via domain name.
    -   **Task-Vultr-1.4:** Configure Vultr security groups/firewall rules to allow necessary traffic (HTTP/S, SSH, specific ports for agent communication if needed).
        -   *Acceptance Criteria:* Only essential ports are open.
    -   **Task-Vultr-1.5:** Set up SSH key-based authentication for secure access.
        -   *Acceptance Criteria:* Password login disabled, SSH keys are functional.
    -   **References:** Vultr Documentation.

### STORY-VULTR-2: Dockerize Sentient Core Application Suite
-   **Description:** Containerize Frontend, Backend API, Agent Services.
-   **Assigned:** AGENT-DEVOPS / AGENT-BACKEND / AGENT-FRONTEND
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Vultr-2.1:** Create `Dockerfile` for Sentient Core Backend (FastAPI).
        -   *Details:* Use a Python base image, install dependencies from `requirements.txt`, copy application code, expose port for Uvicorn.
        -   *Acceptance Criteria:* Backend Docker image builds successfully.
        -   *References:* `../../../02_HACKATHON_CENTRAL/02_06_TECHNOLOGY_GUIDES/02_06_06_fastapi_guide.md`, Docker Documentation.
    -   **Task-Vultr-2.2:** Create `Dockerfile` for Sentient Core Frontend (Next.js 15).
        -   *Details:* Use a multi-stage build. Stage 1: Node.js image to build the app (`npm run build`). Stage 2: Lightweight server (e.g., Nginx or Node.js static server) to serve production assets.
        -   *Acceptance Criteria:* Frontend Docker image builds successfully and serves the application.
        -   *References:* `../../../02_HACKATHON_CENTRAL/02_06_TECHNOLOGY_GUIDES/02_06_07_nextjs_15_guide.md`, Docker Documentation.
    -   **Task-Vultr-2.3:** Create `Dockerfile` for any standalone agent services (if not part of the main backend).
        -   *Acceptance Criteria:* Agent service Docker images build successfully.
    -   **Task-Vultr-2.4:** Test all Docker images locally to ensure they run as expected.
        -   *Acceptance Criteria:* Containers start and basic functionality is verified.

### STORY-VULTR-3: Implement CI/CD Pipeline for Automated Vultr Deployments
-   **Description:** GitHub Actions to Vultr.
-   **Assigned:** AGENT-DEVOPS
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Vultr-3.1:** Design GitHub Actions workflow for CI (linting, testing, security scans).
        -   *Acceptance Criteria:* CI pipeline runs on every push/PR to main branches.
    -   **Task-Vultr-3.2:** Design GitHub Actions workflow for CD (building Docker images, pushing to a registry like Docker Hub or GitHub Container Registry).
        -   *Acceptance Criteria:* New images are built and pushed on merges to main.
    -   **Task-Vultr-3.3:** Implement deployment script (e.g., Bash or Ansible playbook) to be run on the Vultr instance.
        -   *Details:* Script should pull new images, stop old containers, and start new ones using Docker Compose.
        -   *Acceptance Criteria:* Deployment script reliably updates the application.
    -   **Task-Vultr-3.4:** Securely store Vultr SSH credentials and registry credentials in GitHub Secrets.
        -   *Acceptance Criteria:* Secrets are configured and accessible by the CI/CD pipeline.
    -   **Task-Vultr-3.5:** Configure GitHub Actions workflow to trigger the deployment script on the Vultr instance via SSH upon successful image push.
        -   *Acceptance Criteria:* Successful CD pipeline deploys new version to Vultr.

### STORY-VULTR-4: Develop "Enterprise Workflow Agent"
-   **Description:** Demo agent for Vultr track (e.g., marketing content generation or sales lead qualification agent).
-   **Assigned:** AGENT-ARCHITECT / AGENT-BACKEND / AGENT-KNOWLEDGE-SYNTHESIS
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Vultr-4.1:** Define specific use case and capabilities for the Enterprise Workflow Agent.
        -   *Example:* "Automated Blog Post Idea Generator & Outline Creator for Marketing Teams."
        -   *Acceptance Criteria:* Clear problem statement, target users, and desired outcomes defined.
    -   **Task-Vultr-4.2:** Design the agent's LangGraph flow (states, nodes, edges).
        -   *Acceptance Criteria:* Agent workflow diagram and state definitions are complete.
    -   **Task-Vultr-4.3:** Implement agent tools/skills (e.g., web search via Tavily, document analysis, content summarization using Groq/Llama 3).
        -   *Acceptance Criteria:* Tools are functional and tested independently.
        -   *References:* `../../../02_HACKATHON_CENTRAL/02_06_TECHNOLOGY_GUIDES/02_06_01_groq_api_guide.md`
    -   **Task-Vultr-4.4:** Implement the agent logic within the Sentient Core backend (FastAPI service).
        -   *Acceptance Criteria:* Agent can be invoked via an API endpoint.
    -   **Task-Vultr-4.5:** Integrate with Fetch.ai uAgent patterns if the agent requires autonomous periodic tasks or specific protocol interactions.
        -   *Acceptance Criteria:* Fetch.ai components are integrated and functional if used.
        -   *References:* `../../../02_HACKATHON_CENTRAL/02_06_TECHNOLOGY_GUIDES/02_06_03_fetchai_uagent_guide.md`
    -   **Task-Vultr-4.6:** Integrate with Coral Protocol if the agent needs to collaborate with other distinct agents via decentralized discovery/communication.
        -   *Acceptance Criteria:* Coral Protocol components are integrated and functional if used.
        -   *References:* `../../../02_HACKATHON_CENTRAL/02_06_TECHNOLOGY_GUIDES/02_06_04_coral_protocol_guide.md`
    -   **Task-Vultr-4.7:** Develop a simple UI within the Sentient Core frontend to interact with this agent.
        -   *Acceptance Criteria:* User can trigger the agent and see results.
    -   **Task-Vultr-4.8:** Unit test all components of the Enterprise Workflow Agent.
        -   *Acceptance Criteria:* Tests pass, covering core logic and tool integrations.

### STORY-VULTR-5: Implement Monitoring & Logging for Sentient Core on Vultr
-   **Description:** Setup observability for the platform on Vultr.
-   **Assigned:** AGENT-DEVOPS
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Vultr-5.1:** Configure Docker Compose to manage application components (backend, frontend, Nginx reverse proxy).
        -   *Details:* Define services, networks, volumes. Ensure Nginx handles SSL termination and proxies requests to backend/frontend.
        -   *Acceptance Criteria:* `docker-compose up -d` successfully starts all services.
    -   **Task-Vultr-5.2:** Implement structured logging for all application components (FastAPI, Next.js, Nginx).
        -   *Acceptance Criteria:* Logs are consistently formatted (e.g., JSON).
    -   **Task-Vultr-5.3:** Set up basic Vultr monitoring for instance health (CPU, memory, disk, network).
        -   *Acceptance Criteria:* Vultr dashboard shows instance metrics.
    -   **Task-Vultr-5.4:** (Optional Stretch Goal) Deploy a simple log aggregation stack (e.g., ELK minimal or Grafana Loki) if time permits, or ensure logs are easily retrievable from Vultr instance.
        -   *Acceptance Criteria:* Centralized log viewing is possible.
    -   **References:** `../../../03_TECHNICAL_DEEP_DIVES/03_05_llm_observability_management.md`

### STORY-VULTR-6: Prepare Vultr Track Demo Script & Assets
-   **Description:** Finalize demo flow and materials for Vultr presentation.
-   **Assigned:** AGENT-STRATEGIC-EVANGELIST / AGENT-ARCHITECT
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Vultr-6.1:** Outline the demo flow, highlighting key features of the Vultr deployment and the Enterprise Workflow Agent.
        -   *Acceptance Criteria:* Clear, concise demo script is drafted.
    -   **Task-Vultr-6.2:** Create any necessary visual aids or presentation slides.
        -   *Acceptance Criteria:* Supporting materials are ready.
    -   **Task-Vultr-6.3:** Rehearse the demo multiple times to ensure smooth delivery.
        -   *Acceptance Criteria:* Demo can be delivered confidently within time limits.
    -   **Task-Vultr-6.4:** Record a video walkthrough of the deployment and demo.
        -   *Acceptance Criteria:* High-quality video demo is produced.

---

## 3. Success Criteria for Vultr Track (Supporting Role)

- The Sentient Core platform (frontend, backend, example enterprise agent) is successfully deployed and publicly accessible on a Vultr instance, serving as a stable backend and development hub.
- All core services run in Docker containers, orchestrated by Docker Compose, behind an Nginx reverse proxy, demonstrating good DevOps practices.
- An "Enterprise Workflow Agent" (or a similar complex agent) functions correctly, showcasing the platform's capability for multi-step reasoning and tool use (e.g., Groq, Tavily). This demonstrates the potential of Sentient Core beyond the primary on-device demo.
- CI/CD pipeline automates deployment to Vultr, showcasing efficient development workflows.
- Basic monitoring and logging are in place for platform stability.
- The deployment is secure, stable, and performs reliably, providing a solid foundation for the Sentient Core ecosystem.
- Key Vultr infrastructure capabilities are utilized and can be highlighted as part of the broader Sentient Core architecture, supporting the primary Qualcomm track narrative by illustrating how edge agents could be managed or updated in a larger system.
