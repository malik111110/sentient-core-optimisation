# WebContainer Implementation Guide

**ID:** guide:feature:webcontainer_implementation  
**Source Reference(s):** /agentic web dev/webcontainer-api-starter, /agentic web dev/webcontainer-core  
**Last Validated:** June 2025

## 1. Purpose

WebContainer enables secure execution of Node.js applications directly in the browser using WebAssembly, providing a complete development environment without server-side infrastructure.

## 2. Key Concepts

- **WebContainer**: A Node.js runtime environment running in the browser via WebAssembly
- **FileSystemTree**: Virtual file system structure for mounting code and assets
- **Process Spawning**: Ability to run npm commands and development servers within the container
- **Server-Ready Events**: Notification system for when development servers are available
- **Cross-Origin Isolation**: Required browser security model for SharedArrayBuffer support

## 3. Required Dependencies

### NPM Packages
```json
{
  "@webcontainer/api": "^1.1.3",
  "vite": "^4.1.0"
}
```

### Browser Requirements
- **SharedArrayBuffer Support**: Requires cross-origin isolation
- **HTTPS**: Required for production deployment
- **Modern Browser**: Chrome 88+, Firefox 89+, Safari 15.2+

## 4. Step-by-Step Implementation Plan

### 4.1 Environment Setup

Setting up the correct browser environment is crucial for WebContainer to function, primarily due to its reliance on `SharedArrayBuffer`.

1.  **Configure Cross-Origin Isolation Headers:**
    To enable `SharedArrayBuffer`, your server must send the following HTTP headers:
    ```
    Cross-Origin-Opener-Policy: same-origin
    Cross-Origin-Embedder-Policy: require-corp
    ```
    Alternatively, `Cross-Origin-Embedder-Policy: credentialless` can be used if you don't need to send cookies or other credentials in cross-origin requests to embedded content. Ensure these headers are correctly set on the top-level document serving your WebContainer application.

2.  **Set up HTTPS for Production Deployment:**
    Browsers typically require HTTPS for pages that are cross-origin isolated. This is a standard security practice.

3.  **Content Security Policy (CSP) (Recommended):**
    While not strictly for WebContainer's `SharedArrayBuffer`, a robust CSP is highly recommended to enhance security. Your CSP should be configured to allow loading scripts and resources necessary for WebContainer and your application, while restricting potentially malicious content. An example might include `script-src 'self' 'wasm-unsafe-eval' https://*.stackblitz.com;` but tailor this to your specific needs.

4.  **Install WebContainer API Dependency:**
    Ensure `@webcontainer/api` is added to your project's dependencies.

5.  **Create File System Structure Definition:**
    Define the initial `FileSystemTree` that WebContainer will mount on boot.

### 4.2 WebContainer Initialization
1. Import WebContainer from the API
2. Create async function to boot WebContainer instance
3. Mount virtual file system
4. Handle boot errors and fallbacks

### 4.3 File System Management
1. Define FileSystemTree structure
2. Implement file writing capabilities
3. Handle dynamic file updates
4. Manage package.json and dependencies

### 4.4 Process Management
1. Implement dependency installation (npm install)
2. Start development servers (npm run start)
3. Handle process output streaming
4. Monitor process exit codes

### 4.5 Server Integration
1. Listen for server-ready events
2. Update iframe sources for preview
3. Handle port management
4. Implement hot reload capabilities

## 5. Core Code Example

### 5.1 Basic WebContainer Setup
```typescript
import { WebContainer } from '@webcontainer/api';
import type { FileSystemTree } from '@webcontainer/api';

// Define virtual file system
const files: FileSystemTree = {
  'index.js': {
    file: {
      contents: `
import express from 'express';
const app = express();
const port = 3111;

app.get('/', (req, res) => {
  res.send('Welcome to WebContainer! 🥳');
});

app.listen(port, () => {
  console.log(\`App is live at http://localhost:\${port}\`);
});
      `,
    },
  },
  'package.json': {
    file: {
      contents: `
{
  "name": "webcontainer-app",
  "type": "module",
  "dependencies": {
    "express": "latest"
  },
  "scripts": {
    "start": "node index.js"
  }
}
      `,
    },
  },
};

let webcontainerInstance: WebContainer;

// Initialize WebContainer
async function initializeWebContainer() {
  try {
    console.log('Booting WebContainer...');
    webcontainerInstance = await WebContainer.boot();
    console.log('WebContainer booted successfully.');

    // Define event payload types (example)
    interface ServerReadyPayload {
      port: number;
      url: string;
    }

    interface ErrorPayload {
      message: string;
    }

    // Setup event listeners before mounting or spawning processes
    webcontainerInstance.on('server-ready', (port: ServerReadyPayload['port'], url: ServerReadyPayload['url']) => {
      console.log(`Server is ready on port ${port} at ${url}`);
      const iframeEl = document.querySelector('iframe');
      if (iframeEl) {
        iframeEl.src = url;
      }
    });

    webcontainerInstance.on('error', (error: ErrorPayload) => {
      console.error(`WebContainer instance error: ${error.message}`);
      // Potentially update UI to show error state
    });

    // Example: Listening for custom 'port' events if your app emits them, or other custom events
    // webcontainerInstance.on('port', (port: number, type: 'open' | 'close', url?: string) => {
    //   if (type === 'open') {
    //     console.log(`Port ${port} opened. URL (if available): ${url}`);
    //   } else {
    //     console.log(`Port ${port} closed.`);
    //   }
    // });

    console.log('Mounting files...');
    await webcontainerInstance.mount(files);
    console.log('Files mounted successfully.');

    console.log('Installing dependencies...');
    const installProcess = await webcontainerInstance.spawn('npm', ['install']);
    installProcess.output.pipeTo(new WritableStream({
      write(data) {
        console.log('Install:', data);
      }
    }));
    const installExitCode = await installProcess.exit;
    if (installExitCode !== 0) {
      throw new Error(`Installation failed with exit code ${installExitCode}`);
    }
    console.log('Dependencies installed successfully.');

    console.log('Starting the dev server...');
    const startProcess = await webcontainerInstance.spawn('npm', ['run', 'start']);
    startProcess.output.pipeTo(new WritableStream({
        write(data) {
            console.log('Dev Server:', data);
        }
    }));
    // Note: The 'server-ready' event listener above will handle iframe source update.

  } catch (error: any) {
    console.error('Failed to initialize or run WebContainer:', error.message || error);
    // Update UI to reflect the error, offer retry, etc.
  }
}

