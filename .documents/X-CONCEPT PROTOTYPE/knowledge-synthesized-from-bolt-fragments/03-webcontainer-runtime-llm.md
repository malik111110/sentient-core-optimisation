# Bolt.diy WebContainer, Runtime & LLM Architecture Analysis

## Overview
This document analyzes Bolt.diy's WebContainer integration, runtime execution patterns, and LLM provider management system for adaptation in sentient-core.

## WebContainer Integration

### 1. WebContainer Initialization

#### Core Setup Pattern
```typescript
// app/lib/webcontainer/index.ts
export let webcontainer: Promise<WebContainer> = new Promise(() => {
  // noop for ssr
});

if (!import.meta.env.SSR) {
  webcontainer = Promise.resolve()
    .then(() => {
      return WebContainer.boot({
        coep: 'credentialless',
        workdirName: WORK_DIR_NAME,
        forwardPreviewErrors: true, // Enable error forwarding from iframes
      });
    })
    .then(async (webcontainer) => {
      webcontainerContext.loaded = true;
      
      // Setup preview script for error handling
      const response = await fetch('/inspector-script.js');
      const inspectorScript = await response.text();
      await webcontainer.setPreviewScript(inspectorScript);
      
      // Listen for preview errors
      webcontainer.on('preview-message', (message) => {
        if (message.type === 'PREVIEW_UNCAUGHT_EXCEPTION' || 
            message.type === 'PREVIEW_UNHANDLED_REJECTION') {
          const isPromise = message.type === 'PREVIEW_UNHANDLED_REJECTION';
          const title = isPromise ? 'Unhandled Promise Rejection' : 'Uncaught Exception';
          
          workbenchStore.actionAlert.set({
            type: 'preview',
            title,
            description: 'message' in message ? message.message : 'Unknown error',
            content: `Error occurred at ${message.pathname}${message.search}${message.hash}\nPort: ${message.port}\n\nStack trace:\n${cleanStackTrace(message.stack || '')}`,
            source: 'preview',
          });
        }
      });
      
      return webcontainer;
    });
}
```

**Key Features:**
- **SSR Safety**: Conditional initialization for client-side only
- **Hot Reload Support**: State persistence across development reloads
- **Error Forwarding**: Comprehensive error handling from preview iframes
- **Inspector Integration**: Custom script injection for debugging
- **Promise-based Architecture**: Async initialization with proper error handling

### 2. WebContainer Context Management

#### Context State Pattern
```typescript
interface WebContainerContext {
  loaded: boolean;
}

export const webcontainerContext: WebContainerContext = 
  import.meta.hot?.data.webcontainerContext ?? { loaded: false };

if (import.meta.hot) {
  import.meta.hot.data.webcontainerContext = webcontainerContext;
}
```

**Benefits for Sentient-Core:**
- **State Persistence**: Maintain container state across hot reloads
- **Loading Indicators**: Track initialization status for UI feedback
- **Development Experience**: Seamless development workflow

## Runtime Message Parser

### 1. Streaming Message Parser Architecture

#### Core Parser Structure
```typescript
// app/lib/runtime/message-parser.ts
export class StreamingMessageParser {
  #messages = new Map<string, MessageState>();
  
  constructor(private _options: StreamingMessageParserOptions = {}) {}
  
  parse(messageId: string, input: string) {
    let state = this.#messages.get(messageId);
    
    if (!state) {
      state = {
        position: 0,
        insideAction: false,
        insideArtifact: false,
        currentAction: { content: '' },
        actionId: 0,
      };
      this.#messages.set(messageId, state);
    }
    
    // Parse streaming content with state management
    // Handle artifacts, actions, and quick actions
  }
}
```

#### Message State Management
```typescript
interface MessageState {
  position: number;
  insideArtifact: boolean;
  insideAction: boolean;
  currentArtifact?: BoltArtifactData;
  currentAction: BoltActionData;
  actionId: number;
}
```

### 2. Artifact and Action Parsing

