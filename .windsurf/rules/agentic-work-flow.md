---
trigger: model_decision
description: when agentic development flow is needed
---

**2. The Standard Agentic Development Flow**
This is the primary workflow the system will follow to translate a user's idea into a functional prototype.

*   **Phase 1: Clarification & Scoping (Input Agent)**
    *   **Trigger:** User provides an initial free-form request or starts a guided quiz.
    *   **Process:** An agent analyzes the initial input. If it's ambiguous, it triggers a sequence of up to three clarifying open-ended questions. Subsequently, it presents two rounds of structured, multiple-choice quizzes to finalize key product attributes (e.g., app type, target audience, core functionality).
    *   **Output:** A structured JSON object containing a detailed summary of the user's requirements. This object is saved to the Memory Bank.

*   **Phase 2: Design & Wireframing (UX/UI Agent)**
    *   **Trigger:** Successful completion of Phase 1.
    *   **Process:** An agent retrieves the requirements JSON. It then prompts a multimodal model (**Gemini 1.5 Pro**) to generate two distinct visual options for key screen wireframes and user flows.
    *   **Output:** A structured response containing two sets of images and corresponding descriptions for user selection.

*   **Phase 3: Code Generation (Frontend/Backend Agents)**
    *   **Trigger:** User selects a wireframe option from Phase 2.
    *   **Process:** The Architecting Agent creates a plan. Then, specialized agents (Frontend, Backend) retrieve all prior data (requirements, chosen wireframes) and execute the plan, generating the necessary code (HTML, CSS, JS for the MVP). The code is written to the sandboxed file system.
    *   **Output:** A complete set of code files within the Sandbox environment, ready for rendering.

*   **Phase 4: Documentation & Handoff (Architecting Agent)**
    *   **Trigger:** Successful generation of the MVP.
    *   **Process:** The system offers the user the ability to generate comprehensive project documentation based on the entire interaction history.
    *   **Output:** User-selectable documents: PRD, Tech Specs, Project Roadmap, etc.