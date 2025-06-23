# Bolt.diy Component & UI Architecture Analysis

## Overview
This document analyzes Bolt.diy's component architecture, UI patterns, and state management systems that can be adapted for sentient-core.

## Component Architecture

### 1. Core Component Structure

#### Main Application Layout
```typescript
// app/routes/_index.tsx - Landing page structure
export default function Index() {
  return (
    <div className="flex flex-col h-full w-full bg-bolt-elements-background-depth-1">
      <BackgroundRays />
      <Header />
      <ClientOnly fallback={<BaseChat />}>
        {() => <Chat />}
      </ClientOnly>
    </div>
  );
}
```

#### Component Hierarchy
- **Root Layout**: Full-height flex container
- **Background**: Decorative rays component
- **Header**: Navigation and controls
- **Chat Interface**: Main interaction area with client-side hydration

### 2. UI Component System

#### Design System Components (`app/components/ui/`)
```typescript
// Comprehensive UI component exports
export * from './Badge';
export * from './Button';
export * from './Card';
export * from './Checkbox';
export * from './Dialog';
export * from './IconButton';
export * from './Input';
export * from './Tabs';
export * from './LoadingDots';
export * from './SearchInput';
export * from './StatusIndicator';
// ... and more
```

#### Button Component Pattern
```typescript
// app/components/ui/Button.tsx
const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-bolt-elements-background text-bolt-elements-textPrimary',
        destructive: 'bg-red-500 text-white hover:bg-red-600',
        outline: 'border border-bolt-elements-borderColor bg-transparent',
        // ... more variants
      },
      size: {
        default: 'h-9 px-4 py-2',
        sm: 'h-8 rounded-md px-3 text-xs',
        lg: 'h-10 rounded-md px-8',
        icon: 'h-9 w-9',
      },
    },
  },
);
```

**Key Patterns:**
- **Class Variance Authority (CVA)**: Type-safe variant system
- **Consistent Design Tokens**: `bolt-elements-*` CSS custom properties
- **Accessibility**: Focus rings, proper ARIA attributes
- **Responsive Design**: Size variants for different contexts

### 3. Workbench Architecture

#### Workbench Component Structure
```typescript
// app/components/workbench/Workbench.client.tsx
interface WorkspaceProps {
  chatStarted?: boolean;
  isStreaming?: boolean;
  actionRunner: ActionRunner;
  metadata?: { gitUrl?: string; };
  updateChatMestaData?: (metadata: any) => void;
  setSelectedElement?: (element: ElementInfo | null) => void;
}
```

#### View Management System
```typescript
const sliderOptions: SliderOptions<WorkbenchViewType> = {
  left: { value: 'code', text: 'Code' },
  middle: { value: 'diff', text: 'Diff' },
  right: { value: 'preview', text: 'Preview' },
};
```

**Key Features:**
- **Multi-view Interface**: Code, Diff, Preview modes
- **File Change Tracking**: Dropdown for modified files
- **Animation System**: Framer Motion for smooth transitions
- **Inspector Integration**: Element selection and analysis

## State Management Architecture

### 1. Nanostores Pattern

#### Chat Store (Simple State)
```typescript
// app/lib/stores/chat.ts
export const chatStore = map({
  started: false,
  aborted: false,
  showChat: true,
});
```

#### Editor Store (Complex State)
```typescript
// app/lib/stores/editor.ts
export class EditorStore {
  selectedFile: SelectedFile = atom<string | undefined>();
  documents: MapStore<EditorDocuments> = map({});
  
  currentDocument = computed([this.documents, this.selectedFile], 
    (documents, selectedFile) => {
      if (!selectedFile) return undefined;
      return documents[selectedFile];
    }
  );
  
  constructor(filesStore: FilesStore) {
    this.#filesStore = filesStore;
  }
}
```

#### Files Store (Advanced State Management)
```typescript
// app/lib/stores/files.ts
export class FilesStore {
  #webcontainer: Promise<WebContainer>;
  #modifiedFiles: Map<string, string> = new Map();
  #deletedPaths: Set<string> = new Set();
  files: MapStore<FileMap> = map({});
  
  // File locking system
  #loadLockedFiles() {
    // Load from localStorage and apply locks
  }
}
```

**State Management Patterns:**
- **Reactive Stores**: Nanostores for fine-grained reactivity
- **Computed Values**: Derived state with automatic updates
- **Class-based Stores**: Complex state logic encapsulation
- **Persistence Integration**: Hot reload support and localStorage
- **File Locking**: Collaborative editing protection