#### Tag-based Parsing System
```typescript
const ARTIFACT_TAG_OPEN = '<boltArtifact';
const ARTIFACT_TAG_CLOSE = '</boltArtifact>';
const ARTIFACT_ACTION_TAG_OPEN = '<boltAction';
const ARTIFACT_ACTION_TAG_CLOSE = '</boltAction>';
const BOLT_QUICK_ACTIONS_OPEN = '<bolt-quick-actions>';
const BOLT_QUICK_ACTIONS_CLOSE = '</bolt-quick-actions>';
```

#### Content Processing Pipeline
```typescript
function cleanoutMarkdownSyntax(content: string) {
  const codeBlockRegex = /^\s*```\w*\n([\s\S]*?)\n\s*```\s*$/;
  const match = content.match(codeBlockRegex);
  
  if (match) {
    return match[1]; // Remove markdown code blocks
  } else {
    return content;
  }
}

function cleanEscapedTags(content: string) {
  return content.replace(/&lt;/g, '<').replace(/&gt;/g, '>');
}
```

### 3. Callback System

#### Parser Callbacks Interface
```typescript
export interface ParserCallbacks {
  onArtifactOpen?: ArtifactCallback;
  onArtifactClose?: ArtifactCallback;
  onActionOpen?: ActionCallback;
  onActionStream?: ActionCallback;
  onActionClose?: ActionCallback;
}

export interface ActionCallbackData {
  artifactId: string;
  messageId: string;
  actionId: string;
  action: BoltAction;
}
```

**Streaming Benefits:**
- **Real-time Updates**: Progressive content rendering
- **State Preservation**: Maintain parsing state across chunks
- **Error Recovery**: Graceful handling of incomplete messages
- **Action Tracking**: Precise action lifecycle management

## LLM Provider Management

### 1. Base Provider Architecture

#### Abstract Provider Pattern
```typescript
// app/lib/modules/llm/base-provider.ts
export abstract class BaseProvider implements ProviderInfo {
  abstract name: string;
  abstract staticModels: ModelInfo[];
  abstract config: ProviderConfig;
  
  cachedDynamicModels?: {
    cacheId: string;
    models: ModelInfo[];
  };
  
  getApiKeyLink?: string;
  labelForGetApiKey?: string;
  icon?: string;
}
```

#### Provider Configuration System
```typescript
getProviderBaseUrlAndKey(options: {
  apiKeys?: Record<string, string>;
  providerSettings?: IProviderSetting;
  serverEnv?: Record<string, string>;
  defaultBaseUrlKey: string;
  defaultApiTokenKey: string;
}) {
  const { apiKeys, providerSettings, serverEnv, defaultBaseUrlKey, defaultApiTokenKey } = options;
  
  let settingsBaseUrl = providerSettings?.baseUrl;
  const manager = LLMManager.getInstance();
  
  if (settingsBaseUrl && settingsBaseUrl.length == 0) {
    settingsBaseUrl = undefined;
  }
  
  const baseUrlKey = this.config.baseUrlKey || defaultBaseUrlKey;
  let baseUrl = settingsBaseUrl || 
                serverEnv?.[baseUrlKey] || 
                process?.env?.[baseUrlKey] || 
                manager.env?.[baseUrlKey] || 
                this.config.baseUrl;
  
  const apiTokenKey = this.config.apiTokenKey || defaultApiTokenKey;
  const apiKey = apiKeys?.[this.name] || 
                 serverEnv?.[apiTokenKey] || 
                 process?.env?.[apiTokenKey] || 
                 manager.env?.[apiTokenKey];
  
  return { baseUrl, apiKey };
}
```

### 2. Dynamic Model Management

