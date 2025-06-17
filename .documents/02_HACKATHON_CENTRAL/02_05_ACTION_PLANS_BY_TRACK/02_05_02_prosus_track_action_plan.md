# Prosus Track Action Plan: Agent-Powered E-commerce

**Version:** 2.0 (Epic/Story Aligned)
**Date:** June 18, 2025
**Status:** In Refactoring
**Parent Epic:** EPIC-PROSUS (Develop Agent-Powered E-commerce Pack)
**Related Task Breakdown:** [../../../01_PROJECT_PLANNING/01_04_task_breakdown.md#EPIC-PROSUS](README.md)

---

## 1. Objective

To develop an innovative, agent-powered e-commerce solution that leverages the Sentient Core platform to provide a personalized and intelligent shopping experience. This plan details the steps to meet the Prosus sponsor track requirements, organized by stories under EPIC-PROSUS.

## 2. Stories & Detailed Tasks

### STORY-PROSUS-1: Design & Implement User Knowledge Graph
-   **Description:** Supabase schema, FastAPI service for KG management.
-   **Assigned:** AGENT-BACKEND / AGENT-DATA-ARCHITECT
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Pros-1.1:** Design a flexible Supabase schema for user profiles (preferences, purchase history, demographics) and product data (attributes, categories).
        -   *Acceptance Criteria:* Schema diagram and SQL definitions are complete and reviewed.
    -   **Task-Pros-1.2:** Implement Supabase tables and relationships based on the designed schema.
        -   *Acceptance Criteria:* Tables are created in Supabase; RLS policies are in place for security.
    -   **Task-Pros-1.3:** Develop a FastAPI service/module for Knowledge Graph (KG) management.
        -   *Details:* Endpoints for creating/updating user nodes, product nodes, and relationship edges (e.g., "viewed," "purchased," "interested_in").
        -   *Acceptance Criteria:* API endpoints are functional and tested.
    -   **Task-Pros-1.4:** Implement logic within the KG service to infer user interests and build/update their profile graph based on interactions (e.g., product views, searches, purchases).
        -   *Acceptance Criteria:* User interest inference logic is implemented and validated.
    -   **References:** Supabase Documentation, FastAPI Documentation (`../../../02_HACKATHON_CENTRAL/02_06_TECHNOLOGY_GUIDES/02_06_06_fastapi_guide.md`).

### STORY-PROSUS-2: Develop "Product Discovery Agent"
-   **Description:** Tavily Search integration, KG updates.
-   **Assigned:** AGENT-BACKEND / AGENT-KNOWLEDGE-SYNTHESIS
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Pros-2.1:** Define the Product Discovery Agent's capabilities and interaction flow.
        -   *Details:* Agent should understand natural language queries for products, use Tavily for broad web search, and filter/rank results.
        -   *Acceptance Criteria:* Agent specification document is complete.
    -   **Task-Pros-2.2:** Implement Tavily Search API client within Sentient Core.
        -   *Acceptance Criteria:* Tavily client can fetch and parse search results.
    -   **Task-Pros-2.3:** Develop the core logic for the Product Discovery Agent.
        -   *Details:* Integrate Tavily client, process search results, extract relevant product information.
        -   *Acceptance Criteria:* Agent can return a list of relevant products based on a query.
    -   **Task-Pros-2.4:** Integrate the agent with the User Knowledge Graph service to log products viewed/selected by the user, contributing to their profile.
        -   *Acceptance Criteria:* Agent interactions update the user's KG.
    -   **Task-Pros-2.5:** Implement a FastAPI endpoint to expose the Product Discovery Agent's functionality.
        -   *Acceptance Criteria:* Agent is callable via an API.
    -   **References:** Tavily Search API Documentation.

### STORY-PROSUS-3: Develop "Personal Shopper Agent"
-   **Description:** Personalized recommendations from KG, proactive suggestions.
-   **Assigned:** AGENT-BACKEND / AGENT-DATA-SCIENTIST
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Pros-3.1:** Define the Personal Shopper Agent's capabilities.
        -   *Details:* Agent should leverage the User KG to provide recommendations, explain reasoning, and potentially offer proactive suggestions based on learned preferences or triggers (e.g., new arrivals in preferred categories).
        -   *Acceptance Criteria:* Agent specification document is complete.
    -   **Task-Pros-3.2:** Develop algorithms/logic for generating personalized recommendations from the KG (e.g., collaborative filtering concepts, content-based filtering, or graph traversal).
        -   *Acceptance Criteria:* Recommendation logic is implemented and can generate relevant suggestions.
    -   **Task-Pros-3.3:** Implement the core logic for the Personal Shopper Agent.
        -   *Acceptance Criteria:* Agent can provide personalized product recommendations.
    -   **Task-Pros-3.4:** (Optional Stretch) Implement a mechanism for proactive suggestions (e.g., based on time, new inventory, or user's browsing patterns).
        -   *Acceptance Criteria:* Proactive suggestion feature is functional if implemented.
    -   **Task-Pros-3.5:** Implement a FastAPI endpoint to expose the Personal Shopper Agent's functionality.
        -   *Acceptance Criteria:* Agent is callable via an API.

### STORY-PROSUS-4: Implement Voice UI for E-commerce Interaction
-   **Description:** Web Speech API, command parsing, agent invocation.
-   **Assigned:** AGENT-FRONTEND / AGENT-BACKEND
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Pros-4.1:** Research and select a suitable Web Speech API or library for speech-to-text (STT) and text-to-speech (TTS) in the Next.js frontend.
        -   *Acceptance Criteria:* Chosen technology is documented and justified.
    -   **Task-Pros-4.2:** Implement STT functionality in the frontend to capture user voice commands.
        -   *Acceptance Criteria:* Voice input is accurately transcribed to text.
    -   **Task-Pros-4.3:** Develop a command parser (either frontend or backend) to interpret transcribed voice commands and map them to e-commerce agent actions (e.g., "Find me red running shoes," "What are my recommendations?").
        -   *Acceptance Criteria:* Voice commands are correctly parsed into actionable requests.
    -   **Task-Pros-4.4:** Integrate voice command processing with the Product Discovery and Personal Shopper agent API endpoints.
        -   *Acceptance Criteria:* Voice commands successfully trigger agent actions.
    -   **Task-Pros-4.5:** Implement TTS functionality in the frontend to provide voice responses from the agents.
        -   *Acceptance Criteria:* Agent responses are clearly spoken to the user.
    -   **Task-Pros-4.6:** Design and implement UI elements for voice interaction (e.g., microphone button, visual feedback for listening/speaking).
        -   *Acceptance Criteria:* Voice UI is intuitive and user-friendly.
    -   **References:** Web Speech API documentation, Next.js documentation (`../../../02_HACKATHON_CENTRAL/02_06_TECHNOLOGY_GUIDES/02_06_07_nextjs_15_guide.md`).

### STORY-PROSUS-5: Build E-commerce Frontend Interface
-   **Description:** Product display, search results, recommendations UI.
-   **Assigned:** AGENT-FRONTEND
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Pros-5.1:** Design UI mockups/wireframes for the e-commerce interface (product listings, product details, search results, recommendation carousels, voice interaction points).
        -   *Acceptance Criteria:* UI designs are approved.
    -   **Task-Pros-5.2:** Develop React components (using Shadcn/UI, DaisyUI, Tailwind CSS) for displaying products, search results, and recommendations.
        -   *Acceptance Criteria:* Components are responsive and adhere to design.
    -   **Task-Pros-5.3:** Integrate frontend components with FastAPI agent endpoints to fetch and display data.
        -   *Acceptance Criteria:* Frontend dynamically displays data from the backend.
    -   **Task-Pros-5.4:** Implement user authentication and session management if personalized features require login (can leverage Supabase Auth).
        -   *Acceptance Criteria:* Users can log in/out (if applicable).
    -   **Task-Pros-5.5:** Ensure the e-commerce interface is responsive and provides a good user experience on various devices.
        -   *Acceptance Criteria:* UI is tested on desktop and mobile.

### STORY-PROSUS-6: Prepare Prosus Track Demo Script & Assets
-   **Description:** Finalize demo flow and materials for Prosus presentation.
-   **Assigned:** AGENT-STRATEGIC-EVANGELIST / AGENT-ARCHITECT
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Pros-6.1:** Outline the demo flow, showcasing the agent-powered e-commerce features (KG-based personalization, Tavily product discovery, voice UI).
        -   *Acceptance Criteria:* Clear, concise demo script is drafted.
    -   **Task-Pros-6.2:** Create any necessary visual aids or presentation slides.
        -   *Acceptance Criteria:* Supporting materials are ready.
    -   **Task-Pros-6.3:** Rehearse the demo multiple times.
        -   *Acceptance Criteria:* Demo can be delivered confidently.
    -   **Task-Pros-6.4:** Record a video walkthrough of the e-commerce solution.
        -   *Acceptance Criteria:* High-quality video demo is produced.

---

## 3. Success Criteria for Prosus Track

- A functional e-commerce agent pack (Product Discovery, Personal Shopper) is created and integrated into the Sentient Core platform.
- The system can build and utilize a knowledge graph of user preferences (stored in Supabase, managed via FastAPI) to provide personalized recommendations.
- Users can interact with the platform using a natural language voice interface (STT/TTS).
- The solution effectively demonstrates an innovative and intelligent e-commerce experience.
- All Prosus track requirements from the `02_02_raise_your_hack_overview.md` are met.
