# Qualcomm Track Action Plan: Edge AI Utility

**Version:** 2.0 (Epic/Story Aligned)
**Date:** June 18, 2025
**Status:** In Refactoring
**Parent Epic:** EPIC-QUALCOMM (Develop On-Device Edge AI Utility Generator)
**Related Task Breakdown:** [../../../01_PROJECT_PLANNING/01_04_task_breakdown.md#EPIC-QUALCOMM](README.md)

---

## 1. Objective

To design and build a practical, high-performance Edge AI utility that runs entirely on-device, leveraging the power of Snapdragon hardware. This plan details the steps to meet the Qualcomm sponsor track requirements, focusing on offline-first capabilities and efficient on-device inference, organized by stories under EPIC-QUALCOMM.

## 2. Stories & Detailed Tasks

### STORY-QUALCOMM-1: Research & Select On-Device AI Model
-   **Description:** Identify suitable small, efficient model (e.g., text summarizer, code snippet generator) convertible to ONNX.
-   **Assigned:** AGENT-RESEARCH / AGENT-AI
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Qual-1.1:** Define criteria for model selection (size, performance, task suitability for an edge utility, ONNX compatibility, existing pre-trained versions).
        -   *Acceptance Criteria:* Clear selection criteria documented.
    -   **Task-Qual-1.2:** Research and shortlist potential models (e.g., from Hugging Face: DistilBERT variants, MobileBERT, small T5 variants, or specialized models for chosen utility).
        -   *Acceptance Criteria:* List of 3-5 candidate models with pros/cons.
        -   *References:* `../../../02_HACKATHON_CENTRAL/02_06_TECHNOLOGY_GUIDES/02_06_05_llama3_model_guide.md` (for context on model characteristics, though Llama3 itself might be too large for initial utility).
    -   **Task-Qual-1.3:** Select the primary model for the Edge AI utility.
        -   *Acceptance Criteria:* Final model selected and justification documented.
    -   **Task-Qual-1.4:** Research ONNX Runtime specifics for on-device deployment, including the Qualcomm QNN Execution Provider.
        -   *Acceptance Criteria:* Understanding of model conversion, quantization, and QNN EP usage is documented.
        -   *References:* `../../../02_HACKATHON_CENTRAL/02_06_TECHNOLOGY_GUIDES/02_06_08_onnx_runtime_guide.md`.

### STORY-QUALCOMM-2: Convert & Optimize Model for On-Device Inference
-   **Description:** Convert to ONNX, quantize to `.ort` format for QNN Execution Provider.
-   **Assigned:** AGENT-AI
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Qual-2.1:** Obtain the pre-trained selected model (e.g., download from Hugging Face).
        -   *Acceptance Criteria:* Model files are locally available.
    -   **Task-Qual-2.2:** Convert the model to ONNX format using appropriate tools (e.g., `torch.onnx.export`, `tf2onnx`).
        -   *Acceptance Criteria:* `.onnx` model file is generated and passes basic validation.
    -   **Task-Qual-2.3:** Apply quantization (e.g., 8-bit static or dynamic) to the ONNX model to reduce size and improve inference speed.
        -   *Acceptance Criteria:* Quantized ONNX model is generated.
    -   **Task-Qual-2.4:** Convert the quantized ONNX model to the `.ort` format, optimized for ONNX Runtime.
        -   *Acceptance Criteria:* `.ort` model file is generated.
    -   **Task-Qual-2.5:** Test the `.ort` model with ONNX Runtime on a development machine (CPU first) to ensure correctness.
        -   *Acceptance Criteria:* Model loads and produces expected outputs.
    -   **References:** `../../../02_HACKATHON_CENTRAL/02_06_TECHNOLOGY_GUIDES/02_06_08_onnx_runtime_guide.md`.

### STORY-QUALCOMM-3: Develop "Edge AI Utility" Application
-   **Description:** Python app, ONNX Runtime integration, simple UI (Tkinter/web).
-   **Assigned:** AGENT-BACKEND / AGENT-FRONTEND (if web UI)
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Qual-3.1:** Define the specific functionality and user interface for the chosen utility (e.g., "Offline Text Summarizer," "On-Device Code Formatter").
        -   *Acceptance Criteria:* Utility specification and basic UI wireframes are complete.
    -   **Task-Qual-3.2:** Develop the core Python application logic for the utility.
        -   *Acceptance Criteria:* Core functionality (without AI model yet) is implemented.
    -   **Task-Qual-3.3:** Integrate ONNX Runtime into the Python application to load and run the `.ort` model.
        -   *Details:* Implement inference session creation, input preprocessing, model execution, and output postprocessing.
        -   *Acceptance Criteria:* Application can successfully perform inference using the model.
    -   **Task-Qual-3.4:** Configure the application to use the Qualcomm QNN Execution Provider. Include fallbacks to CPU EP if QNN is unavailable.
        -   *Acceptance Criteria:* Application attempts to use QNN EP first.
    -   **Task-Qual-3.5:** Develop a simple user interface for the utility.
        -   *Options:* Tkinter for a native desktop feel, or a very lightweight local web server (e.g., Flask/FastAPI with minimal HTML/JS) if a browser-based UI is preferred.
        -   *Acceptance Criteria:* UI allows user input and displays model output.
    -   **Task-Qual-3.6:** Package the application and model for easy distribution/testing (e.g., as a standalone script with dependencies, or a simple installer).
        -   *Acceptance Criteria:* Application can be run on a target-like environment.

### STORY-QUALCOMM-4: Test & Benchmark Utility on Snapdragon Hardware (Simulated/Actual)
-   **Description:** Performance testing, QNN EP validation.
-   **Assigned:** AGENT-AI / AGENT-DEVOPS
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Qual-4.1:** If actual Snapdragon X Elite hardware is unavailable, set up a development environment that best simulates it (e.g., ARM64 VM, or focus on cross-platform ONNX Runtime testing).
        -   *Acceptance Criteria:* Test environment is ready.
    -   **Task-Qual-4.2:** Deploy and run the Edge AI utility on the test environment.
        -   *Acceptance Criteria:* Utility runs successfully.
    -   **Task-Qual-4.3:** Verify that the Qualcomm QNN Execution Provider is being utilized (check logs or use ONNX Runtime APIs if available).
        -   *Acceptance Criteria:* QNN EP usage confirmed.
    -   **Task-Qual-4.4:** Perform basic performance benchmarking (e.g., inference latency, resource usage).
        -   *Acceptance Criteria:* Performance metrics are recorded.
    -   **Task-Qual-4.5:** Identify any performance bottlenecks or issues and attempt to optimize.
        -   *Acceptance Criteria:* Optimization efforts are documented.

### STORY-QUALCOMM-5: Prepare Qualcomm Track Demo Script & Assets
-   **Description:** Finalize demo flow and materials for Qualcomm presentation.
-   **Assigned:** AGENT-STRATEGIC-EVANGELIST / AGENT-ARCHITECT
-   **Status:** To Do
-   **Detailed Tasks:**
    -   **Task-Qual-5.1:** Outline the demo flow, highlighting the on-device nature, offline capability, and performance of the Edge AI utility.
        -   *Acceptance Criteria:* Clear, concise demo script is drafted.
    -   **Task-Qual-5.2:** Emphasize how Sentient Core's architecture facilitates the creation of such edge utilities (even if the generator itself is a future concept).
        -   *Acceptance Criteria:* Demo narrative connects to Sentient Core.
    -   **Task-Qual-5.3:** Create any necessary visual aids or presentation slides.
        -   *Acceptance Criteria:* Supporting materials are ready.
    -   **Task-Qual-5.4:** Rehearse the demo multiple times.
        -   *Acceptance Criteria:* Demo can be delivered confidently.
    -   **Task-Qual-5.5:** Record a video walkthrough of the Edge AI utility in action.
        -   *Acceptance Criteria:* High-quality video demo is produced.

---

## 3. Success Criteria for Qualcomm Track

- A functional Edge AI utility is created that runs entirely offline on a target device/environment.
- The utility uses a quantized ONNX model (`.ort`) for efficient on-device inference.
- The application is configured to attempt leveraging the Qualcomm QNN Execution Provider.
- The solution effectively demonstrates the potential of on-device AI on Snapdragon hardware (or simulated environment).
- The demo clearly articulates the benefits of on-device AI and its connection to the broader Sentient Core vision.
- All Qualcomm track requirements from the `02_02_raise_your_hack_overview.md` are met.
