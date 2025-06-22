

---

## **Blueprint for an AI-Powered Development Platform: User Experience & Agentic Workflow**

**Goal:** To engineer an intelligent AI-driven platform that empowers users to effortlessly generate and iterate on applications, leveraging a sophisticated agentic architecture and interactive development environments like Webcontainer and E2B. This document outlines the core user journey and the underlying AI agent responsibilities.

---

### **Section 1: The User Journey – Front-End Interaction & Progressive Refinement**

This section details the user's experience within the platform, emphasizing the front-end interactions and the seamless integration of Webcontainer and E2B for dynamic UI and execution. While agent actions are mentioned, the primary focus here is on the user's perspective and the system's presentation.

**1. Initial Engagement: The Dashboard & Project Incubation**

*   **User State:** The user begins at the main dashboard, poised to initiate a new project.
*   **Primary Input:** A prominent text area is provided for the user's initial project prompt.
*   **Prompt Enhancement:** The system offers advanced prompt enhancement capabilities, similar to [flowith 2.0 - Your AI Creation Workspace, with Knowledge](https://flowith.io/blank), guiding users to articulate their vision effectively.
*   **Contextual Input Options:**
    *   **Video Upload:** Users can upload video content to provide visual context or demonstrate desired functionalities.
    *   **URL Context:** Users can provide a URL to an existing website.
        *   **Agent Activation:** Upon URL input, the **Web Cloner Agent** is automatically activated. This agent will autonomously scrape the target website, learn its structure, capture screenshots, and extract relevant design and functional elements to inform the new project.

**2. Project Generation Modes: Tailored Development Paths**

The platform offers two distinct modes to accommodate varying user needs and desired levels of control:

*   **2.1. YOLO Mode (You Only Live Once): Rapid Full-App Generation**
    *   **Description:** This mode is designed for speed and simplicity. A single, comprehensive prompt from the user directly initiates the generation of a complete, functional application.
    *   **AI Task:** The AI system will interpret the prompt, make intelligent assumptions where necessary, and deliver a finished application with minimal user intervention.

*   **2.2. Walk Me Through Mode: Iterative & Guided Development**
    *   **Description:** This mode provides an interactive, step-by-step guidance system, allowing users to progressively define their application with detailed feedback and choices from the AI.
    *   **Initial Interaction:**
        *   The system presents an expanding accordion interface with a series of structured questions.
        *   **Example Questions:** "What kind of application or website do you intend to build?"
        *   **Input Mechanisms:** Users can respond via predefined button choices or a flexible text input box.
    *   **Deepening Understanding via Chat:**
        *   The AI will engage in a dynamic chat conversation, expanding the chat box to offer structured output, multiple-choice options, and selection feels.
        *   **AI Goal:** To thoroughly understand the user's purpose, target audience, and desired features for the application.
    *   **Foundation & Agent Selection:**
        *   Once the foundational understanding is established, the UI will present a list of interactive button cards (similar to the Flowith interface example).
        *   **User Action:** Users can explicitly select specific AI agents to collaborate on their project (e.g., Front-End Designer, Backend Architect).
    *   **Interactive Flow UI (Perplexity Labs-like Experience):**
        *   **Transition:** The system transitions to an advanced "Flow UI" screen, designed for controlled, iterative development.
        *   **Layout:** This UI will feature a flexible 2 or 3-column layout to display various outputs from the AI agents.
        *   **Dynamic Outputs:** This includes:
            *   Wireframes and Low-Fidelity Mockups
            *   Architectural Graphs and Diagrams
            *   Interactive Application UI Previews (rendered via Webcontainer/E2B for live interaction)
            *   Structured Data Visualizations and Charts
        *   **Sandbox Integration:** **Crucially, sandbox environments are leveraged to create and render these interactive UI components and visual representations. The `Chooser` utility intelligently selects between WebContainer (via the `WebContainerTool`) for frontend previews and E2B (via the `E2BSandboxTool`) for backend tasks, allowing for real-time feedback and manipulation.**
        *   **Comprehensive Document Display:** This Flow UI also serves as a central hub for displaying and collecting:
            *   Project Documents (e.g., Markdown files, PDFs)
            *   Images (e.g., mood boards, design inspirations)
            *   Code Snippets and Examples
            *   **AI Task:** All displayed documents are actively collected and stored by the AI for final extraction and synthesis into comprehensive project documentation.
    *   **Granular Agentic Workflow & Confirmation:**
        *   **Principle:** The agent flow is designed to ensure granular task completion. Agents will proceed only after completing smaller, defined steps.
        *   **Confirmation:** When progressing, the system will explicitly confirm the agent's work and automatically collect and temporarily store information into three critical sets:
            1.  **Project Structure & Overview:** Captures high-level features and flow. The AI agents are empowered to identify vague or potentially incorrect user inputs, transforming them and seeking explicit confirmation when necessary to ensure alignment.
            2.  **Technical Domain Breakdown:** Categorizes information into relevant technical domains (Front-End, Back-End, API, Hooks, Database, Schema, CMS, etc.). The AI agents will dynamically adjust the depth of technical questioning based on the user's detected tech expertise and the project's complexity. Initially, relational metadata might be implicit in temporary memory, but will be formalized as development progresses.
            3.  **Product Requirements Document (PRD):** This document is continuously synthesized and populated throughout the entire development flow, evolving with each user interaction and agent output.
    *   **Automated Technical Decisions for MVP:**
        *   **Scenario:** If the user does not explicitly specify technical choices (e.g., database type, API structure) for the Minimum Viable Product (MVP).
        *   **AI Action:** AI agents will autonomously make these decisions based on best practices and project context.
        *   **User Notification:** The system will clearly communicate these automated decisions to the user via on-screen messages, providing easy-to-understand explanations.
    *   **Flow Constraints & Output Diversity:**
        *   **Question Limit:** The "Walk Me Through" flow is optimized to ask no more than 10 core questions.
        *   **Output Diversity:** It will generate approximately 6 distinct types of output, including:
            *   User Interface Choices (interactive elements)
            *   Images (design concepts, mockups)
            *   Interactive Boards (e.g., kanban, mind maps)
            *   Charts or Diagrams (showing architecture, data flow)
            *   Markdown or PDF Files (e.g., matrices, tables, structured reports)
    *   **Core Agents in "Walk Me Through" Flow:**
        *   **Front-End Designer Agent:** Focuses on user interface, experience, and visual aesthetics.
        *   **Back-End & API State Structure Architect Agent:** Designs the server-side logic, data models, and API interfaces.
        *   **Stake & Feature Solutions Research & Analysis Architect Agent:** Conducts research, analyzes requirements, and proposes optimal solutions for features and business logic.
    *   **Industry-Specific Agent Integration:**
        *   **Dynamic Inclusion:** If an **Industry Vertical Agent** (formerly "industry-specific agent") is selected or inferred, it will seamlessly join the flow.
        *   **Role:** This agent suggests industry best practices, investigates specific domain requirements, and harnesses optimal solutions tailored to the user's field or department.
    *   **Comprehensive Documentation Generation:**
        *   The system generates at least three types of comprehensive documents, further categorized into supportive sub-documents:
            1.  **Project Documentation:**
                *   **Project High-Level Plan:** Outlines goals, objectives, and scope.
                *   **Product Requirements Document (PRD):** Defines functional/non-functional requirements, user stories, and use cases.
                *   **Future Visions & Roadmap:** States clear scalability plans and anticipated changes.
            2.  **Design Documentation:**
                *   **Wireframes & Mockups:** Visual representations of the UI layout and structure.
                *   **Data Model Diagram:** Illustrates database structure and entity relationships.
                *   **API Documentation:** Details the structure and usage of application APIs.
            3.  **Technical Documentation:**
                *   **Architecture Overview:** Explains overall application structure, components, and interactions.
                *   **Code Documentation:** Explains purpose and functionality of modules, functions, and classes.
                *   **API Specifications:** Provides detailed API information, including request/response formats.
                *   **Technology Selection Document:** Details chosen technologies (languages, frameworks, libraries, databases).
                *   **Third-Party Libraries:** Specifies all external dependencies.
            4.  **Specialized Documents (Conditional):** For industry/department-specific users, the system can generate tailored documents like business plans, marketing plans, teaching plans, or syllabi. Each of these will be structured to provide maximum utility.

**3. Transition to Pro Mode: The Integrated Development Environment (IDE-like)**

*   **User State:** After the comprehensive planning and documentation generation in the "Walk Me Through" flow, the user seamlessly transitions to the "Pro Mode" screen.
*   **Interface:** This mode presents an IDE-like environment, similar to `bold.new`, featuring:
    *   **Code Editor:** For direct code manipulation.
    *   **Live Preview Panel:** To visualize changes in real-time.
    *   **Integrated Terminal:** For command-line operations.
    *   **File/Code Tree:** For navigating the project structure.
*   **The Documents Drawer: Multi-Layered Knowledge Memory**
    *   **Unique Feature:** A specialized "Documents Drawer" provides access to a powerful, multi-layered knowledge memory system.
    *   **Memory Architecture:** These documents are not merely static files; they are:
        *   **Chunked:** Broken into manageable units.
        *   **Vectorized:** Converted into numerical representations for efficient semantic search.
        *   **Hierarchical:** Organized in a logical tree structure.
        *   **Relational Graph:** Interconnected with metadata to show relationships.
        *   **Clustered:** Grouped by similarity or topic.
    *   **Knowledge Memory Layers (Examples):**
        *   **Task-Based & Plans Layer:** Stores detailed execution plans and task breakdowns.
        *   *(Further layers to be defined, e.g., Codebase Knowledge Layer, User Preferences Layer, System Constraints Layer).*

---

**4. Core Agentic Tools: The Execution Layer**

These tools form the practical execution layer, translating agent decisions into actions within sandboxed environments. They are the direct interface to the E2B and WebContainer technologies.

*   **4.1. The `Chooser` Utility:**
    *   **Location:** `src/sentient_core/orchestrator/chooser.py`
    *   **Role:** This critical utility acts as a traffic controller. Based on a defined decision tree (e.g., task requirements, language, need for UI), it determines whether a given task should be executed in a WebContainer or an E2B sandbox. This is invoked by the **Coordinator** agent before dispatching tasks.

*   **4.2. The `WebContainerTool`:**
    *   **Location:** `src/sentient_core/tools/webcontainer_tool.py`
    *   **Role:** This tool serves as the primary interface for the **FrontEndAgent**. It packages files (HTML, CSS, JS) and commands to be run in a client-side WebContainer instance, enabling live, interactive UI previews and development.

*   **4.3. The `E2BSandboxTool`:**
    *   **Location:** `src/sentient_core/tools/e2b_sandbox_tool.py`
    *   **Role:** This tool is used by the **BackEndAgent** to securely execute backend code (e.g., Python, Node.js scripts) in an isolated E2B cloud sandbox. It is ideal for running tests, data processing, and validating server-side logic.

---

### **Section 2: The Sentient-Core Agent Architecture**

This section details the specialized AI agents that form the intelligent core of the platform, enabling sophisticated code generation and project management.

**1. Sentient-Core Exclusive Agents: Specialized Capabilities**

These agents possess unique, high-level capabilities crucial for advanced project development.

*   **1.1. Image Generation Agent:** Capable of generating visual assets, icons, and UI elements based on textual prompts or design specifications.
*   **1.2. Video Generation Agent:** Specializes in creating video content, such as UI walkthroughs, promotional clips, or animated explanations.
*   **1.3. Multimedia Understanding Agent:** This agent excels at interpreting complex concepts embedded within uploaded multimedia (videos, images, audio). It extracts key ideas, identifies patterns, and translates visual/auditory information into actionable insights for other agents.
*   **1.4. Industry Vertical Agent (Suggested Renaming for "industry-specific agent"):**
    *   **Role:** This intelligent agent analyzes user input (prompts, uploaded sources, context) to accurately detect the user's industry, job role, or specific department for which they are developing the application.
    *   **Coordination:** It then coordinates with other agents, providing best practices, industry-specific templates, optimal tech stacks, and tailored development pipelines relevant to that domain, ensuring highly optimized and relevant solutions.
*   **1.5. Data Visualization Agent:** Generates interactive graphs, charts, and comprehensive data analyses presented in visually intuitive formats directly within the UI.
*   **1.6. Prototype Agent:**
    *   **Core Function:** While the platform holistically adapts to all user tech levels by breaking down tasks and facilitating detailed back-and-forth conversations, the Prototype Agent visualizes these steps.
    *   **Output:** It presents interactive options for wireframes, front-end interfaces of varying styles and layouts (simple HTML/CSS builds).
    *   **User Benefit:** Empowers users to visualize the end product at early stages, ensuring alignment and reducing rework.
*   **1.7. Open-Source Repository Ingestion & Integration Agent:**
    *   **Input:** Users can provide direct GitHub links, or the agent can intelligently scout public repositories via search engines.
    *   **Process:**
        1.  **Cloning & Sandboxing:** Clones the target repository into a secure sandbox environment (leveraging Webcontainer/E2B for isolated execution).
        2.  **Feature Learning:** Collaborates with other agents (e.g., Codebase Memory Knowledge Layer Agent, Architecture Agent, Plan & Task Breakdown Agent) to run, analyze, and thoroughly understand all features and functionalities of the ingested codebase.
        3.  **Dissection & Reasoning:** After a comprehensive dissection process, a highly intelligent model with advanced reasoning capabilities synthesizes insights from the user's existing codebase.
        4.  **Selection & Planning:** It intelligently selects relevant components, identifies areas for integration, and generates a detailed development plan based on the current codebase.
        5.  **Execution Handoff:** The refined plan is then handed off to other specialized agents for granular task breakdown and execution.

**2. Enabled by Default Sentient-Core Agents: Code Domain Synthesizers/Regulators**

These agents are foundational to the platform's code generation capabilities, acting as specialized domain experts.

*   **Domains of Expertise:**
    *   Database Management
    *   Backend Logic
    *   API Definition & Implementation
    *   Frontend Hooks & State Management
    *   Frontend UI & UX
    *   Authentication & Type Definitions
    *   Configuration Management (YAML/JSON/XML)
    *   Utilities & Tooling (scripts, CLIs)
*   **Their Core Responsibilities:**
    *   **Task Ingestion:** Receive granular, actionable task breakdowns with assigned domains from the main **Sentient-Core Supervisor Agent**.
    *   **Deep Domain Understanding:** Possess profound comprehension of code structures, languages, and syntax within their specific domain.
    *   **Contextual Awareness:** Are continuously fetched with the latest changes from their own domain and closely related domains.
    *   **Knowledge Retrieval:** Actively query and retrieve necessary document parts/nodes and key summaries from the vectorized, hierarchical knowledge memory layers, including past chat sessions.
    *   **Hierarchical Synthesis:** Synthesize all gathered information into clear, hierarchical build steps and sequences tailored for their respective domain builders.
    *   **Prototyping Note:** While the ultimate vision involves distinct domain coders, for the current prototype, a single versatile model may initially perform the coding tasks across all domains, demonstrating the end-to-end flow.

**3. Other Sentient-Brain Agents: Memory & Knowledge Integration**

These agents work in synergy with the memory layers, ensuring a robust and context-aware development process.

*   **Code Knowledge Memory Agent:**
    *   **Functionality:** This agent is deeply involved in integrating with all other agents and leveraging the platform's multi-layered memory system (clusters, nodes, vectorized graphs).
    *   **Goal:** To provide real-time, contextually relevant code knowledge, best practices, and historical project data to inform agent decisions and code generation.

---