#### Model Caching System
```typescript
getModelsFromCache(options: {
  apiKeys?: Record<string, string>;
  providerSettings?: Record<string, IProviderSetting>;
  serverEnv?: Record<string, string>;
}): ModelInfo[] | null {
  if (!this.cachedDynamicModels) {
    return null;
  }
  
  const cacheKey = this.cachedDynamicModels.cacheId;
  const generatedCacheKey = this.getDynamicModelsCacheKey(options);
  
  if (cacheKey !== generatedCacheKey) {
    this.cachedDynamicModels = undefined;
    return null;
  }
  
  return this.cachedDynamicModels.models;
}

getDynamicModelsCacheKey(options: {
  apiKeys?: Record<string, string>;
  providerSettings?: Record<string, IProviderSetting>;
  serverEnv?: Record<string, string>;
}) {
  return JSON.stringify({
    apiKeys: options.apiKeys?.[this.name],
    providerSettings: options.providerSettings?.[this.name],
    serverEnv: options.serverEnv,
  });
}
```

### 3. LLM Manager Singleton

#### Manager Architecture
```typescript
// app/lib/modules/llm/manager.ts
export class LLMManager {
  private static _instance: LLMManager;
  private _providers = new Map<string, BaseProvider>();
  private _modelList: ModelInfo[] = [];
  
  static getInstance(): LLMManager {
    if (!LLMManager._instance) {
      LLMManager._instance = new LLMManager();
    }
    return LLMManager._instance;
  }
  
  registerProvider(provider: BaseProvider) {
    this._providers.set(provider.name, provider);
  }
  
  async getModelList(options: {
    apiKeys?: Record<string, string>;
    providerSettings?: Record<string, IProviderSetting>;
    serverEnv?: Record<string, string>;
  }): Promise<ModelInfo[]> {
    // Combine static and dynamic models
    const dynamicModels = await Promise.all(
      Array.from(this._providers.values()).map(async (provider) => {
        if (!provider.getDynamicModels) {
          return [];
        }
        
        const cachedModels = provider.getModelsFromCache(options);
        if (cachedModels) {
          return cachedModels;
        }
        
        const dynamicModels = await provider
          .getDynamicModels(apiKeys, providerSettings?.[provider.name], serverEnv)
          .then((models) => {
            provider.storeDynamicModels(options, models);
            return models;
          })
          .catch((err) => {
            logger.error(`Error getting dynamic models ${provider.name}:`, err);
            return [];
          });
        
        return dynamicModels;
      }),
    );
    
    const staticModels = Array.from(this._providers.values()).flatMap((p) => p.staticModels || []);
    const dynamicModelsFlat = dynamicModels.flat();
    
    // Filter out duplicates and combine
    const modelList = [...dynamicModelsFlat, ...filteredStaticModels];
    modelList.sort((a, b) => a.name.localeCompare(b.name));
    
    return modelList;
  }
}
```

### 4. Provider Types System

#### Model and Provider Interfaces
```typescript
// app/lib/modules/llm/types.ts
export interface ModelInfo {
  name: string;
  label: string;
  provider: string;
  maxTokenAllowed: number;
}

export interface ProviderInfo {
  name: string;
  staticModels: ModelInfo[];
  getDynamicModels?: (
    apiKeys?: Record<string, string>,
    settings?: IProviderSetting,
    serverEnv?: Record<string, string>,
  ) => Promise<ModelInfo[]>;
  getModelInstance: (options: {
    model: string;
    serverEnv: Env;
    apiKeys?: Record<string, string>;
    providerSettings?: Record<string, IProviderSetting>;
  }) => LanguageModelV1;
  getApiKeyLink?: string;
  labelForGetApiKey?: string;
  icon?: string;
}

export interface ProviderConfig {
  baseUrlKey?: string;
  baseUrl?: string;
  apiTokenKey?: string;
}
```

## Integration Recommendations for Sentient-Core

### 1. WebContainer Adaptation

#### Agent Sandbox Integration
```typescript
// Proposed adaptation for sentient-core
export class AgentSandboxManager {
  private webcontainer: Promise<WebContainer>;
  private agentContexts = new Map<string, AgentContext>();
  
  async initializeAgentSandbox(agentId: string) {
    const container = await this.webcontainer;
    
    // Create isolated workspace for agent
    const agentWorkspace = `/agents/${agentId}`;
    await container.fs.mkdir(agentWorkspace, { recursive: true });
    
    // Setup agent-specific error handling
    container.on('preview-message', (message) => {
      this.handleAgentError(agentId, message);
    });
    
    return {
      workspace: agentWorkspace,
      container,
      executeCommand: (cmd: string, args: string[]) => 
        container.spawn(cmd, args, { cwd: agentWorkspace }),
      writeFile: (path: string, content: string) => 
        container.fs.writeFile(`${agentWorkspace}/${path}`, content),
    };
  }
}
```

