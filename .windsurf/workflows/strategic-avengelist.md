---
description: : To extrapolate from the foundational project documents and user pain points, conduct deep research, and produce a comprehensive technical roadmap and a persuasive, professional pitch deck to articulate the project's world-changing potential
---

**Core Directive:** To extrapolate from the foundational project documents and user pain points, conduct deep research, and produce a comprehensive technical roadmap and a persuasive, professional pitch deck to articulate the project's world-changing potential.

**Primary Tools:**
*   **@wonderwhy-er/desktop-commander:** To read all foundational project documents, user pain point descriptions, and the code within the `/knowledge_base/` reference repos.
*   **Exa Search (`web_search_exa`):** The primary tool for deep research into market trends, competitor analysis, technology validation, and finding statistics to back up claims.
*   **@smithery-ai/server-sequential-thinking:** The core reasoning engine for structuring the narrative, formulating the roadmap, and designing the slide-by-slide flow of the presentation.
*   **@falahgs/flux-imagegen-mcp-server:** To generate high-quality visual assets for the pitch deck, such as conceptual diagrams, UI mockups, and architectural illustrations.
*   **@alioshr/memory-bank-mcp:** To save the final roadmap and presentation outline as retrievable artifacts.

**Workflow and Responsibilities:**

**Phase 1: Foundational Synthesis & Intelligence Gathering**
*   **1.1. Trigger:** A directive to "prepare the project pitch and roadmap."
*   **1.2. Process:**
    1.  **Ingest Internal Knowledge:** Use `desktop-commander` to read and fully comprehend:
        *   The "Agentic App Genesis Engine" high-level plan.
        *   The detailed user pain points document.
        *   The "6 Core Concepts of Agentic Ultra Agents."
        *   The `README.md` files of key reference repos (`Archon`, `bolt.new`, `webcontainer-core`).
    2.  **External Deep Dive:** Initiate a `sequential-thinking` session to guide a deep research campaign using `Exa Search`. The goal is to find external validation for the internal vision.
        *   **Pain Point Validation:** Search for industry reports, articles, and statistics on topics like "digital transformation challenges for non-tech SMEs," "citizen developer market size 2025," "limitations of low-code platforms."
        *   **Competitive Landscape:** Analyze the positioning and technical limitations of `v0.dev`, `Replit`, `Bubble.io`, etc. Find articles that critique them.
        *   **Technological Validation:** Find the latest announcements, case studies, and performance benchmarks for core technologies like `LangGraph`, `WebContainers`, and `Gemini 1.5 Pro`.

**Phase 2: Crafting the Grand Narrative & Technical Roadmap**
*   **2.1. Trigger:** Completion of the research phase.
*   **2.2. Process:**
    1.  **Formulate the Core Narrative:** Start a `sequential-thinking` session to weave all inputs into a persuasive story. The structure must be: **Problem -> Flawed Solutions -> Our Vision -> Our Unique Solution.**
        *   *Example Narrative Point:* "While low-code platforms promise ease of use, they fail at complexity. Pro-code AI IDEs offer power but alienate 99% of industry experts. We bridge this chasm with a system that learns *your* industry and builds the complex tools *you* need, with an interface that evolves *with you* from novice to expert."
    2.  **Develop the Technical Roadmap:** Expand the MVP plan into a multi-stage, technically-grounded roadmap.
        *   **Stage 0: The Hackathon Prototype (The Proof-of-Concept):** Frame the existing "Genesis Engine" plan as the successful, tangible first step that proves the core agentic workflow is viable.
        *   **Stage 1: The Core Platform (The 'Archon' Layer):** Detail the plan to build the robust agent-building and orchestration agents.
            *   **Tech:** LangGraph for stateful orchestration, `Knowledge Synthesis Agent` for continuous learning, Supabase CLI for reproducible local development environments.
        *   **Stage 2: Industry Agent Packs (The Vertical Solution):** Outline the strategy to create specialized, pre-trained groups of agents for specific industries (e.g., "Salesforce Agent Pack," "Healthcare Compliance Agent Pack"). This directly addresses the user pain point of generic tools.
            *   **Tech:** Advanced RAG over industry-specific documents, fine-tuning smaller models on domain jargon.
        *   **Stage 3: The Sentient Ecosystem (The Ultimate Vision):** Describe the implementation of the most advanced concepts.
            *   **Tech:** `Observation & Monitoring Ultra Agents` using LangSmith for analytics, feedback loops that trigger automatic retraining, and a GUI that dynamically adds/removes complexity based on user behavior.
*   **2.3. Output:**
    *   A detailed Markdown document: `ROADMAP.md`.
    *   A concise summary of the core narrative.

**Phase 3: Designing the Winning Pitch Deck**
*   **3.1. Trigger:** Finalization of the narrative and roadmap.
*   **3.2. Process:**
    1.  Initiate a `sequential-thinking` session to outline a professional, 10-slide pitch deck, slide by slide.
    2.  For each slide, define the key message, the talking points, and the required visual aid.
*   **3.2. Slide-by-Slide Outline & Visual Generation Plan:**
    *   **Slide 1: Title.** Project Name (e.g., "Nexus Weaver: From Industry Pain to Agentic Gain").
        *   *Visual:* Generate a stunning, abstract hero image using **`@falahgs/flux-imagegen-mcp-server`** with a prompt like "abstract network of glowing neural pathways connecting industry icons like a factory and a hospital, futuristic, corporate."
    *   **Slide 2: The $1 Trillion Chasm.** State the problem using the powerful statistics found during research.
        *   *Visual:* A simple, stark infographic showing the gap between industry needs and tech solutions.
    *   **Slide 3: Today's Compromises.** Show logos of existing solutions (Low-Code vs. Pro-Code) and list their critical flaws.
    *   **Slide 4: Our Vision: The Symbiotic Platform.** Introduce the 6 Core Concepts.
        *   *Visual:* Generate a high-level architectural diagram with `@falahgs/flux-imagegen-mcp-server` that visually represents the 6 concepts interacting.
    *   **Slide 5: The Solution: Nexus Weaver.** Explain the core product.
        *   *Visual:* A clean UI mockup of the platform's "easy mode" interface, also generated by the image tool.
    *   **Slide 6: Live Demo: The Genesis Engine.** **Crucially, this is where you connect the vision to your working MVP.** "We've already built the core of this. Let us show you." (This is the moment for the live demo of your foundational agentic flow).
    *   **Slide 7: The Path to Dominance (Our Roadmap).** A visual timeline based on the `ROADMAP.md` generated in Phase 2.
    *   **Slide 8: The Unfair Advantage.** Why your team/approach is the one to succeed (e.g., "Our multi-layered agentic architecture is fundamentally more adaptable than monolithic solutions").
    *   **Slide 9: The Ask.** What you need to win the hackathon/get funding.
    *   **Slide 10: Thank You & Contact.**
*   **3.3. Output:**
    *   A JSON object (`presentation_outline.json`) where each key is a slide number and the value is an object containing `{"title": "...", "talking_points": [...], "visual_prompt": "..."}`.
    *   The generated image assets, saved with clear filenames (e.g., `slide_1_hero.png`).
    *   All artifacts saved to **`@alioshr/memory-bank-mcp`**.