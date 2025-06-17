# TutorialKit Integration Guide

**ID:** guide:feature:tutorialkit_integration  
**Source Reference(s):** /agentic web dev/tutorialkit  
**Last Validated:** June 2025

## 1. Purpose

Implement TutorialKit for creating interactive, step-by-step coding tutorials and educational content within the Genesis Engine, providing a comprehensive learning platform with live code execution and guided instruction.

## 2. Key Concepts

- **Interactive Tutorials**: Step-by-step coding lessons with live execution
- **WebContainer Integration**: Browser-based code execution environment
- **Lesson Structure**: Hierarchical organization of tutorial content
- **Code Validation**: Automatic checking of user progress
- **Template System**: Reusable tutorial templates and components
- **Progress Tracking**: User advancement through tutorial steps
- **Live Preview**: Real-time code execution and output display
- **Markdown-based Content**: Tutorial content written in enhanced Markdown

## 3. Required Dependencies

### Frontend Dependencies
```json
{
  "dependencies": {
    "@tutorialkit/astro": "^0.2.0",
    "@tutorialkit/components": "^0.2.0",
    "@tutorialkit/runtime": "^0.2.0",
    "@tutorialkit/theme": "^0.2.0",
    "@stackblitz/webcontainer-core": "^1.1.0",
    "astro": "^4.0.0",
    "@astrojs/react": "^3.0.0",
    "@astrojs/tailwind": "^5.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwindcss": "^3.4.0",
    "monaco-editor": "^0.45.0",
    "@monaco-editor/react": "^4.6.0",
    "shiki": "^0.14.0",
    "remark": "^15.0.0",
    "remark-gfm": "^4.0.0",
    "unified": "^11.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

### Environment Variables
```bash
# TutorialKit Configuration
TUTORIAL_BASE_URL=https://your-domain.com/tutorials
TUTORIAL_CONTENT_PATH=./src/content/tutorials
TUTORIAL_ASSETS_PATH=./public/tutorial-assets

# WebContainer Configuration
WEBCONTAINER_API_URL=https://webcontainer.io
WEBCONTAINER_ORIGIN=https://your-domain.com

# Content Management
CONTENT_GITHUB_REPO=your-org/tutorial-content
CONTENT_GITHUB_TOKEN=your_github_token
CONTENT_BRANCH=main

