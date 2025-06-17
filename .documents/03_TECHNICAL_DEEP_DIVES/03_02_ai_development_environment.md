# AI Development Environment Guide

**ID:** guide:feature:ai_development_environment  
**Source Reference(s):** /agentic web dev/bolt.new  
**Last Validated:** January 2025

## 1. Purpose

Implement a comprehensive AI-powered development environment that combines chat interfaces, real-time code generation, WebContainer execution, and artifact management for seamless AI-assisted software development.

## 2. Key Concepts

- **AI Chat Interface**: Conversational UI for natural language programming
- **Streaming Responses**: Real-time AI output with `streamText` and `useChat`
- **Artifact Management**: Version-controlled code artifacts with preview capabilities
- **WebContainer Integration**: Secure browser-based code execution environment
- **Hot Module Replacement (HMR)**: Real-time code updates and preview
- **State Management**: Centralized application state with stores and context
- **Component Architecture**: Modular React components with TypeScript

## 3. Required Dependencies

### Frontend Dependencies
```json
{
  "dependencies": {
    "@ai-sdk/anthropic": "^0.0.39",
    "@ai-sdk/openai": "^0.0.42",
    "@ai-sdk/google": "^0.0.37",
    "@remix-run/node": "^2.8.1",
    "@remix-run/react": "^2.8.1",
    "@remix-run/serve": "^2.8.1",
    "@stackblitz/webcontainer-core": "^1.3.0",
    "ai": "^3.1.12",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "nanostores": "^0.9.5",
    "@nanostores/react": "^0.7.1",
    "framer-motion": "^11.0.0",
    "lucide-react": "^0.263.1",
    "monaco-editor": "^0.44.0",
    "@monaco-editor/react": "^4.6.0",
    "xterm": "^5.3.0",
    "@xterm/addon-fit": "^0.8.0",
    "diff": "^5.1.0",
    "which-pm-runs": "^1.1.0",
    "file-saver": "^2.0.5"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.1.0",
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

### Environment Variables
```bash
# AI Provider Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_GENERATIVE_AI_API_KEY=your_google_key

# Application Configuration
VITE_LOG_LEVEL=debug
VITE_ALLOW_ANALYTICS=false
VITE_ENABLE_WEBCONTAINER=true

# Development Configuration
NODE_ENV=development
VITE_DEV_SERVER_PORT=5173
VITE_PREVIEW_PORT=4173
```

## 4. Step-by-Step Implementation Plan

### 4.1 Project Structure Setup
1. Initialize Remix application with TypeScript
2. Configure Vite for optimal development experience
3. Set up Tailwind CSS for styling
4. Configure Monaco Editor for code editing
5. Set up WebContainer integration

### 4.2 AI Chat Interface Implementation
1. Implement chat UI components with streaming support
2. Set up AI SDK integration with multiple providers
3. Create message handling and history management
4. Implement real-time response streaming
5. Add support for code artifacts in chat

### 4.3 WebContainer Integration
1. Set up WebContainer boot and initialization
2. Implement file system operations
3. Create terminal interface with xterm.js
4. Set up process management and command execution
5. Implement preview server with hot reloading

### 4.4 State Management System
1. Set up nanostores for global state
2. Create stores for chat, files, and WebContainer
3. Implement reactive state updates
4. Set up persistence for user preferences
5. Create state synchronization mechanisms

### 4.5 Artifact Management
1. Implement code artifact creation and versioning
2. Set up file diff and merge capabilities
3. Create artifact preview and editing interface
4. Implement export and sharing functionality
5. Set up artifact persistence and recovery

## 5. Core Code Example

### 5.1 AI Chat Implementation
```typescript
// app/lib/ai/chat.ts
import { streamText, generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';
import { google } from '@ai-sdk/google';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: number;
  artifacts?: CodeArtifact[];
}

export interface CodeArtifact {
  id: string;
  type: 'file' | 'component' | 'snippet';
  title: string;
  language: string;
  content: string;
  filePath?: string;
  isNew?: boolean;
}

