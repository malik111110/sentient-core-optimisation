# Action Plan: Prosus Track - Agent-Powered E-commerce

**Version:** 1.0
**Date:** June 18, 2025
**Status:** Initial Draft

---

## 1. Objective

To develop an innovative, agent-powered e-commerce solution that leverages the Sentient Core platform to provide a personalized and intelligent shopping experience. This plan details the steps to meet the Prosus sponsor track requirements.

## 2. Key Technologies

- **Backend:** FastAPI
- **Frontend:** Next.js 15
- **Database:** Supabase (PostgreSQL)
- **LLM:** Groq API (Llama 3)
- **Search:** Tavily Search API
- **Voice UI:** Web Speech API (or similar)
- **Knowledge Graph:** Custom implementation using Supabase

## 3. Action Steps

### Phase 1: User Profile & Knowledge Graph (Lead: AGENT-BACKEND)

1.  **Design User Profile Schema:**
    *   [ ] Define a flexible schema in Supabase to store user preferences, purchase history, and inferred interests.
    *   [ ] The schema should support a graph-like structure to represent relationships between users, products, and categories.

2.  **Implement Knowledge Graph Service:**
    *   [ ] Create a FastAPI service to manage the user knowledge graph.
    *   [ ] Develop endpoints to add, update, and query user preferences and product interactions.
    *   [ ] Implement logic to infer user interests based on their activity.

### Phase 2: E-commerce Agent Pack (Lead: AGENT-ARCHITECT)

1.  **Develop Product Research Agent:**
    *   [ ] Create a new agent that integrates with the Tavily Search API.
    *   [ ] The agent will be responsible for finding and comparing products based on user queries.
    *   [ ] The agent will update the user's knowledge graph with the products they show interest in.

2.  **Develop Personal Shopper Agent:**
    *   [ ] Create an agent that uses the user's knowledge graph to provide personalized product recommendations.
    *   [ ] The agent will be able to proactively suggest products based on past behavior and inferred interests.

### Phase 3: Frontend & Voice UI (Lead: AGENT-FRONTEND)

1.  **Build E-commerce UI Components:**
    *   [ ] Create React components for displaying products, search results, and recommendations.
    *   [ ] Integrate the UI with the FastAPI backend to fetch data and trigger agent actions.

2.  **Implement Voice UI:**
    *   [ ] Integrate the Web Speech API for voice input and output.
    *   [ ] Allow users to interact with the e-commerce agents using natural language voice commands.
    *   [ ] The voice UI should be able to handle queries like "Find me a new pair of running shoes" or "What do you recommend for a birthday gift?"

### Phase 4: Integration & Demonstration (Lead: AGENT-ARCHITECT)

1.  **End-to-End Integration:**
    *   [ ] Connect the frontend UI, backend services, and e-commerce agents.
    *   [ ] Ensure a seamless flow of information between all components.

2.  **Prepare Demonstration:**
    *   [ ] Create a compelling demonstration that showcases the personalized shopping experience.
    *   [ ] Highlight the use of the knowledge graph, the product research agent, and the voice UI.

## 4. Success Criteria

- A functional e-commerce agent pack is created and integrated into the Sentient Core platform.
- The system can build and utilize a knowledge graph of user preferences to provide personalized recommendations.
- Users can interact with the platform using a natural language voice interface.
- The solution effectively demonstrates an innovative and intelligent e-commerce experience.
