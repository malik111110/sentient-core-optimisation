# Sentient Core - Technology Strategy

This document outlines the official technology stack for the Sentient Core project, with a specific focus on the "Raise Your Hack" hackathon requirements. All development should adhere to these choices to ensure consistency, interoperability, and alignment with our strategic goals.

This strategy is based on validated, up-to-date information from official documentation sources. For deeper implementation details, refer to the specific developer guides located in the `.documents/hackathon/` sub-directories.

## 1. Core Philosophy

- **Best-in-Breed Open Technologies:** We will prioritize modern, high-performance, open-source, or openly-available technologies that have strong community support and clear documentation.
- **Pragmatism over Dogma:** The chosen stack is designed to meet the specific requirements of the hackathon tracks (Vultr, Prosus, Qualcomm) while building a robust, scalable platform for the future.
- **Developer Experience:** We will use tools and frameworks that offer excellent developer experience, including strong typing, good tooling, and fast iteration cycles.

## 2. Backend Services

- **Framework:** **FastAPI** will be the Python framework for all backend services. Its high performance, async support, and automatic data validation/documentation make it ideal for building robust APIs for our agentic core.
- **Language:** Python 3.11+

## 3. Frontend & User Interface

- **Framework:** **Next.js 15** (App Router) will be used for the main web application and landing page.
- **UI Components:** We will use **Shadcn/UI** and **DaisyUI**, built on **Tailwind CSS**, to create a modern, responsive, and themeable (light/dark) user interface.
- **Language:** TypeScript

## 4. Large Language Models (LLMs)

- **Primary Cloud LLM:** **Groq** will be our primary provider for high-speed LLM inference in the cloud.
    - **Model:** We will use `llama-3.3-70b-versatile` for its advanced chat and tool-use capabilities.
- **On-Device LLM:** **Meta Llama 3** (8B and 3.2 models) will be used for on-device and edge AI scenarios.

## 5. Agent & Communication Frameworks

- **Agent Development:** **Fetch.ai uAgents** will be the primary framework for creating our individual, autonomous agents. This aligns with the decentralized ethos of the project.
- **Inter-Agent Collaboration:** **Coral Protocol** will be used as the infrastructure for inter-agent communication, discovery, and coordination.
    - **Note:** The Coral Protocol is in early development. We will use the available `coral-server` for orchestration. Client-side implementation will be based on the server's MCP tool definitions until an official Python client is released.

## 6. On-Device AI & Edge Computing (Qualcomm Track)

- **Inference Runtime:** **ONNX Runtime** will be used to run models on edge devices.
- **Execution Provider:** We will leverage the **QNN Execution Provider** for optimal performance on Qualcomm Snapdragon hardware.
- **Model Framework:** We will use **ExecuTorch** for preparing and running Llama 3 models on-device, as recommended by Meta.

## 7. Database & Storage

- **Primary Database:** **Supabase** (PostgreSQL) will be used for structured data storage, user authentication, and real-time capabilities.

## 8. Deployment & Infrastructure (Vultr Track)

- **Cloud Provider:** **Vultr** will be the target deployment platform for our core services.
- **Containerization:** **Docker** will be used to containerize the FastAPI backend and other services for consistent and portable deployments.
- **CI/CD:** A CI/CD pipeline will be established (e.g., using GitHub Actions) to automate testing and deployment to Vultr.