# Analytics and Tracking
TUTORIAL_ANALYTICS_ID=your_analytics_id
PROGRESS_TRACKING_ENABLED=true
```

## 4. Step-by-Step Implementation Plan

### 4.1 Project Setup and Configuration

1.  **Initialize a new TutorialKit Project:**
    Use the CLI to scaffold a new project. This will set up Astro, Tailwind CSS, and all necessary TutorialKit packages.
    ```bash
    npx tutorialkit@latest create my-tutorial-project
    cd my-tutorial-project
    ```

2.  **Install Additional Dependencies (if any):**
    While the CLI installs core dependencies, you might need others based on your specific tutorial content (e.g., particular JavaScript libraries for examples).

3.  **Configure Astro (`astro.config.mjs`):**
    The CLI should pre-configure Astro with TutorialKit's Astro integration (`@tutorialkit/astro`). Verify that your `astro.config.mjs` includes it. It typically involves adding the integration to the `integrations` array.
    ```javascript
    // astro.config.mjs
    import { defineConfig } from 'astro/config';
    import tutorialkit from '@tutorialkit/astro';
    import react from "@astrojs/react";
    import tailwind from "@astrojs/tailwind";

    export default defineConfig({
      integrations: [
        tutorialkit(), 
        react(), 
        tailwind()
      ]
    });
    ```

4.  **Set up Content Directory Structure:**
    Tutorials are typically authored as Markdown files (`.md` or `.mdx`) within a designated content directory (e.g., `src/content/tutorials/`). Each tutorial can be a folder containing its steps and assets.

5.  **Configure WebContainer for Code Execution:**
    WebContainer is used by TutorialKit for running code examples. Ensure your environment supports cross-origin isolation as detailed in the WebContainer integration guide. TutorialKit handles much of the WebContainer setup internally when you use its components.

6.  **Theme and Styling Customization:**
    TutorialKit uses Tailwind CSS. You can customize the theme by modifying your `tailwind.config.cjs` file. The `@tutorialkit/theme` package provides defaults that can be extended.

#### 4.1.1 Advanced Configuration Examples

**A. Theming and Styling:**

TutorialKit is built with Tailwind CSS, making it highly customizable. You can override or extend the default theme provided by `@tutorialkit/theme`.

*   **Modify `tailwind.config.cjs`:**
    ```javascript
    // tailwind.config.cjs
    const tutorialKitTheme = require('@tutorialkit/theme/tailwind.config.js');

    module.exports = {
      content: [
        './src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}',
        './node_modules/@tutorialkit/components/src/**/*.{js,jsx,ts,tsx}',
        // Add other paths that include Tailwind classes
      ],
      theme: {
        extend: {
          // Override or extend TutorialKit's default theme
          colors: {
            'tk-primary': '#FF6B6B', // Example: Change primary color
            'tk-surface': '#F0F4F8', // Example: Change surface color
            'custom-accent': '#4ECDC4',
          },
          fontFamily: {
            sans: ['Inter', ...tutorialKitTheme.theme.extend.fontFamily.sans],
            mono: ['Fira Code', ...tutorialKitTheme.theme.extend.fontFamily.mono],
          }
        },
      },
      plugins: [
        require('@tailwindcss/typography'),
        // Potentially add TutorialKit's Tailwind plugin if it exposes one for specific component styles
      ],
    };
    ```
*   **Custom CSS:** For more complex styling, you can add custom CSS in your Astro project's global stylesheets or component-specific styles.

**B. Internationalization (i18n):**

While TutorialKit itself might not have a dedicated i18n system out-of-the-box for its UI components, you can implement i18n for your tutorial *content* and surrounding Astro application using standard Astro i18n practices.

*   **Astro i18n Routing:** Use Astro's built-in routing capabilities or libraries like `astro-i18n` to manage localized routes and content.
    *   Structure your content: `src/content/tutorials/en/my-tutorial/` and `src/content/tutorials/es/my-tutorial/`.
    *   Use Astro's `getStaticPaths` to generate pages for each locale.
*   **UI Strings:** For UI strings outside the Markdown content (e.g., in custom Astro components wrapping TutorialKit), manage translations using your chosen i18n library (e.g., `i18next`, `lingui`).

**C. Advanced Editor (Monaco) Configuration:**

TutorialKit components that use a code editor often rely on Monaco Editor. You can pass options to customize its behavior.

*   **Passing Options via Component Props:** When using a TutorialKit component (e.g., `<CodeEditor>`, `<InteractiveCodeBlock>`), check its documentation for props that allow passing Monaco editor options.
    ```jsx
    // Example in an .mdx file or React component within Astro
    import { CodeEditor } from '@tutorialkit/components';

    const editorOptions = {
      fontSize: 14,
      minimap: { enabled: false },
      wordWrap: 'on',
      // Add any other valid Monaco Editor options
    };

    <CodeEditor initialCode="console.log('Hello');" language="javascript" editorOptions={editorOptions} />
    ```
*   **Global Configuration (if available):** Some frameworks allow global Monaco settings. Refer to TutorialKit's documentation or its Astro integration for possibilities.

**D. WebContainer Terminal Customization:**

If TutorialKit exposes props for customizing the WebContainer terminal (e.g., Xterm.js options):

*   **Component Props:** Similar to the editor, look for props on terminal-related components.
    ```jsx
    // Example
    import { Terminal } from '@tutorialkit/components'; // Assuming such a component exists

    const terminalOptions = {
      fontSize: 13,
      cursorBlink: true,
      theme: {
        background: '#232428',
        foreground: '#F8F8F2',
      }
    };

    <Terminal /* ...other props... */ terminalOptions={terminalOptions} />
    ```
*   **Direct WebContainer API:** For very advanced scenarios, if you are interacting with the WebContainer instance directly (perhaps in custom components), you can use the WebContainer API's `spawn` method with options to control the pseudo-terminal (PTY).

### 4.2 Tutorial Content Structure
1. Design tutorial metadata schema
2. Create lesson hierarchy and navigation
3. Implement step-by-step progression
4. Set up code validation and testing
5. Configure progress tracking and persistence

### 4.3 Interactive Code Environment
1. Integrate Monaco Editor for code editing
2. Set up WebContainer for code execution
3. Implement live preview and output display
4. Create file system management
5. Add debugging and error handling

### 4.4 User Experience Features
1. Implement tutorial navigation and breadcrumbs
2. Create progress indicators and completion tracking
3. Add hint system and help documentation
4. Implement user preferences and settings
5. Create responsive design for mobile devices

### 4.5 Content Management System
1. Set up tutorial authoring tools
2. Implement content versioning and updates
3. Create template system for common patterns
4. Add content validation and testing
5. Implement automated deployment pipeline

## 5. Core Code Example

### 5.1 Astro Configuration
```typescript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import tutorialkit from '@tutorialkit/astro';

