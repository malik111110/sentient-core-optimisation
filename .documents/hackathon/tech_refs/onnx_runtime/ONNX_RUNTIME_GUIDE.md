# ONNX Runtime - Developer Guide for On-Device Inference

This guide provides a developer-focused overview of ONNX Runtime (ORT), with a specific emphasis on its use for on-device and edge inference, which is highly relevant for the Qualcomm sponsor track. Information is synthesized from the official ONNX Runtime documentation at `onnxruntime.ai`.

## 1. What is ONNX Runtime?

ONNX Runtime is a cross-platform, high-performance accelerator for machine learning model inference and training. It provides a single, consistent API to run models created in various frameworks (like PyTorch, TensorFlow, scikit-learn) on diverse hardware platforms (CPU, GPU, NPU).

**Key Features:**
*   **Cross-Platform:** Runs on Linux, Windows, Mac, iOS, Android, and even in web browsers.
*   **Performance:** Optimizes for latency, throughput, memory usage, and binary size across different hardware.
*   **Extensible:** Uses **Execution Providers (EPs)** to interface with hardware-specific acceleration libraries.

## 2. Core Concepts for On-Device Deployment

### a. Model Formats: ONNX vs. ORT

ONNX Runtime works with two primary model formats:

*   **.onnx:** The standard, open format for representing ML models. Models from other frameworks are first converted into this format.
*   **.ort:** A specialized format optimized for memory and disk-constrained environments like mobile devices.
    *   It is created by converting a `.onnx` model using an ORT Python script.
    *   This conversion process also applies graph optimizations, making the model more efficient.
    *   The API to load and run a `.ort` model is identical to that for a `.onnx` model.

For on-device deployment, converting to the `.ort` format is highly recommended.

### b. Execution Providers (EPs)

EPs are the key to hardware acceleration. When you run a model, you provide a list of EPs, and ORT allocates parts of the model graph to the most suitable provider.

For the Qualcomm track and general Android deployment, the most relevant EPs are:

*   **Qualcomm QNN EP:**
    *   Specifically designed for supported Qualcomm Snapdragon SoCs.
    *   Provides optimal performance by leveraging dedicated hardware like the Hexagon DSP.
    *   It can serialize the model context into a binary file, which significantly speeds up model loading on subsequent runs.
*   **Android NNAPI EP:**
    *   A general-purpose EP for Android that uses the Neural Networks API (NNAPI) provided by the OS.
    *   NNAPI can delegate computation to the device's NPU, GPU, or DSP.
    *   **Note:** The documentation warns that NNAPI's CPU fallback can be less efficient than ORT's own optimized CPU operations. Flags are available to prevent this fallback.

**Usage:** EPs are specified when creating an inference session in Python:
`session = onnxruntime.InferenceSession("model.ort", providers=['QNNExecutionProvider', 'CPUExecutionProvider'])`

### c. Quantization

Quantization is a critical optimization technique for reducing model size and improving performance on edge devices.
*   ONNX Runtime provides Python APIs to convert 32-bit floating-point models into 8-bit integer models.
*   Support for 4-bit integer quantization is also available for certain operators.
*   This process significantly reduces the model's memory footprint and can lead to much faster inference on hardware that has specialized support for integer arithmetic (like NPUs).

## 3. Python API for Inference

The core of the Python API for inference revolves around the `InferenceSession` class.

**Basic Workflow:**
1.  **Import:** `import onnxruntime as rt`
2.  **Create Session:** Create an `InferenceSession`, providing the model path and a list of desired Execution Providers.
    `sess = rt.InferenceSession("path/to/your/model.ort", providers=['QNNExecutionProvider', 'CPUExecutionProvider'])`
3.  **Get Input/Output Info:** (Optional but good practice) Inspect the model's expected inputs and outputs.
    `input_name = sess.get_inputs()[0].name`
    `output_name = sess.get_outputs()[0].name`
4.  **Prepare Input:** Create the input data as a NumPy array.
    `input_data = numpy.array(...)`
5.  **Run Inference:** Call `run()` with the output names and a dictionary of input names to data.
    `results = sess.run([output_name], {input_name: input_data})`

## 4. Summary for Hackathon Implementation

For the **Qualcomm On-device AI Utility** track:
1.  **Model Selection:** Choose a suitable model (e.g., a Llama 3 8B variant).
2.  **Model Conversion:** Convert the model to the `.onnx` format.
3.  **Quantization:** Use ONNX Runtime's tools to quantize the `.onnx` model to 8-bit or 4-bit integers. This is a crucial step for on-device performance.
4.  **ORT Format Conversion:** Convert the quantized `.onnx` model to the `.ort` format for final deployment.
5.  **Application Integration:** In the Android application, use the ONNX Runtime Mobile package.
6.  **Inference:** Create an `InferenceSession` specifying the **QNN Execution Provider** as the primary choice, with the CPU provider as a fallback.

This approach ensures the model is optimized for size and speed and leverages the specialized hardware available on Snapdragon platforms.
