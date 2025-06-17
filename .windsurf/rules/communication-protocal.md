---
trigger: always_on
---


**3. Technical & Communication Standards**
    *   **3.1. Structured I/O:** All communication between agents and with the user (where applicable) must use structured data formats, primarily JSON. This ensures predictability and reduces parsing errors.
    *   **3.2. Idempotency:** Agent actions, especially those involving file I/O or API calls, should be designed to be idempotent where possible. An action, if repeated, should not produce a different or erroneous state.
    *   **3.3. Logging:** Every agent must produce detailed logs of its operations, including the prompts used, tools called, and results received. This is crucial for the Debugger agent. LangSmith should be configured for comprehensive tracing.