### 2. Message Parser for Agent Communication

#### Agent Response Parser
```typescript
// Adapted for agent-to-agent communication
export class AgentMessageParser extends StreamingMessageParser {
  constructor(options: AgentParserOptions) {
    super({
      callbacks: {
        onArtifactOpen: (data) => {
          // Handle agent-generated artifacts
          this.handleAgentArtifact(data);
        },
        onActionOpen: (data) => {
          // Handle agent actions
          this.handleAgentAction(data);
        },
        onActionStream: (data) => {
          // Stream agent progress
          this.streamAgentProgress(data);
        },
      },
    });
  }
  
  private handleAgentArtifact(data: ArtifactCallbackData) {
    // Store in SurrealDB
    // Update agent state
    // Notify other agents
  }
}
```

### 3. LLM Provider Integration

#### Multi-Agent Provider Management
```typescript
// Enhanced for multi-agent scenarios
export class AgentLLMManager extends LLMManager {
  private agentProviders = new Map<string, BaseProvider>();
  
  registerAgentProvider(agentId: string, provider: BaseProvider) {
    this.agentProviders.set(agentId, provider);
  }
  
  async getAgentModel(agentId: string, options: ModelOptions) {
    const provider = this.agentProviders.get(agentId) || this.getDefaultProvider();
    return provider.getModelInstance(options);
  }
  
  async streamAgentResponse(agentId: string, messages: Messages) {
    const model = await this.getAgentModel(agentId, {});
    
    return streamText({
      model,
      messages,
      onChunk: (chunk) => {
        // Update SurrealDB with streaming progress
        this.updateAgentProgress(agentId, chunk);
      },
    });
  }
}
```

### 4. Runtime Architecture Adaptation

#### Async Agent Runtime
```typescript
// Integration with existing AsyncBaseAgent
export class AgentRuntime {
  private parser: AgentMessageParser;
  private sandboxManager: AgentSandboxManager;
  private llmManager: AgentLLMManager;
  
  async executeAgentTask(agentId: string, task: AgentTask) {
    // Initialize sandbox
    const sandbox = await this.sandboxManager.initializeAgentSandbox(agentId);
    
    // Get LLM model
    const model = await this.llmManager.getAgentModel(agentId, task.modelOptions);
    
    // Stream response with parsing
    const stream = await streamText({
      model,
      messages: task.messages,
      onChunk: (chunk) => {
        this.parser.parse(task.id, chunk.text);
      },
    });
    
    return stream;
  }
}
```

## Key Takeaways

### WebContainer Benefits
- **Isolated Execution**: Secure sandbox for agent-generated code
- **Error Handling**: Comprehensive error forwarding and debugging
- **Hot Reload Support**: Development-friendly state management
- **Preview Integration**: Real-time preview with error tracking

### Runtime Parser Benefits
- **Streaming Support**: Real-time content processing
- **State Management**: Robust parsing state preservation
- **Extensible Callbacks**: Flexible event handling system
- **Content Cleaning**: Automatic markdown and escape handling

### LLM Provider Benefits
- **Multi-Provider Support**: Flexible provider switching
- **Dynamic Model Discovery**: Runtime model enumeration
- **Caching System**: Efficient model list management
- **Configuration Flexibility**: Multiple configuration sources

### Next Steps
1. **Part 4**: Persistence & Database Integration
2. **Part 5**: Action Runner & Execution Engine
3. **Part 6**: Integration Roadmap & Implementation Guide

This runtime architecture provides the foundation for building a robust, streaming-first agent execution environment that can handle complex multi-agent workflows while maintaining security and performance.