# On-Device AI Model Feasibility Study

**Version:** 1.0
**Date:** June 19, 2025
**Status:** Completed

## 1. Objective

This document summarizes the research conducted to identify suitable, high-performance, on-device AI models for the core functionalities of the Sentient-Core hackathon demo. The primary requirements were open-source availability, strong performance, low resource footprint, and compatibility with the ONNX Runtime for deployment on Windows (specifically on Snapdragon hardware).

## 2. Key Areas of Research

1.  **Speech-to-Text (STT):** For processing the initial voice command that activates the agentic factory.
2.  **Language Model (LLM):** For on-device summarization and Q&A capabilities within the generated "PharmaPulse" application, and potentially for use by agents in the factory.

## 3. Findings & Selected Models

### 3.1. Speech-to-Text (STT)

*   **Selected Model:** **`sherpa-onnx`**
*   **Repository:** [https://github.com/k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)
*   **Rationale:**
    *   **Optimized for ONNX:** It is purpose-built for high-performance, offline inference using the ONNX Runtime.
    *   **Cross-Platform:** Officially supports Windows, Linux, macOS, Android, and iOS, making it a perfect fit for our Qualcomm track demonstration.
    *   **Lightweight & Performant:** Designed for embedded systems and edge devices, ensuring it will run efficiently on the Snapdragon X Elite.
    *   **Feature-Rich:** Includes VAD (Voice Activity Detection), which is crucial for a smooth voice command experience.

### 3.2. Language Model (LLM)

*   **Selected Model:** **Microsoft Phi-3**
*   **Repository:** [https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-onnx](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-onnx)
*   **Rationale:**
    *   **State-of-the-Art Small LLM:** Phi-3 offers performance comparable to models 10x its size, making it ideal for on-device deployment without significant compromise.
    *   **Official ONNX Support:** Microsoft provides officially optimized ONNX models, ensuring seamless integration with ONNX Runtime and DirectML on Windows.
    *   **Quantization:** Availability of `int4` quantized versions is critical for minimizing memory footprint and maximizing performance on the Snapdragon NPU.
    *   **Strong Corporate Backing:** As a Microsoft model, it has a credible and well-supported ecosystem, which strengthens our technical narrative.

## 4. Conclusion

This research confirms the technical feasibility of our proposed demo. The selection of `sherpa-onnx` for STT and `Phi-3` for LLM tasks provides a robust, high-performance, and credible foundation for building a compelling on-device AI experience. These choices directly support our primary Prosus track goal and our supporting Qualcomm track narrative.