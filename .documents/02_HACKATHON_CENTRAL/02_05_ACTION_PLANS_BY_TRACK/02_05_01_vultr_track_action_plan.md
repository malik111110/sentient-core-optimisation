# Action Plan: Vultr Track - Enterprise Agentic Workflow Platform

**Version:** 1.0
**Date:** June 18, 2025
**Status:** Initial Draft

---

## 1. Objective

To deploy the Sentient Core platform on Vultr's cloud infrastructure and demonstrate a sophisticated, enterprise-grade agentic workflow. This plan details the technical steps required to meet the Vultr sponsor track requirements for the 'Raise Your Hack' competition.

## 2. Key Technologies

- **Cloud Provider:** Vultr
- **Backend:** FastAPI
- **Frontend:** Next.js 15
- **Containerization:** Docker
- **LLM:** Groq API (Llama 3)
- **Agent Framework:** Fetch.ai uAgents
- **Communication:** Coral Protocol

## 3. Action Steps

### Phase 1: Infrastructure Setup (Lead: AGENT-DEVOPS)

1.  **Provision Vultr Instance:**
    *   [ ] Create a new Vultr cloud compute instance (e.g., High Frequency Compute).
    *   [ ] Configure the instance with a standard OS (e.g., Ubuntu 22.04).
    *   [ ] Set up networking, security groups, and SSH access.

2.  **Install Core Dependencies:**
    *   [ ] Install Docker and Docker Compose on the Vultr instance.
    *   [ ] Install Nginx to act as a reverse proxy.
    *   [ ] Configure DNS records to point to the Vultr instance's IP address.

### Phase 2: Application Containerization (Lead: AGENT-BACKEND, AGENT-FRONTEND)

1.  **Backend (FastAPI) Dockerization:**
    *   [ ] Create a `Dockerfile` for the FastAPI application.
    *   [ ] Ensure the container installs all Python dependencies from `requirements.txt`.
    *   [ ] Configure the container to run the FastAPI application using `uvicorn`.

2.  **Frontend (Next.js) Dockerization:**
    *   [ ] Create a multi-stage `Dockerfile` for the Next.js application.
    *   [ ] The first stage will build the production-ready application (`npm run build`).
    *   [ ] The second stage will serve the static build artifacts using a lightweight server.

### Phase 3: Deployment & Orchestration (Lead: AGENT-DEVOPS)

1.  **Create Docker Compose Configuration:**
    *   [ ] Create a `docker-compose.yml` file to define and orchestrate the backend, frontend, and database services.
    *   [ ] Configure environment variables for all services, including API keys for Groq and Fetch.ai (to be injected securely).

2.  **Deploy to Vultr:**
    *   [ ] Copy the project source code to the Vultr instance.
    *   [ ] Run `docker-compose up -d --build` to build and start the application containers.
    *   [ ] Verify that all containers are running and communicating correctly.

3.  **Configure Reverse Proxy:**
    *   [ ] Configure Nginx to route traffic to the appropriate containers (e.g., `/api/*` to the FastAPI backend, `/` to the Next.js frontend).
    *   [ ] Set up SSL/TLS using Let's Encrypt to secure the application.

### Phase 4: Integration & Demonstration (Lead: AGENT-ARCHITECT)

1.  **Implement Core Agentic Workflow:**
    *   [ ] Develop the logic for the demonstration workflow (e.g., an automated market research agent).
    *   [ ] Ensure the workflow correctly utilizes the Groq, Fetch.ai, and Coral Protocol clients.

2.  **Final Testing & Validation:**
    *   [ ] Conduct end-to-end testing of the deployed application.
    *   [ ] Verify that the agentic workflow runs successfully in the Vultr environment.
    *   [ ] Prepare a demonstration script and record a video walkthrough.

## 4. Connecting to Our Users

This Vultr track directly addresses the needs of key user personas (see `../../../00_CONCEPTUAL_FRAMEWORK/00_03_user_personas.md`):

*   **For Morgan, The Development Team Lead:** Deploying Sentient Core on Vultr provides a standardized, enterprise-grade environment. This aligns with Morgan's goals of ensuring architectural consistency, standardizing development processes, and delivering high-quality software. The containerized approach (Docker) and reverse proxy setup (Nginx) reflect best practices that Morgan would champion, alleviating pain points around complex stack management and ensuring maintainability.
*   **For Alex, The Technical Entrepreneur:** A robust Vultr deployment means Alex can take their rapidly developed MVPs (built with Sentient Core) and scale them reliably. This addresses Alex's need for speed and quality, ensuring that the technology underpinning their vision is solid and can grow with their business, avoiding the pitfalls of solutions that are easy to start but hard to scale.

By showcasing a seamless deployment to a leading cloud provider like Vultr, we demonstrate that Sentient Core is not just a development tool but a complete platform for bringing sophisticated applications to life and managing them effectively.

---

## 5. Success Criteria

- The Sentient Core platform is successfully deployed and accessible on a Vultr instance.
- The backend and frontend services are running in Docker containers, orchestrated by Docker Compose.
- A functional, enterprise-grade agentic workflow is demonstrated, showcasing the integration of Groq, Fetch.ai, and Coral Protocol.
- The deployment is secure, stable, and performs reliably.
