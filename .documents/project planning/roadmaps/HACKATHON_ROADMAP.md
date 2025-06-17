# Sentient Core: Hackathon Development Roadmap ('Raise Your Hack' MVP)

## Phase 1: Core Platform & Vultr Track (Sprint 1-2)
- **Objective**: Deploy the core Sentient Core platform on Vultr and demonstrate an enterprise agentic workflow.
- **Deliverables**:
  - FastAPI backend and Next.js frontend containerized with Docker.
  - CI/CD pipeline for automated deployment to Vultr infrastructure.
  - Functional "Automated Market Research" agent utilizing Groq/Llama 3.
  - Web interface for initiating and monitoring the agent workflow.

## Phase 2: Prosus E-Commerce Pack (Sprint 3-4)
- **Objective**: Develop and integrate the agent-powered e-commerce solution.
- **Deliverables**:
  - E-commerce agent capable of product discovery and recommendation.
  - Integration with Tavily API for real-time product/service search.
  - ChromaDB-backed knowledge graph for dynamic user profiles.
  - Personalization of agent responses based on the user's knowledge graph.

## Phase 3: Qualcomm Edge Utility & Final Polish (Sprint 5-6)
- **Objective**: Implement the on-device AI utility generator and prepare for final submission.
- **Deliverables**:
  - Sentient Core module to generate Python code for a consumer utility.
  - AI model conversion to `.ort` format for on-device inference with ONNX Runtime.
  - Generated utility runs offline, targeting Snapdragon X Elite via QNN Execution Provider.
  - Final integration, testing, and documentation for all three sponsor tracks.
