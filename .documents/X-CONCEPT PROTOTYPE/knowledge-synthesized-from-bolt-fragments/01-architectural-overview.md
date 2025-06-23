# Bolt.diy Architecture Analysis - Part 1: Core Architecture Overview

## Executive Summary

Bolt.diy represents a sophisticated AI-powered development environment that combines WebContainer technology for in-browser code execution with advanced LLM integration for code generation and management. This analysis provides a comprehensive breakdown of its architecture for integration into the sentient-core project.

## Core Architectural Patterns

### 1. Store-Based State Management (Nanostores)

**Pattern**: Reactive state management using nanostores with MapStore and WritableAtom

**Key Implementation**:
```typescript
// From app/lib/stores/workbench.ts
import { atom, map, type MapStore, type WritableAtom } from 'nanostores';

export class WorkbenchStore {
  artifacts: Artifacts = map({});
  showWorkbench: WritableAtom<boolean> = atom(false);
  currentView: WritableAtom<WorkbenchViewType> = atom('code');
  unsavedFiles: WritableAtom<Set<string>> = atom(new Set<string>());
  
  // Hot reload preservation
  constructor() {
    if (import.meta.hot) {
      import.meta.hot.data.artifacts = this.artifacts;
      import.meta.hot.data.unsavedFiles = this.unsavedFiles;
    }
  }
}
```

**Sentient-Core Integration**: Replace current state management with nanostores pattern for better reactivity and hot reload support.

### 2. Action Runner Pattern

**Pattern**: Queue-based action execution with abort capabilities and status tracking

**Key Implementation**:
```typescript
// From app/lib/runtime/action-runner.ts
export type ActionStatus = 'pending' | 'running' | 'complete' | 'aborted' | 'failed';

export class ActionRunner {
  #currentExecutionPromise: Promise<void> = Promise.resolve();
  actions: ActionsMap = map({});
  
  addAction(data: ActionCallbackData) {
    const abortController = new AbortController();
    this.actions.setKey(actionId, {
      ...data.action,
      status: 'pending',
      executed: false,
      abort: () => {
        abortController.abort();
        this.#updateAction(actionId, { status: 'aborted' });
      },
      abortSignal: abortController.signal,
    });
  }
  
  async runAction(data: ActionCallbackData, isStreaming: boolean = false) {
    this.#currentExecutionPromise = this.#currentExecutionPromise
      .then(() => this.#executeAction(actionId, isStreaming))
      .catch((error) => console.error('Action failed:', error));
  }
}
```

**Sentient-Core Integration**: Implement similar pattern for E2B sandbox actions and async agent task execution.

### 3. WebContainer Integration Pattern

**Pattern**: Promise-based WebContainer initialization with error forwarding and hot reload support

**Key Implementation**:
```typescript
// From app/lib/webcontainer/index.ts
export let webcontainer: Promise<WebContainer> = new Promise(() => {});

if (!import.meta.env.SSR) {
  webcontainer = Promise.resolve()
    .then(() => {
      return WebContainer.boot({
        coep: 'credentialless',
        workdirName: WORK_DIR_NAME,
        forwardPreviewErrors: true,
      });
    })
    .then(async (webcontainer) => {
      // Error handling setup
      webcontainer.on('preview-message', (message) => {
        if (message.type === 'PREVIEW_UNCAUGHT_EXCEPTION') {
          workbenchStore.actionAlert.set({
            type: 'preview',
            title: 'Uncaught Exception',
            description: message.message,
            content: `Stack trace:\n${cleanStackTrace(message.stack)}`,
          });
        }
      });
      return webcontainer;
    });
}
```

**Sentient-Core Integration**: Adapt this pattern for E2B sandbox initialization with similar error handling.

### 4. LLM Provider Management

**Pattern**: Plugin-based provider system with dynamic model discovery

**Key Implementation**:
```typescript
// From app/lib/modules/llm/manager.ts
export class LLMManager {
  private static _instance: LLMManager;
  private _providers: Map<string, BaseProvider> = new Map();
  private _modelList: ModelInfo[] = [];
  
  private async _registerProvidersFromDirectory() {
    for (const exportedItem of Object.values(providers)) {
      if (typeof exportedItem === 'function' && exportedItem.prototype instanceof BaseProvider) {
        const provider = new exportedItem();
        this.registerProvider(provider);
      }
    }
  }
  
  async updateModelList(options: {
    apiKeys?: Record<string, string>;
    providerSettings?: Record<string, IProviderSetting>;
  }): Promise<ModelInfo[]> {
    // Dynamic model discovery from enabled providers
  }
}
```

**Sentient-Core Integration**: Extend current LLM integration with this provider management pattern.

## Directory Structure Analysis

### Core Libraries (`app/lib/`)

1. **`.server/`** - Server-side LLM utilities
   - `llm/` - Stream handling, context selection, summarization
   - Key files: `stream-text.ts`, `select-context.ts`, `create-summary.ts`

2. **`hooks/`** - React hooks for state management
   - 17 specialized hooks for different concerns
   - Key patterns: `useMessageParser`, `usePromptEnhancer`, `useSupabaseConnection`

3. **`modules/llm/`** - LLM provider abstraction
   - `base-provider.ts` - Abstract provider interface
   - `manager.ts` - Provider registration and management
   - `providers/` - Individual provider implementations

4. **`persistence/`** - Data persistence layer
   - `db.ts` - IndexedDB operations
   - `chats.ts` - Chat history management
   - `useChatHistory.ts` - React hook for chat persistence

5. **`runtime/`** - Core execution engine
   - `action-runner.ts` - Action execution management
   - `message-parser.ts` - Streaming message parsing

6. **`stores/`** - State management
   - 13 specialized stores using nanostores
   - Key stores: `workbench.ts`, `chat.ts`, `files.ts`

7. **`webcontainer/`** - WebContainer integration
   - `index.ts` - WebContainer initialization and management

## Key Insights for Sentient-Core

1. **Modular Architecture**: Each concern is separated into focused modules
2. **Reactive State**: Nanostores provide excellent reactivity with minimal overhead
3. **Action-Based Execution**: All operations are modeled as actions with status tracking
4. **Provider Abstraction**: LLM providers are pluggable and discoverable
5. **Persistence Strategy**: IndexedDB for client-side persistence with structured schemas
6. **Error Handling**: Comprehensive error forwarding and alert systems

## Next Steps

This overview establishes the foundation. The following documents will detail:
- Part 2: Component Architecture and UI Patterns
- Part 3: Streaming and Real-time Communication
- Part 4: File System and Code Management
- Part 5: Integration Roadmap for Sentient-Core