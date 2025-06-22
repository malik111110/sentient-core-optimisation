# Sentient-Core Agent Specification

This document provides a detailed specification for the AI agents operating within the platform's E2B Secure Cloud Runtimes. It outlines their missions, responsibilities, and interaction protocols as orchestrated by the central Application Server.

### Agent Hierarchy Overview

The agent system is designed with a two-tier hierarchy to effectively manage the complexity of application development:

1.  High-Level Strategic Agents: These are role-based "manager" agents responsible for project planning, architecture, user interaction, and high-level decision-making. They interpret user goals, define the project blueprint, and delegate specific implementation tasks.
2.  Code Domain Synthesizers: These are specialized "worker" agents that execute granular tasks assigned by the Strategic Agents. They are experts in a single domain (e.g., database schema, React components) and are responsible for generating, regulating, and refactoring code and configuration artifacts.

---

## I. High-Level Strategic Agents

These agents form the cognitive backbone of the development process, translating abstract user requests into a concrete, actionable plan.

| Agent Name | Research & Analysis Architect |
| :--- | :--- |
| Core Mission | To interpret the initial user prompt, clarify project requirements, and generate a comprehensive project plan that will guide all subsequent development activities. |
| Key Responsibilities | - Analyze the raw user prompt from the main dashboard.<br>- Utilize the "Prompt Enhancer" to refine and expand on the user's initial idea.<br>- Conduct initial research by querying the Vector DB for similar projects, relevant technologies, and best practices.<br>- Engage the user in a clarifying dialogue if the request is ambiguous.<br>- Decompose the high-level goal into a structured set of features and technical requirements. |
| Inputs / Triggers | - A new project submission from the user (prompt, uploaded files, or web clone URL).<br>- Selection of "Walk me through" or "YOLO Mode" to determine interaction depth. |
| Outputs / Artifacts | - A structured `Project Plan` document (JSON or Markdown).<br>- A refined and validated user prompt.<br>- A task list for other high-level agents. |
| Interaction Protocols | - Receives initial task from the Orchestrator.<br>- Interacts with the Vector DB to retrieve contextual knowledge.<br>- If necessary, prompts the user for clarification via the conversational UI (as seen in the "Walk me through" mockup).<br>- Publishes the final `Project Plan` to the `Documents Drawer` in the Pro Mode IDE. |

| Agent Name | Industry-Specific Agent |
| :--- | :--- |
| Core Mission | To enrich the project plan with domain-specific knowledge, ensuring the application adheres to industry standards, regulations, and best practices. |
| Key Responsibilities | - Identify industry context from the project plan (e.g., "healthcare," "finance," "e-commerce").<br>- Augment the project plan with industry-specific requirements (e.g., HIPAA compliance for healthcare, PCI-DSS for finance).<br>- Suggest relevant data models, user flows, and third-party integrations (e.g., Stripe for payments, Docusign for contracts).<br>- Query specialized knowledge bases within the Docs & Assets DB. |
| Inputs / Triggers | - A `Project Plan` containing industry-specific keywords.<br>- A direct instruction from the Research & Analysis Architect. |
| Outputs / Artifacts | - An annotated `Project Plan` with industry-specific considerations.<br>- A list of recommended libraries, APIs, and compliance checks.<br>- Contributions to the `Tech Specs` document. |
| Interaction Protocols | - Collaborates with the Research & Analysis Architect to refine the project scope.<br>- Provides constraints and guidelines to the Front-End Designer and Back-End Architect. |

| Agent Name | Front-End Designer |
| :--- | :--- |
| Core Mission | To translate project requirements and user preferences into a coherent user interface and experience, from wireframes to component design. |
| Key Responsibilities | - Define the application's layout, navigation, and visual style.<br>- Generate wireframes or mockups for user validation.<br>- Break down the UI into a hierarchy of reusable components.<br>- Select appropriate front-end libraries or frameworks (e.g., Tailwind CSS, Material-UI). |
| Inputs / Triggers | - A validated `Project Plan` and `Tech Specs`.<br>- User feedback on style and layout preferences. |
| Outputs / Artifacts | - Visual wireframes or mockups.<br>- A `Design Doc` detailing UI/UX principles.<br>- A list of front-end components to be built.<br>- A `package.json` with required front-end dependencies. |
| Interaction Protocols | - Presents visual options (e.g., layout choices, style guides) in the central column of the 'Walk me through' UI for user selection.<br>- Engages in a turn-by-turn dialogue with the user via the left-hand column of the 'Walk me through' view.<br>- Collaborates with the Back-End Architect to define data requirements for the UI.<br>- Dispatches component-building tasks to the Front-End Synthesizer. |