### 2. Hook System

#### Available Hooks (`app/lib/hooks/`)
```typescript
// Core hooks for different functionalities
export * from './useMessageParser';     // Chat message processing
export * from './usePromptEnhancer';    // AI prompt optimization
export * from './useShortcuts';         // Keyboard shortcuts
export * from './useEditChatDescription'; // Chat metadata
export * from './useViewport';          // Responsive design
export * from './useFeatures';          // Feature flags
export * from './useNotifications';     // Toast notifications
export * from './useConnectionStatus';  // Network status
export * from './useDebugStatus';       // Development tools
```

#### Message Parser Hook Pattern
```typescript
// app/lib/hooks/useMessageParser.ts
export function useMessageParser() {
  const parser = useMemo(() => new StreamingMessageParser({
    onArtifactOpen: (artifact) => {
      workbenchStore.addArtifact(artifact);
    },
    onArtifactClose: () => {
      // Handle artifact completion
    },
    onActionOpen: (action) => {
      workbenchStore.addAction(action);
    },
    onActionClose: () => {
      workbenchStore.runAction();
    },
  }), []);
  
  return parser;
}
```

## API & Service Layer

### 1. API Route Structure

#### Chat API (`app/routes/api.chat.ts`)
```typescript
export async function action({ context, request }: ActionFunctionArgs) {
  const { messages, files, promptId, contextOptimization, supabase, chatMode, designScheme } = 
    await request.json();
  
  // Cookie-based API key management
  const cookieHeader = request.headers.get('Cookie');
  const apiKeys = JSON.parse(parseCookies(cookieHeader || '').apiKeys || '{}');
  
  // Streaming response with progress tracking
  const dataStream = createDataStream({
    async execute(dataStream) {
      // Context optimization and file filtering
      // LLM streaming with usage tracking
    }
  });
}
```

#### Available API Endpoints
- `api.chat.ts` - Main chat interface
- `api.models.$provider.ts` - Dynamic model management
- `api.enhancer.ts` - Prompt enhancement
- `api.supabase.*.ts` - Database operations
- `api.github-template.ts` - Template management
- `api.system.*.ts` - System diagnostics

### 2. Service Architecture

#### Import/Export Service
```typescript
// app/lib/services/importExportService.ts
export class ImportExportService {
  static async exportAllChats(db: IDBDatabase) {
    const chats = await getAllChats(db);
    return {
      chats: sanitizedChats,
      exportDate: new Date().toISOString(),
    };
  }
  
  static async exportSettings() {
    return {
      core: { /* user settings */ },
      providers: { /* API configurations */ },
      features: { /* feature flags */ },
    };
  }
}
```

## Integration Recommendations for Sentient-Core

### 1. High-Priority Adoptions

#### Component System
- **CVA-based Design System**: Implement variant-driven components
- **Workbench Pattern**: Multi-view interface for different agent outputs
- **File Management UI**: Adapt for agent-generated artifacts

#### State Management
- **Nanostores Integration**: Replace current state with reactive stores
- **Class-based Store Pattern**: For complex agent state management
- **Computed Values**: For derived agent status and progress

### 2. Architectural Patterns

#### Hook System
```typescript
// Proposed hooks for sentient-core
useAgentParser()     // Parse agent responses
useAgentStatus()     // Track agent execution
useArtifactManager() // Manage generated artifacts
useWorkflowState()   // Handle async workflows
```

#### API Integration
```typescript
// Adapt streaming patterns for agent communication
const agentStream = createDataStream({
  async execute(dataStream) {
    // Stream agent progress and outputs
    // Handle SurrealDB state updates
    // Manage checkpoint creation
  }
});
```

### 3. Next Analysis Steps

1. **Part 3**: WebContainer & Sandbox Integration
2. **Part 4**: LLM Provider Management
3. **Part 5**: Persistence & Database Patterns
4. **Part 6**: Action Runner & Execution Engine
5. **Part 7**: Integration Roadmap & Implementation Guide

## Key Takeaways

- **Modular Component Architecture**: Clean separation of concerns
- **Reactive State Management**: Fine-grained updates with Nanostores
- **Streaming-First Design**: Real-time updates and progress tracking
- **Type-Safe Patterns**: Comprehensive TypeScript integration
- **Accessibility Focus**: Built-in ARIA support and keyboard navigation
- **Performance Optimization**: Client-side hydration and lazy loading

This component architecture provides a solid foundation for building the sentient-core UI while maintaining the reactive, streaming-first approach needed for AI agent interactions.