export default defineConfig({
  integrations: [
    react(),
    tailwind(),
    tutorialkit({
      // TutorialKit configuration
      contentDir: './src/content/tutorials',
      defaultTemplate: 'default',
      webContainer: {
        enabled: true,
        origin: process.env.WEBCONTAINER_ORIGIN || 'http://localhost:4321'
      },
      theme: {
        colors: {
          primary: '#3b82f6',
          secondary: '#64748b',
          accent: '#f59e0b'
        },
        fonts: {
          sans: ['Inter', 'system-ui', 'sans-serif'],
          mono: ['JetBrains Mono', 'Consolas', 'monospace']
        }
      },
      features: {
        progressTracking: true,
        codeValidation: true,
        livePreview: true,
        fileExplorer: true,
        terminal: true
      }
    })
  ],
  vite: {
    optimizeDeps: {
      include: ['@stackblitz/webcontainer-core']
    },
    server: {
      headers: {
        'Cross-Origin-Embedder-Policy': 'require-corp',
        'Cross-Origin-Opener-Policy': 'same-origin'
      }
    }
  }
});
```

### 5.2 Tutorial Content Schema
```typescript
// src/types/tutorial.ts
export interface TutorialMetadata {
  title: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  duration: number; // in minutes
  tags: string[];
  prerequisites: string[];
  learningObjectives: string[];
  author: {
    name: string;
    avatar?: string;
    bio?: string;
  };
  version: string;
  lastUpdated: string;
  featured?: boolean;
}

export interface TutorialStep {
  id: string;
  title: string;
  description: string;
  content: string; // Markdown content
  code?: {
    files: Record<string, string>;
    solution?: Record<string, string>;
    validation?: string; // Validation script
  };
  hints?: string[];
  resources?: {
    title: string;
    url: string;
    type: 'documentation' | 'video' | 'article';
  }[];
  estimatedTime?: number;
}

export interface Tutorial {
  id: string;
  metadata: TutorialMetadata;
  steps: TutorialStep[];
  template: string;
  config: {
    webContainer?: {
      enabled: boolean;
      template?: string;
      dependencies?: Record<string, string>;
    };
    editor?: {
      theme: string;
      fontSize: number;
      wordWrap: boolean;
    };
  };
}

// Tutorial progress tracking
export interface TutorialProgress {
  tutorialId: string;
  userId: string;
  currentStep: number;
  completedSteps: number[];
  startedAt: string;
  lastAccessedAt: string;
  completedAt?: string;
  timeSpent: number; // in seconds
  codeSubmissions: {
    stepId: string;
    code: Record<string, string>;
    timestamp: string;
    passed: boolean;
  }[];
}
```

### 5.3 Tutorial Runtime Implementation
```typescript
// src/components/TutorialRuntime.tsx
import React, { useState, useEffect, useCallback } from 'react';
import { WebContainer } from '@stackblitz/webcontainer-core';
import { Editor } from '@monaco-editor/react';
import type { Tutorial, TutorialStep, TutorialProgress } from '~/types/tutorial';

