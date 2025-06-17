# WebContainer Integration Guide

**ID:** guide:feature:webcontainer_integration
**Source Reference(s):** /agentic web dev/webcontainer-api-starter, /agentic web dev/webcontainer-core
**Last Validated:** June 2025

## 1. Purpose

WebContainer enables secure execution of Node.js applications directly in the browser using WebAssembly, providing a complete development environment without server-side infrastructure. This guide covers foundational implementation and advanced usage patterns.

## 2. Key Concepts

- **WebContainer**: A Node.js runtime environment running in the browser via WebAssembly.
- **FileSystemTree**: Virtual file system structure for mounting code and assets.
- **Process Spawning**: Ability to run npm commands and development servers within the container.
- **Server-Ready Events**: Notification system for when development servers are available.
- **Cross-Origin Isolation**: Required browser security model for SharedArrayBuffer support.

## 3. Required Dependencies

### NPM Packages
```json
{
  "@webcontainer/api": "^1.1.3",
  "vite": "^4.1.0" 
}
```

### Browser Requirements
- **SharedArrayBuffer Support**: Requires cross-origin isolation.
- **HTTPS**: Required for production deployment.
- **Modern Browser**: Chrome 88+, Firefox 89+, Safari 15.2+

## 4. Step-by-Step Implementation Plan

### 4.1. Environment Setup

Setting up the correct browser environment is crucial for WebContainer to function, primarily due to its reliance on `SharedArrayBuffer`.

1.  **Configure Cross-Origin Isolation Headers:**
    Your server must send:
    ```
    Cross-Origin-Opener-Policy: same-origin
    Cross-Origin-Embedder-Policy: require-corp
    ```
    (Alternatively, `Cross-Origin-Embedder-Policy: credentialless`)

2.  **Set up HTTPS for Production Deployment.**

### 4.2. Initialize WebContainer

```typescript
import { WebContainer } from '@webcontainer/api';

let webcontainerInstance: WebContainer;

async function initializeWebContainer() {
  if (!webcontainerInstance) {
    webcontainerInstance = await WebContainer.boot();
  }
  return webcontainerInstance;
}

// Call this function when your application loads
initializeWebContainer().then(() => {
  console.log('WebContainer booted successfully!');
  // Proceed with mounting files and running commands
}).catch(error => {
  console.error('Failed to boot WebContainer:', error);
});
```

### 4.3. File System Operations

- **Mounting Files and Directories:**
  ```typescript
  const files = {
    'index.js': {
      file: {
        contents: 'console.log("Hello from WebContainer!");',
      },
    },
    'package.json': {
      file: {
        contents: `{
          "name": "my-app",
          "type": "module",
          "dependencies": {
            "express": "latest"
          },
          "scripts": {
            "start": "node index.js"
          }
        }`,
      },
    },
  };
  await webcontainerInstance.mount(files);
  ```

- **Writing Files Dynamically:**
  ```typescript
  await webcontainerInstance.fs.writeFile('newFile.js', 'console.log("Newly created file!");');
  ```

- **Reading Files:**
  ```typescript
  const content = await webcontainerInstance.fs.readFile('package.json', 'utf-8');
  ```

### 4.4. Running Processes (npm commands, dev servers)

- **Installing Dependencies:**
  ```typescript
  const installProcess = await webcontainerInstance.spawn('npm', ['install']);
  installProcess.output.pipeTo(new WritableStream({
    write(data) {
      console.log('npm install:', data);
    }
  }));
  const exitCode = await installProcess.exit;
  if (exitCode !== 0) {
    throw new Error('npm install failed');
  }
  ```

- **Running a Development Server:**
  ```typescript
  const serverProcess = await webcontainerInstance.spawn('npm', ['run', 'start']); // Assumes 'start' script in package.json
  serverProcess.output.pipeTo(new WritableStream({
    write(data) {
      console.log('Server output:', data);
    }
  }));

  webcontainerInstance.on('server-ready', (port, url) => {
    console.log(`Server ready at ${url} on port ${port}`);
    // Update iframe src or provide link to user
    // e.g., iframeElement.src = url;
  });
  ```

## 5. Advanced Usage & Performance Optimization

### 5.1. Lazy Loading & Code Splitting
- Use dynamic `import()` within your WebContainer application.
- Mount or write files to the WebContainer's file system on demand.
- Benefit: Faster initial boot times, reduced memory footprint.

### 5.2. Efficient File System Operations
- **Batch Operations:** Use `webcontainerInstance.mount()` with a nested directory object for multiple files.
- **Avoid Unnecessary Reads/Writes:** Cache frequently accessed file contents in JavaScript memory.

### 5.3. Managing Multiple Processes
- Keep track of spawned processes and kill them when no longer needed to free resources.
  ```typescript
  const devServer = await webcontainerInstance.spawn('npm', ['run', 'dev']);
  // ... later
  await devServer.kill();
  ```

### 5.4. Inter-Process Communication (IPC)
- WebContainers do not support traditional Node.js IPC mechanisms like `process.send()` directly between a WebContainer process and the main browser thread.
- Communication typically happens via: Events (`server-ready`, `port`), `ReadableStream` / `WritableStream` for process I/O, or by reading/writing to the shared file system.

### 5.5. Handling Large Files & Binary Data
- Use `Uint8Array` for binary content when writing files.
- Be mindful of browser memory limits when dealing with very large files.

## 6. Error Handling and Debugging

- **Process Exit Codes:** Check `await process.exit` for non-zero values.
- **Runtime Errors:** Listen to the `error` event on `webcontainerInstance`.
  ```javascript
  webcontainerInstance.on('error', (error) => {
    console.error('WebContainer runtime error:', error.message);
  });
  ```
- **Debugging Node.js Apps:** Primarily `console.log` debugging. Complex debugging might require custom tooling.

## 7. Security Considerations

- **Sandboxing:** WebContainer provides built-in sandboxing. No direct access to host file system or sensitive browser APIs.
- **Content Security Policy (CSP):**
  ```html
  <meta http-equiv="Content-Security-Policy" 
        content="default-src 'self'; script-src 'self' 'unsafe-eval'; worker-src 'self' blob:;">
  ```
  (Adjust `'unsafe-eval'` if possible, though WebContainer might require it for its initial setup or certain dynamic code executions).

## 8. Use Cases in Sentient Core

- **Agent Tooling:** Safely execute user-provided code snippets for validation or simple transformations.
- **Interactive Tutorials/Code Sandboxes:** Provide live coding environments.
- **Ephemeral Development Environments:** Quickly scaffold and run small projects or test library integrations.
- **Client-Side Build Processes:** Simple build steps (bundling, transpiling) could run client-side.

## 9. Conclusion

WebContainers offer a paradigm shift for running Node.js applications client-side. By understanding and applying these techniques, developers can build highly performant, robust, and feature-rich experiences. Continuous experimentation and attention to browser limitations and security best practices are key.