export class AIChat {
  private model: any;
  private systemPrompt: string;

  constructor(provider: 'openai' | 'anthropic' | 'google' = 'openai') {
    this.model = this.getModel(provider);
    this.systemPrompt = this.getSystemPrompt();
  }

  private getModel(provider: string) {
    switch (provider) {
      case 'anthropic':
        return anthropic('claude-3-5-sonnet-20241022');
      case 'google':
        return google('gemini-1.5-pro-latest');
      default:
        return openai('gpt-4-turbo-preview');
    }
  }

  private getSystemPrompt(): string {
    return `
You are an expert full-stack developer and AI assistant specialized in creating web applications.

Capabilities:
- Generate complete, production-ready code
- Create React components with TypeScript
- Build backend APIs and services
- Implement database schemas and queries
- Set up build tools and configurations
- Debug and optimize existing code

When generating code:
1. Always provide complete, runnable code
2. Include proper TypeScript types
3. Add comprehensive error handling
4. Follow modern best practices
5. Include helpful comments
6. Ensure code is production-ready

For file operations:
- Use the <boltArtifact> tag for code files
- Specify the file path and language
- Include the complete file content
- Mark new files with isNew=true

Example:
<boltArtifact id="component-1" type="file" title="Button Component" language="typescript" filePath="src/components/Button.tsx" isNew="true">
// Complete component code here
</boltArtifact>
`;
  }

  async *streamResponse(
    messages: ChatMessage[],
    onArtifact?: (artifact: CodeArtifact) => void
  ): AsyncGenerator<string, void, unknown> {
    try {
      const result = await streamText({
        model: this.model,
        system: this.systemPrompt,
        messages: messages.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        temperature: 0.7,
        maxTokens: 4000,
      });

      let accumulatedContent = '';

      for await (const delta of result.textStream) {
        accumulatedContent += delta;
        yield delta;

        // Extract artifacts from accumulated content
        const artifacts = this.extractArtifacts(accumulatedContent);
        artifacts.forEach(artifact => {
          if (onArtifact) {
            onArtifact(artifact);
          }
        });
      }
    } catch (error) {
      console.error('AI streaming error:', error);
      yield `Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`;
    }
  }

  private extractArtifacts(content: string): CodeArtifact[] {
    const artifacts: CodeArtifact[] = [];
    const artifactRegex = /<boltArtifact\s+([^>]+)>([\s\S]*?)<\/boltArtifact>/g;
    
    let match;
    while ((match = artifactRegex.exec(content)) !== null) {
      const attributes = this.parseAttributes(match[1]);
      const artifactContent = match[2].trim();

      artifacts.push({
        id: attributes.id || `artifact-${Date.now()}`,
        type: (attributes.type as any) || 'file',
        title: attributes.title || 'Untitled',
        language: attributes.language || 'typescript',
        content: artifactContent,
        filePath: attributes.filePath,
        isNew: attributes.isNew === 'true'
      });
    }

    return artifacts;
  }

  private parseAttributes(attributeString: string): Record<string, string> {
    const attributes: Record<string, string> = {};
    const attrRegex = /(\w+)=["']([^"']*)["']/g;
    
    let match;
    while ((match = attrRegex.exec(attributeString)) !== null) {
      attributes[match[1]] = match[2];
    }
    
    return attributes;
  }