// Call the initialization function when the window loads
// window.addEventListener('load', initializeWebContainer);

// Write files dynamically
async function writeFile(path: string, content: string) {
  if (webcontainerInstance) {
    await webcontainerInstance.fs.writeFile(path, content);
  }
}

// Initialize on page load
window.addEventListener('load', initializeWebContainer);
```

### 5.2 HTML Setup with Cross-Origin Headers
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WebContainer App</title>
  
  <!-- Required for SharedArrayBuffer -->
  <meta http-equiv="Cross-Origin-Embedder-Policy" content="require-corp">
  <meta http-equiv="Cross-Origin-Opener-Policy" content="same-origin">
</head>
<body>
  <div id="app">
    <div class="editor">
      <textarea id="editor" placeholder="Edit your code here..."></textarea>
    </div>
    <div class="preview">
      <iframe id="preview"></iframe>
    </div>
  </div>
  
  <script type="module" src="/main.js"></script>
</body>
</html>
```

### 5.3 Server Configuration (for development)
```javascript
// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    headers: {
      'Cross-Origin-Embedder-Policy': 'require-corp',
      'Cross-Origin-Opener-Policy': 'same-origin',
    },
  },
  optimizeDeps: {
    exclude: ['@webcontainer/api'],
  },
});
```

## 6. Common Pitfalls & Error Handling

### 6.1 Cross-Origin Isolation Issues
- **Problem**: SharedArrayBuffer not available
- **Solution**: Ensure proper COOP/COEP headers are set
- **Detection**: Check `crossOriginIsolated` property in browser

```typescript
if (!crossOriginIsolated) {
  throw new Error('Cross-origin isolation required for WebContainer');
}
```

### 6.2 Boot Failures
- **Problem**: WebContainer.boot() fails
- **Solution**: Implement retry logic with exponential backoff
- **Fallback**: Provide alternative development environment

```typescript
async function bootWithRetry(maxRetries = 3): Promise<WebContainer> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await WebContainer.boot();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
    }
  }
  throw new Error('Failed to boot WebContainer after retries');
}
```

### 6.3 Package Installation Failures
- **Problem**: npm install fails or times out
- **Solution**: Implement timeout handling and retry logic
- **Monitoring**: Track installation progress and provide feedback

```typescript
async function installWithTimeout(timeoutMs = 30000): Promise<number> {
  const installProcess = await webcontainerInstance.spawn('npm', ['install']);
  
  return Promise.race([
    installProcess.exit,
    new Promise<number>((_, reject) => 
      setTimeout(() => reject(new Error('Installation timeout')), timeoutMs)
    )
  ]);
}
```

### 6.4 Memory Management
- **Problem**: Memory leaks in long-running sessions
- **Solution**: Implement cleanup and resource monitoring
- **Prevention**: Dispose of unused processes and file watchers

```typescript
class WebContainerManager {
  private processes: Set<any> = new Set();
  
  async cleanup() {
    for (const process of this.processes) {
      try {
        await process.kill();
      } catch (error) {
        console.warn('Failed to kill process:', error);
      }
    }
    this.processes.clear();
  }
}
```

## 7. Performance Optimization

### 7.1 File System Optimization
- Use batch operations for multiple file writes
- Implement file change debouncing
- Cache frequently accessed files

### 7.2 Process Management
- Reuse existing processes when possible
- Implement process pooling for common tasks
- Monitor resource usage and implement limits

### 7.3 Network Optimization
- Preload common packages
- Implement package caching strategies
- Use CDN for static assets

## 8. Security Considerations

### 8.1 Sandboxing
- WebContainer provides built-in sandboxing
- No access to host file system
- Network access is controlled

### 8.2 Code Execution
- All code runs in isolated environment
- No access to sensitive browser APIs
- Process resource limits enforced

### 8.3 Content Security Policy
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self' 'unsafe-eval'; worker-src 'self' blob:;">
```

## 9. Integration with Genesis Engine

### 9.1 Agent Integration
- Frontend Agent uses WebContainer for live preview
- Backend Agent can test API endpoints
- Testing Agent runs automated tests in container

### 9.2 State Management
- Sync WebContainer state with application state
- Persist file changes across sessions
- Handle collaborative editing scenarios

### 9.3 Monitoring and Analytics
- Track container performance metrics
- Monitor resource usage patterns
- Collect user interaction data

---

*Implementation Status: Ready for Genesis Engine integration*  
*Next Steps: Integrate with multi-agent architecture and implement collaborative features*