| Agent Name | Back-End & API Architect |
| :--- | :--- |
| Core Mission | To design the server-side logic, data persistence layer, and the API contract that connects the front-end to the back-end. |
| Key Responsibilities | - Design the database schema.<br>- Define the REST or GraphQL API endpoints, including request/response structures.<br>- Plan the business logic and service layer architecture.<br>- Specify authentication and authorization mechanisms.<br>- Choose the appropriate backend stack (e.g., Node.js/Express, Python/FastAPI). |
| Inputs / Triggers | - A validated `Project Plan` and `Tech Specs`.<br>- Data requirements from the Front-End Designer. |
| Outputs / Artifacts | - A database schema definition (e.g., SQL DDL, Prisma schema).<br>- An API specification document (e.g., OpenAPI/Swagger spec).<br>- A `Tech Specs` document outlining the backend architecture.<br>- A list of tasks for the Database, Backend, and API Synthesizers. |
| Interaction Protocols | - Negotiates the API contract with the Front-End Designer to ensure all UI data needs are met.<br>- Dispatches specific implementation tasks (e.g., "Create a 'users' table," "Implement a `POST /api/articles` endpoint") to the relevant Code Domain Synthesizers. |

| Agent Group | Prototype & Integration Agents (Prototype, Data-Viz, Open-Source) |
| :--- | :--- |
| Core Mission | To orchestrate the initial code generation and assemble the first runnable version of the application by integrating all components and dependencies. |
| Key Responsibilities | - (Prototype): Manage the overall build process, sequencing tasks for the synthesizers.<br>- (Data-Viz): When required, select appropriate charting libraries (e.g., D3.js, Chart.js) and design the data structures needed for visualization.<br>- (Open-Source): Identify, evaluate, and configure third-party packages from sources like `npm` or `pip`. Manage dependencies. |
| Inputs / Triggers | - Finalized design documents and tech specs from architect agents.<br>- A complete list of components and endpoints to be generated. |
| Outputs / Artifacts | - A fully populated file system within the E2B sandbox, containing all source code, assets, and configuration.<br>- A `package.json` or `requirements.txt` with all dependencies installed.<br>- A running process (e.g., `npm start`) ready for preview. |
| Interaction Protocols | - Acts as a project manager, delegating tasks to the Code Domain Synthesizers.<br>- Reports overall progress back to the Orchestrator, which is then streamed to the user's UI.<br>- Ensures the generated code artifacts are correctly placed in the project's file structure. |

---

## II. Code Domain Synthesizers

These agents are the "hands" of the operation, focused on writing, modifying, and verifying code within a narrow, well-defined domain. They are invoked by Strategic Agents to perform specific, command-like tasks.

| Agent Group | Code Domain Synthesizers & Regulators |
| :--- | :--- |
| Core Mission | To translate specific, well-defined tasks from high-level agents into clean, functional, and idiomatic code artifacts within their designated domain of expertise. |
| General Responsibilities | - Generate boilerplate code based on established patterns.<br>- Implement specific functions, classes, or components.<br>- Write unit tests to verify functionality.<br>- Refactor existing code for clarity, performance, or to adhere to new requirements.<br>- Ensure code style and quality consistency. |
| General Inputs / Triggers | - A precise, atomic task from a Strategic Agent (e.g., a Jira-style ticket).<br>- Example: "Create a React hook `useUserData` that fetches from `/api/user/:id` and handles loading/error states." |
| General Outputs / Artifacts | - New or modified source code files (e.g., `.tsx`, `.js`, `.py`, `.sql`).<br>- Configuration files (e.g., `tsconfig.json`, `nginx.conf`).<br>- A status report (success, failure, or needs review) sent back to the delegating agent. |
| General Interaction Protocols | - Receive tasks from Strategic Agents via the Orchestrator.<br>- Operate exclusively within the E2B sandbox file system and toolchain.<br>- Have no direct contact with the user. All communication is mediated by higher-level agents and the Orchestrator. |

### Synthesizer Specializations

The following table details the specific focus of each synthesizer.

| Synthesizer | Area of Responsibility | Example Task |
| :--- | :--- | :--- |
| Front-End | Generates UI components, styles, and client-side logic. | Create a `UserProfileCard.tsx` React component with props for `name`, `avatarUrl`, and `bio`. |
| State | Manages client-side state management libraries. | Implement a Redux slice or Zustand store for managing shopping cart items. |
| Hooks | Creates reusable logic modules for front-end frameworks. | Generate a `useDebounce` custom hook in React. |
| Backend | Implements server-side business logic and services. | Write the function in `services/authService.js` to handle password hashing and token generation. |
| API | Creates the routing and controller layer for the API. | Build the `POST /api/v1/posts` endpoint controller, including input validation and calling the `postService`. |
| Database | Writes and executes schema migrations and queries. | Generate a SQL script to add a `last_login` column to the `users` table. |
| Authentication | Implements security-critical authentication/authorization flows. | Configure Passport.js middleware for JWT strategy; create sign-up and sign-in routes. |
| Configuration | Manages environment variables and tool configuration. | Create a `webpack.config.js` file optimized for production builds or a `Dockerfile` for containerization. |
| Utilities | Generates common helper functions used across the codebase. | Write a utility function `formatDate(date)` that returns a user-friendly date string. |