  async generateCode(
    prompt: string,
    context?: {
      files?: Record<string, string>;
      framework?: string;
      requirements?: string[];
    }
  ): Promise<CodeArtifact[]> {
    const contextPrompt = context ? `
Context:
- Framework: ${context.framework || 'React'}
- Requirements: ${context.requirements?.join(', ') || 'None'}
- Existing files: ${Object.keys(context.files || {}).join(', ')}
` : '';

    const result = await generateText({
      model: this.model,
      system: this.systemPrompt,
      prompt: `${prompt}${contextPrompt}`,
      temperature: 0.7,
      maxTokens: 4000,
    });

    return this.extractArtifacts(result.text);
  }
}
```

### 5.2 Chat UI Component
```typescript
// app/components/chat/ChatInterface.tsx
import React, { useState, useRef, useEffect } from 'react';
import { useChat } from 'ai/react';
import { Send, Code, Download, Play } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { CodeArtifact, ChatMessage } from '~/lib/ai/chat';
import { useWebContainer } from '~/hooks/useWebContainer';
import { ArtifactPreview } from './ArtifactPreview';
import { MessageList } from './MessageList';

export interface ChatInterfaceProps {
  onArtifactCreate?: (artifact: CodeArtifact) => void;
  onCodeExecute?: (code: string, language: string) => void;
}