interface TutorialRuntimeProps {
  tutorial: Tutorial;
  initialProgress?: TutorialProgress;
  onProgressUpdate: (progress: TutorialProgress) => void;
}

export function TutorialRuntime({ 
  tutorial, 
  initialProgress, 
  onProgressUpdate 
}: TutorialRuntimeProps) {
  const [currentStepIndex, setCurrentStepIndex] = useState(initialProgress?.currentStep || 0);
  const [webContainer, setWebContainer] = useState<WebContainer | null>(null);
  const [files, setFiles] = useState<Record<string, string>>({});
  const [output, setOutput] = useState<string>('');
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState<TutorialProgress>(
    initialProgress || {
      tutorialId: tutorial.id,
      userId: '', // Set from auth context
      currentStep: 0,
      completedSteps: [],
      startedAt: new Date().toISOString(),
      lastAccessedAt: new Date().toISOString(),
      timeSpent: 0,
      codeSubmissions: []
    }
  );

  const currentStep = tutorial.steps[currentStepIndex];

  // Initialize WebContainer
  useEffect(() => {
    async function initWebContainer() {
      if (!tutorial.config.webContainer?.enabled) return;

      try {
        const container = await WebContainer.boot();
        setWebContainer(container);

        // Set up initial files
        if (currentStep.code?.files) {
          await setupFiles(container, currentStep.code.files);
          setFiles(currentStep.code.files);
        }
      } catch (error) {
        console.error('Failed to initialize WebContainer:', error);
      }
    }

    initWebContainer();
  }, [tutorial.id]);

  // Update files when step changes
  useEffect(() => {
    if (webContainer && currentStep.code?.files) {
      setupFiles(webContainer, currentStep.code.files);
      setFiles(currentStep.code.files);
    }
  }, [currentStepIndex, webContainer]);

  const setupFiles = async (container: WebContainer, fileMap: Record<string, string>) => {
    for (const [path, content] of Object.entries(fileMap)) {
      await container.fs.writeFile(path, content);
    }
  };

  const runCode = useCallback(async () => {
    if (!webContainer) return;

    setIsRunning(true);
    setOutput('');

    try {
      // Write current files to container
      for (const [path, content] of Object.entries(files)) {
        await webContainer.fs.writeFile(path, content);
      }

      // Run the code (assuming npm start or similar)
      const process = await webContainer.spawn('npm', ['start']);
      
      process.output.pipeTo(
        new WritableStream({
          write(data) {
            setOutput(prev => prev + data);
          }
        })
      );

      await process.exit;
    } catch (error) {
      setOutput(`Error: ${error}`);
    } finally {
      setIsRunning(false);
    }
  }, [webContainer, files]);

  const validateCode = useCallback(async () => {
    if (!currentStep.code?.validation) return true;

    try {
      // Run validation script
      const validationResult = await webContainer?.spawn('node', ['-e', currentStep.code.validation]);
      return validationResult?.exit === 0;
    } catch (error) {
      console.error('Validation failed:', error);
      return false;
    }
  }, [webContainer, currentStep]);

  const nextStep = useCallback(async () => {
    const isValid = await validateCode();
    
    if (!isValid) {
      alert('Please complete the current step before proceeding.');
      return;
    }

    const newProgress = {
      ...progress,
      currentStep: currentStepIndex + 1,
      completedSteps: [...progress.completedSteps, currentStepIndex],
      lastAccessedAt: new Date().toISOString(),
      codeSubmissions: [
        ...progress.codeSubmissions,
        {
          stepId: currentStep.id,
          code: files,
          timestamp: new Date().toISOString(),
          passed: true
        }
      ]
    };

    setProgress(newProgress);
    onProgressUpdate(newProgress);
    setCurrentStepIndex(currentStepIndex + 1);
  }, [currentStepIndex, progress, files, validateCode, onProgressUpdate]);

  const previousStep = useCallback(() => {
    if (currentStepIndex > 0) {
      setCurrentStepIndex(currentStepIndex - 1);
    }
  }, [currentStepIndex]);

  const updateFile = useCallback((path: string, content: string) => {
    setFiles(prev => ({ ...prev, [path]: content }));
  }, []);

  return (
    <div className="tutorial-runtime flex h-screen">
      {/* Sidebar with tutorial content */}
      <div className="w-1/3 bg-gray-50 p-6 overflow-y-auto">
        <div className="mb-4">
          <h1 className="text-2xl font-bold text-gray-900">{tutorial.metadata.title}</h1>
          <div className="flex items-center mt-2 text-sm text-gray-600">
            <span>Step {currentStepIndex + 1} of {tutorial.steps.length}</span>
            <div className="ml-4 flex-1 bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentStepIndex + 1) / tutorial.steps.length) * 100}%` }}
              />
            </div>
          </div>
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-3">{currentStep.title}</h2>
          <div 
            className="prose prose-sm max-w-none"
            dangerouslySetInnerHTML={{ __html: currentStep.content }}
          />
        </div>

        {currentStep.hints && (
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-700 mb-2">Hints</h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
              {currentStep.hints.map((hint, index) => (
                <li key={index}>{hint}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="flex space-x-3">
          <button
            onClick={previousStep}
            disabled={currentStepIndex === 0}
            className="px-4 py-2 bg-gray-300 text-gray-700 rounded disabled:opacity-50"
          >
            Previous
          </button>
          <button
            onClick={nextStep}
            disabled={currentStepIndex === tutorial.steps.length - 1}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Next Step
          </button>
        </div>
      </div>

      {/* Code editor and preview */}
      <div className="flex-1 flex flex-col">
        {/* File tabs */}
        <div className="flex border-b border-gray-200">
          {Object.keys(files).map(filename => (
            <button
              key={filename}
              className="px-4 py-2 text-sm border-r border-gray-200 hover:bg-gray-50"
            >
              {filename}
            </button>
          ))}
        </div>

        {/* Editor */}
        <div className="flex-1 flex">
          <div className="w-1/2 border-r border-gray-200">
            <Editor
              height="100%"
              defaultLanguage="javascript"
              value={files[Object.keys(files)[0]] || ''}
              onChange={(value) => updateFile(Object.keys(files)[0], value || '')}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                wordWrap: 'on',
                automaticLayout: true
              }}
            />
          </div>

          {/* Preview/Output */}
          <div className="w-1/2 flex flex-col">
            <div className="flex items-center justify-between p-3 border-b border-gray-200">
              <h3 className="font-medium text-gray-700">Output</h3>
              <button
                onClick={runCode}
                disabled={isRunning}
                className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700 disabled:opacity-50"
              >
                {isRunning ? 'Running...' : 'Run Code'}
              </button>
            </div>
            <div className="flex-1 p-4 bg-black text-green-400 font-mono text-sm overflow-y-auto">
              <pre>{output || 'Click "Run Code" to see output...'}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

### 5.4 Tutorial Content Management
```typescript
// src/lib/tutorialManager.ts
import type { Tutorial, TutorialProgress } from '~/types/tutorial';
import { supabaseService } from '~/lib/supabase/client';

export class TutorialManager {
  private tutorials: Map<string, Tutorial> = new Map();
  private progressCache: Map<string, TutorialProgress> = new Map();

  async loadTutorial(tutorialId: string): Promise<Tutorial | null> {
    // Check cache first
    if (this.tutorials.has(tutorialId)) {
      return this.tutorials.get(tutorialId)!;
    }

    try {
      // Load from database or content files
      const tutorial = await this.fetchTutorialContent(tutorialId);
      if (tutorial) {
        this.tutorials.set(tutorialId, tutorial);
      }
      return tutorial;
    } catch (error) {
      console.error('Failed to load tutorial:', error);
      return null;
    }
  }

  async fetchTutorialContent(tutorialId: string): Promise<Tutorial | null> {
    // This would typically load from your content management system
    // For now, we'll simulate loading from a content directory
    try {
      const response = await fetch(`/api/tutorials/${tutorialId}`);
      if (!response.ok) return null;
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch tutorial content:', error);
      return null;
    }
  }

  async getUserProgress(userId: string, tutorialId: string): Promise<TutorialProgress | null> {
    const cacheKey = `${userId}-${tutorialId}`;
    
    if (this.progressCache.has(cacheKey)) {
      return this.progressCache.get(cacheKey)!;
    }

    try {
      const progress = await supabaseService.query('tutorial_progress')
        .select('*')
        .eq('user_id', userId)
        .eq('tutorial_id', tutorialId)
        .single();

      if (progress.data) {
        this.progressCache.set(cacheKey, progress.data);
        return progress.data;
      }
    } catch (error) {
      console.error('Failed to load user progress:', error);
    }

    return null;
  }

  async saveProgress(progress: TutorialProgress): Promise<void> {
    try {
      const cacheKey = `${progress.userId}-${progress.tutorialId}`;
      
      // Update cache
      this.progressCache.set(cacheKey, progress);

      // Save to database
      await supabaseService.client
        .from('tutorial_progress')
        .upsert(progress, {
          onConflict: 'user_id,tutorial_id'
        });
    } catch (error) {
      console.error('Failed to save progress:', error);
      throw error;
    }
  }

  async getTutorialList(filters?: {
    difficulty?: string;
    tags?: string[];
    featured?: boolean;
  }): Promise<Tutorial[]> {
    try {
      let query = supabaseService.client
        .from('tutorials')
        .select('*')
        .eq('published', true);

      if (filters?.difficulty) {
        query = query.eq('difficulty', filters.difficulty);
      }

      if (filters?.featured) {
        query = query.eq('featured', true);
      }

      if (filters?.tags && filters.tags.length > 0) {
        query = query.contains('tags', filters.tags);
      }

      const { data, error } = await query.order('created_at', { ascending: false });
      
      if (error) throw error;
      return data || [];
    } catch (error) {
      console.error('Failed to fetch tutorial list:', error);
      return [];
    }
  }

  async searchTutorials(searchTerm: string): Promise<Tutorial[]> {
    try {
      const { data, error } = await supabaseService.client
        .from('tutorials')
        .select('*')
        .or(`title.ilike.%${searchTerm}%,description.ilike.%${searchTerm}%,tags.cs.{${searchTerm}}`)
        .eq('published', true)
        .order('created_at', { ascending: false });

      if (error) throw error;
      return data || [];
    } catch (error) {
      console.error('Failed to search tutorials:', error);
      return [];
    }
  }

  async createTutorial(tutorial: Omit<Tutorial, 'id'>): Promise<Tutorial> {
    try {
      const { data, error } = await supabaseService.client
        .from('tutorials')
        .insert({
          ...tutorial,
          created_at: new Date().toISOString(),
          published: false
        })
        .select()
        .single();

      if (error) throw error;
      
      const newTutorial = data as Tutorial;
      this.tutorials.set(newTutorial.id, newTutorial);
      return newTutorial;
    } catch (error) {
      console.error('Failed to create tutorial:', error);
      throw error;
    }
  }

  async updateTutorial(tutorialId: string, updates: Partial<Tutorial>): Promise<Tutorial> {
    try {
      const { data, error } = await supabaseService.client
        .from('tutorials')
        .update({
          ...updates,
          updated_at: new Date().toISOString()
        })
        .eq('id', tutorialId)
        .select()
        .single();

      if (error) throw error;
      
      const updatedTutorial = data as Tutorial;
      this.tutorials.set(tutorialId, updatedTutorial);
      return updatedTutorial;
    } catch (error) {
      console.error('Failed to update tutorial:', error);
      throw error;
    }
  }

  // Analytics and reporting
  async getTutorialAnalytics(tutorialId: string) {
    try {
      const { data, error } = await supabaseService.client
        .from('tutorial_progress')
        .select('*')
        .eq('tutorial_id', tutorialId);

      if (error) throw error;

      const progress = data || [];
      const totalUsers = progress.length;
      const completedUsers = progress.filter(p => p.completed_at).length;
      const averageTimeSpent = progress.reduce((sum, p) => sum + p.time_spent, 0) / totalUsers;
      const completionRate = (completedUsers / totalUsers) * 100;

      return {
        totalUsers,
        completedUsers,
        completionRate,
        averageTimeSpent,
        stepCompletionRates: this.calculateStepCompletionRates(progress)
      };
    } catch (error) {
      console.error('Failed to get tutorial analytics:', error);
      return null;
    }
  }

  private calculateStepCompletionRates(progressData: TutorialProgress[]) {
    const stepCounts: Record<number, number> = {};
    
    progressData.forEach(progress => {
      progress.completedSteps.forEach(stepIndex => {
        stepCounts[stepIndex] = (stepCounts[stepIndex] || 0) + 1;
      });
    });

    return stepCounts;
  }
}

export const tutorialManager = new TutorialManager();
```

### 5.5 Tutorial API Routes
```typescript
// src/pages/api/tutorials/[id].ts
import type { APIRoute } from 'astro';
import { tutorialManager } from '~/lib/tutorialManager';

export const GET: APIRoute = async ({ params, request }) => {
  const tutorialId = params.id;
  
  if (!tutorialId) {
    return new Response(JSON.stringify({ error: 'Tutorial ID required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const tutorial = await tutorialManager.loadTutorial(tutorialId);
    
    if (!tutorial) {
      return new Response(JSON.stringify({ error: 'Tutorial not found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    return new Response(JSON.stringify(tutorial), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};

export const PUT: APIRoute = async ({ params, request }) => {
  const tutorialId = params.id;
  
  if (!tutorialId) {
    return new Response(JSON.stringify({ error: 'Tutorial ID required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const updates = await request.json();
    const tutorial = await tutorialManager.updateTutorial(tutorialId, updates);
    
    return new Response(JSON.stringify(tutorial), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: 'Failed to update tutorial' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};

// src/pages/api/tutorials/progress.ts
export const POST: APIRoute = async ({ request }) => {
  try {
    const progress = await request.json();
    await tutorialManager.saveProgress(progress);
    
    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: 'Failed to save progress' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
```

## 6. Common Pitfalls & Error Handling

### 6.1 WebContainer Integration Issues
- **Problem**: WebContainer fails to boot or execute code
- **Solution**: Ensure proper CORS headers and origin configuration
- **Prevention**: Implement fallback modes and error recovery

### 6.2 Content Synchronization
- **Problem**: Tutorial content becomes out of sync with code examples
- **Solution**: Implement automated testing and validation
- **Detection**: Set up content validation pipelines

### 6.3 Progress Tracking Reliability
- **Problem**: User progress is lost or inconsistent
- **Solution**: Implement robust state management and persistence
- **Prevention**: Use optimistic updates with conflict resolution

### 6.4 Performance with Large Tutorials
- **Problem**: Slow loading and execution with complex tutorials
- **Solution**: Implement lazy loading and code splitting
- **Optimization**: Use virtual scrolling and progressive enhancement

## 7. Performance Optimization

### 7.1 Content Loading
- Implement progressive loading of tutorial steps
- Use code splitting for large tutorials
- Cache tutorial content and assets

### 7.2 WebContainer Optimization
- Reuse WebContainer instances when possible
- Implement container pooling for multiple users
- Optimize file system operations

### 7.3 Editor Performance
- Use Monaco Editor's lazy loading features
- Implement virtual scrolling for large files
- Optimize syntax highlighting and IntelliSense

## 8. Integration with Genesis Engine

### 8.1 AI-Powered Tutorial Generation
- Use Genesis agents to create tutorial content
- Implement automated code example generation
- Create personalized learning paths

### 8.2 Multi-Agent Tutorial Assistance
- Deploy teaching agents for real-time help
- Implement code review and feedback agents
- Create adaptive difficulty adjustment

### 8.3 Collaborative Learning Features
- Enable multi-user tutorial sessions
- Implement peer review and discussion
- Create mentor-student interaction tools

---

*Implementation Status: Ready for Genesis Engine integration*  
*Next Steps: Set up tutorial authoring tools and AI-powered content generation*