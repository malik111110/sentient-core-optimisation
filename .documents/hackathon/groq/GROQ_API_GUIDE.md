# Groq API - Developer Guide (Python)

This guide provides a summary of how to use the Groq API with Python, based on information from the official Groq API Cookbook. Groq provides access to Large Language Models (LLMs) with a focus on high-speed inference.

## 1. Installation

Install the official Groq Python library:

```bash
pip install groq
```

## 2. Authentication

The Groq API uses API keys for authentication.

*   **Set Environment Variable:** The recommended way is to set the `GROQ_API_KEY` environment variable.
    ```bash
    export GROQ_API_KEY="YOUR_GROQ_API_KEY_HERE"
    ```
*   **Streamlit:** If using Streamlit, you can store it in `.streamlit/secrets.toml`:
    ```toml
    # .streamlit/secrets.toml
    GROQ_API_KEY="your_groq_api_key_here"
    ```

## 3. Client Initialization

Import the library and initialize the client:

```python
import os
from groq import Groq

# Retrieve the API key from environment variables
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

client = Groq(api_key=api_key)
```

## 4. Chat Completions

This is the primary way to interact with the models.

### Basic Chat Completion

```python
try:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of low-latency LLM inference.",
            }
        ],
        model="mixtral-8x7b-32768", # Or other available models like llama2-70b-4096
    )
    print(chat_completion.choices[0].message.content)
except Exception as e:
    print(f"An error occurred: {e}")
```

### Available Models (Examples from Docs)

*   `mixtral-8x7b-32768`
*   `llama2-70b-4096`
*   `gemma-7b-it`
*(Always check Groq's official documentation for the latest list of supported models.)*

### Streaming Chat Completions

For real-time responses:

```python
try:
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Write a short story about an AI exploring the internet for the first time.",
            }
        ],
        model="mixtral-8x7b-32768",
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="")
    print() # Newline at the end
except Exception as e:
    print(f"An error occurred during streaming: {e}")
```

## 5. Advanced Features (Overview)

The Groq API and its cookbook demonstrate several advanced capabilities:

*   **Function Calling / Tool Use:**
    *   The API supports defining tools (functions) that the LLM can choose to call.
    *   This enables the LLM to interact with external systems or data sources.
    *   JSON mode can be used to ensure the LLM outputs valid JSON for tool arguments.
    *   Examples include generating SQL queries based on natural language.

*   **Content Moderation (Llama Guard 3):**
    *   You can use models like Llama Guard 3 via the Groq API to screen user inputs or LLM outputs for harmful content across various categories.
    *   This involves making a chat completion request to the moderation model.

*   **RAG (Retrieval Augmented Generation):**
    *   The cookbook provides examples of implementing RAG pipelines, where relevant context is fetched from a knowledge base (e.g., presidential speeches, financial documents) and provided to the LLM to generate more informed responses.

*   **Integrations:**
    *   **LangChain:** Seamless integration with LangChain for building complex LLM applications.
    *   **Streamlit:** Examples for creating interactive web demos.
    *   **Replit:** Ready-to-use examples on Replit.

## 6. Key Considerations

*   **API Key Security:** Always protect your API key. Do not hardcode it directly into your source code. Use environment variables or secure secret management.
*   **Model Selection:** Choose the model that best suits your task's complexity, context window requirements, and desired output quality. Refer to Groq's documentation for the latest model offerings and their capabilities.
*   **Error Handling:** Implement robust error handling to manage API errors, network issues, or unexpected responses.
*   **Rate Limits:** Be aware of any API rate limits and implement retry mechanisms if necessary. (Details typically found in API documentation).

This guide should serve as a starting point. For more detailed examples, specific use cases, and the latest updates, always refer to the [official Groq API Cookbook](https://github.com/groq/groq-api-cookbook) and Groq Cloud documentation.