export function ChatInterface({ 
  onArtifactCreate, 
  onCodeExecute 
}: ChatInterfaceProps) {
  const [selectedArtifact, setSelectedArtifact] = useState<CodeArtifact | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { webContainer, isLoading: wcLoading } = useWebContainer();

  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
    error
  } = useChat({
    api: '/api/chat',
    onResponse: () => setIsStreaming(true),
    onFinish: () => setIsStreaming(false),
    onError: (error) => {
      console.error('Chat error:', error);
    }
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleArtifactSelect = (artifact: CodeArtifact) => {
    setSelectedArtifact(artifact);
    if (onArtifactCreate) {
      onArtifactCreate(artifact);
    }
  };

  const handleExecuteArtifact = async (artifact: CodeArtifact) => {
    if (!webContainer || !artifact.filePath) return;

    try {
      // Write file to WebContainer
      await webContainer.fs.writeFile(artifact.filePath, artifact.content);
      
      if (onCodeExecute) {
        onCodeExecute(artifact.content, artifact.language);
      }
    } catch (error) {
      console.error('Failed to execute artifact:', error);
    }
  };

  const handleDownloadArtifact = (artifact: CodeArtifact) => {
    const blob = new Blob([artifact.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = artifact.filePath || `${artifact.title}.${artifact.language}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex h-full bg-gray-50">
      {/* Chat Panel */}
      <div className="flex-1 flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          <MessageList 
            messages={messages}
            onArtifactSelect={handleArtifactSelect}
            onArtifactExecute={handleExecuteArtifact}
            onArtifactDownload={handleDownloadArtifact}
          />
          
          {isStreaming && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center space-x-2 text-blue-600"
            >
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              <span className="text-sm">AI is thinking...</span>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <div className="border-t bg-white p-4">
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <input
              value={input}
              onChange={handleInputChange}
              placeholder="Describe what you want to build..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading || wcLoading}
            />
            <button
              type="submit"
              disabled={isLoading || wcLoading || !input.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              <Send className="w-4 h-4" />
              <span>Send</span>
            </button>
          </form>
          
          {error && (
            <div className="mt-2 text-red-600 text-sm">
              Error: {error.message}
            </div>
          )}
        </div>
      </div>

      {/* Artifact Preview Panel */}
      <AnimatePresence>
        {selectedArtifact && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: '50%', opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            className="border-l bg-white"
          >
            <ArtifactPreview
              artifact={selectedArtifact}
              onClose={() => setSelectedArtifact(null)}
              onExecute={() => handleExecuteArtifact(selectedArtifact)}
              onDownload={() => handleDownloadArtifact(selectedArtifact)}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
```

### 5.3 WebContainer Integration Hook
```typescript
// app/hooks/useWebContainer.ts
import { useState, useEffect, useCallback } from 'react';
import { WebContainer } from '@stackblitz/webcontainer-core';
import type { FileSystemTree, WebContainerProcess } from '@stackblitz/webcontainer-core';

export interface UseWebContainerReturn {
  webContainer: WebContainer | null;
  isLoading: boolean;
  error: string | null;
  terminal: WebContainerProcess | null;
  previewUrl: string | null;
  bootContainer: () => Promise<void>;
  writeFiles: (files: FileSystemTree) => Promise<void>;
  runCommand: (command: string, args?: string[]) => Promise<WebContainerProcess>;
  installDependencies: () => Promise<void>;
  startDevServer: () => Promise<void>;
}

export function useWebContainer(): UseWebContainerReturn {
  const [webContainer, setWebContainer] = useState<WebContainer | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [terminal, setTerminal] = useState<WebContainerProcess | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const bootContainer = useCallback(async () => {
    if (webContainer) return;

    setIsLoading(true);
    setError(null);

    try {
      console.log('Booting WebContainer...');
      const container = await WebContainer.boot();
      setWebContainer(container);
      
      // Set up preview URL listener
      container.on('server-ready', (port, url) => {
        console.log(`Server ready on port ${port}: ${url}`);
        setPreviewUrl(url);
      });

      console.log('WebContainer booted successfully');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to boot WebContainer';
      console.error('WebContainer boot error:', errorMessage);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [webContainer]);

  const writeFiles = useCallback(async (files: FileSystemTree) => {
    if (!webContainer) {
      throw new Error('WebContainer not initialized');
    }

    try {
      await webContainer.mount(files);
      console.log('Files written to WebContainer');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to write files';
      console.error('File write error:', errorMessage);
      throw new Error(errorMessage);
    }
  }, [webContainer]);

  const runCommand = useCallback(async (
    command: string, 
    args: string[] = []
  ): Promise<WebContainerProcess> => {
    if (!webContainer) {
      throw new Error('WebContainer not initialized');
    }

    try {
      console.log(`Running command: ${command} ${args.join(' ')}`);
      const process = await webContainer.spawn(command, args);
      
      // Log output
      process.output.pipeTo(new WritableStream({
        write(data) {
          console.log(data);
        }
      }));

      return process;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Command execution failed';
      console.error('Command execution error:', errorMessage);
      throw new Error(errorMessage);
    }
  }, [webContainer]);

  const installDependencies = useCallback(async () => {
    if (!webContainer) {
      throw new Error('WebContainer not initialized');
    }

    try {
      console.log('Installing dependencies...');
      const installProcess = await runCommand('npm', ['install']);
      const exitCode = await installProcess.exit;
      
      if (exitCode !== 0) {
        throw new Error(`npm install failed with exit code ${exitCode}`);
      }
      
      console.log('Dependencies installed successfully');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Dependency installation failed';
      console.error('Dependency installation error:', errorMessage);
      throw new Error(errorMessage);
    }
  }, [webContainer, runCommand]);

  const startDevServer = useCallback(async () => {
    if (!webContainer) {
      throw new Error('WebContainer not initialized');
    }

    try {
      console.log('Starting development server...');
      const devProcess = await runCommand('npm', ['run', 'dev']);
      setTerminal(devProcess);
      
      console.log('Development server started');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to start dev server';
      console.error('Dev server error:', errorMessage);
      throw new Error(errorMessage);
    }
  }, [webContainer, runCommand]);

  // Auto-boot on mount
  useEffect(() => {
    bootContainer();
  }, [bootContainer]);

  return {
    webContainer,
    isLoading,
    error,
    terminal,
    previewUrl,
    bootContainer,
    writeFiles,
    runCommand,
    installDependencies,
    startDevServer
  };
}
```

### 5.4 State Management with Nanostores
```typescript
// app/lib/stores/chatStore.ts
import { atom, map } from 'nanostores';
import type { ChatMessage, CodeArtifact } from '~/lib/ai/chat';

export interface ChatState {
  messages: ChatMessage[];
  artifacts: CodeArtifact[];
  isStreaming: boolean;
  selectedArtifact: string | null;
  chatHistory: string[];
}

// Chat store
export const chatStore = map<ChatState>({
  messages: [],
  artifacts: [],
  isStreaming: false,
  selectedArtifact: null,
  chatHistory: []
});

// Actions
export const addMessage = (message: ChatMessage) => {
  const currentMessages = chatStore.get().messages;
  chatStore.setKey('messages', [...currentMessages, message]);
};

export const addArtifact = (artifact: CodeArtifact) => {
  const currentArtifacts = chatStore.get().artifacts;
  const existingIndex = currentArtifacts.findIndex(a => a.id === artifact.id);
  
  if (existingIndex >= 0) {
    // Update existing artifact
    const updatedArtifacts = [...currentArtifacts];
    updatedArtifacts[existingIndex] = artifact;
    chatStore.setKey('artifacts', updatedArtifacts);
  } else {
    // Add new artifact
    chatStore.setKey('artifacts', [...currentArtifacts, artifact]);
  }
};

export const setStreaming = (isStreaming: boolean) => {
  chatStore.setKey('isStreaming', isStreaming);
};

export const selectArtifact = (artifactId: string | null) => {
  chatStore.setKey('selectedArtifact', artifactId);
};

export const clearChat = () => {
  chatStore.set({
    messages: [],
    artifacts: [],
    isStreaming: false,
    selectedArtifact: null,
    chatHistory: []
  });
};

// Selectors
export const getSelectedArtifact = () => {
  const state = chatStore.get();
  if (!state.selectedArtifact) return null;
  return state.artifacts.find(a => a.id === state.selectedArtifact) || null;
};

export const getArtifactsByType = (type: CodeArtifact['type']) => {
  return chatStore.get().artifacts.filter(a => a.type === type);
};
```

### 5.5 Remix API Route for Chat
```typescript
// app/routes/api.chat.ts
import { type ActionFunctionArgs } from '@remix-run/node';
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';

export async function action({ request }: ActionFunctionArgs) {
  try {
    const { messages, provider = 'openai' } = await request.json();

    // Select AI model based on provider
    const model = provider === 'anthropic' 
      ? anthropic('claude-3-5-sonnet-20241022')
      : openai('gpt-4-turbo-preview');

    const systemPrompt = `
You are an expert full-stack developer and AI assistant.

When generating code:
1. Always provide complete, runnable code
2. Include proper TypeScript types
3. Add comprehensive error handling
4. Follow modern best practices
5. Include helpful comments

For file operations, use the <boltArtifact> tag:
<boltArtifact id="unique-id" type="file" title="File Title" language="typescript" filePath="src/path/file.tsx" isNew="true">
// Complete file content here
</boltArtifact>
`;

    const result = await streamText({
      model,
      system: systemPrompt,
      messages,
      temperature: 0.7,
      maxTokens: 4000,
    });

    return result.toAIStreamResponse();
  } catch (error) {
    console.error('Chat API error:', error);
    return new Response(
      JSON.stringify({ error: 'Internal server error' }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}
```

### 5.6 Main Application Layout
```typescript
// app/routes/_index.tsx
import { useState } from 'react';
import { useStore } from '@nanostores/react';
import { ChatInterface } from '~/components/chat/ChatInterface';
import { FileExplorer } from '~/components/files/FileExplorer';
import { PreviewPanel } from '~/components/preview/PreviewPanel';
import { Terminal } from '~/components/terminal/Terminal';
import { chatStore, addArtifact } from '~/lib/stores/chatStore';
import { useWebContainer } from '~/hooks/useWebContainer';
import type { CodeArtifact } from '~/lib/ai/chat';

export default function Index() {
  const [activePanel, setActivePanel] = useState<'chat' | 'files' | 'preview' | 'terminal'>('chat');
  const chatState = useStore(chatStore);
  const { webContainer, previewUrl, isLoading } = useWebContainer();

  const handleArtifactCreate = async (artifact: CodeArtifact) => {
    // Add to store
    addArtifact(artifact);

    // Write to WebContainer if file path is provided
    if (webContainer && artifact.filePath) {
      try {
        await webContainer.fs.writeFile(artifact.filePath, artifact.content);
        console.log(`File written: ${artifact.filePath}`);
      } catch (error) {
        console.error('Failed to write file to WebContainer:', error);
      }
    }
  };

  const handleCodeExecute = async (code: string, language: string) => {
    if (!webContainer) return;

    try {
      if (language === 'javascript' || language === 'typescript') {
        // Execute JavaScript/TypeScript code
        const process = await webContainer.spawn('node', ['-e', code]);
        await process.exit;
      }
    } catch (error) {
      console.error('Code execution failed:', error);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <header className="bg-white border-b px-4 py-2 flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-800">AI Development Environment</h1>
        
        <div className="flex items-center space-x-2">
          {isLoading && (
            <div className="flex items-center space-x-2 text-blue-600">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              <span className="text-sm">Initializing...</span>
            </div>
          )}
          
          <div className="flex bg-gray-200 rounded-lg p-1">
            {(['chat', 'files', 'preview', 'terminal'] as const).map((panel) => (
              <button
                key={panel}
                onClick={() => setActivePanel(panel)}
                className={`px-3 py-1 rounded-md text-sm font-medium capitalize transition-colors ${
                  activePanel === panel
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {panel}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Primary Panel */}
        <div className="flex-1">
          {activePanel === 'chat' && (
            <ChatInterface
              onArtifactCreate={handleArtifactCreate}
              onCodeExecute={handleCodeExecute}
            />
          )}
          
          {activePanel === 'files' && (
            <FileExplorer
              artifacts={chatState.artifacts}
              onFileSelect={(artifact) => addArtifact(artifact)}
            />
          )}
          
          {activePanel === 'preview' && (
            <PreviewPanel
              previewUrl={previewUrl}
              isLoading={isLoading}
            />
          )}
          
          {activePanel === 'terminal' && (
            <Terminal webContainer={webContainer} />
          )}
        </div>
      </div>
    </div>
  );
}
```

## 6. Common Pitfalls & Error Handling

### 6.1 WebContainer Boot Failures
- **Problem**: WebContainer fails to initialize in certain browsers
- **Solution**: Implement fallback mechanisms and clear error messaging
- **Prevention**: Check browser compatibility and required headers

### 6.2 AI Response Streaming Issues
- **Problem**: Streaming responses get cut off or fail
- **Solution**: Implement retry logic and connection monitoring
- **Detection**: Monitor stream completion and implement timeouts

### 6.3 File System Synchronization
- **Problem**: Files get out of sync between UI and WebContainer
- **Solution**: Implement bidirectional sync and conflict resolution
- **Prevention**: Use atomic file operations and version tracking

### 6.4 Memory Management
- **Problem**: Large artifacts cause memory issues
- **Solution**: Implement lazy loading and cleanup mechanisms
- **Monitoring**: Track memory usage and implement limits

## 7. Performance Optimization

### 7.1 Code Splitting
- Lazy load Monaco Editor and heavy components
- Split AI providers into separate chunks
- Implement route-based code splitting

### 7.2 Streaming Optimization
- Implement response caching for repeated queries
- Use compression for large responses
- Optimize token usage and context management

### 7.3 WebContainer Optimization
- Cache WebContainer instances
- Implement file system snapshots
- Optimize build processes and hot reloading

## 8. Integration with Genesis Engine

### 8.1 Multi-Agent Integration
- Connect chat interface to agent orchestrator
- Implement agent-specific UI components
- Set up agent result visualization

### 8.2 Database Integration
- Persist chat history and artifacts
- Implement user session management
- Set up project versioning and sharing

### 8.3 Authentication & Security
- Implement secure API key management
- Set up user authentication with Supabase
- Implement sandbox security measures

---

*Implementation Status: Ready for Genesis Engine integration*  
*Next Steps: Integrate with multi-agent architecture and implement advanced artifact management*