# Bolt.diy Hooks System & API Architecture Analysis

## Overview
This document analyzes Bolt.diy's comprehensive hook system and API architecture, providing insights for building a robust agent-centric system in sentient-core.

## Hook System Architecture

### 1. Hook Categories & Organization

#### Core Hook Structure
```typescript
// app/lib/hooks/index.ts - Central Export Pattern
export * from './usePromptEnhancer';
export * from './useShortcuts';
export * from './StickToBottom';
export * from './useEditChatDescription';
export { default } from './useViewport';
export { useUpdateCheck } from './useUpdateCheck';
export { useFeatures } from './useFeatures';
export { useNotifications } from './useNotifications';
export { useConnectionStatus } from './useConnectionStatus';
export { useDebugStatus } from './useDebugStatus';
```

#### Hook Categories
1. **Settings & Configuration**: `useSettings`, `useFeatures`
2. **Data Operations**: `useDataOperations`, `useIndexedDB`
3. **External Integrations**: `useGit`, `useSupabaseConnection`
4. **UI & UX**: `useShortcuts`, `useViewport`, `StickToBottom`
5. **System Monitoring**: `useConnectionStatus`, `useNotifications`, `useDebugStatus`
6. **Development Tools**: `useUpdateCheck`, `usePromptEnhancer`

### 2. Settings Management Hook

#### Comprehensive Settings Architecture
```typescript
// app/lib/hooks/useSettings.ts
export interface UseSettingsReturn {
  // Theme and UI settings
  setTheme: (theme: Settings['theme']) => void;
  setLanguage: (language: string) => void;
  setNotifications: (enabled: boolean) => void;
  setEventLogs: (enabled: boolean) => void;
  setTimezone: (timezone: string) => void;
  settings: Settings;

  // Provider settings
  providers: Record<string, IProviderConfig>;
  activeProviders: ProviderInfo[];
  updateProviderSettings: (provider: string, config: IProviderSetting) => void;

  // Debug and development settings
  debug: boolean;
  enableDebugMode: (enabled: boolean) => void;
  eventLogs: boolean;
  promptId: string;
  setPromptId: (promptId: string) => void;
  isLatestBranch: boolean;
  enableLatestBranch: (enabled: boolean) => void;
  autoSelectTemplate: boolean;
  setAutoSelectTemplate: (enabled: boolean) => void;
  contextOptimizationEnabled: boolean;
  enableContextOptimization: (enabled: boolean) => void;

  // Tab configuration
  tabConfiguration: TabWindowConfig;
  updateTabConfiguration: (config: TabVisibilityConfig) => void;
  resetTabConfiguration: () => void;
}
```

#### Settings Persistence Pattern
```typescript
const [settings, setSettings] = useState<Settings>(() => {
  const storedSettings = getLocalStorage('settings');
  return {
    theme: storedSettings?.theme || 'system',
    language: storedSettings?.language || 'en',
    notifications: storedSettings?.notifications ?? true,
    eventLogs: storedSettings?.eventLogs ?? true,
    timezone: storedSettings?.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone,
    tabConfiguration,
  };
});

// Auto-sync with stores
useEffect(() => {
  const active = Object.entries(providers)
    .filter(([_key, provider]) => provider.settings.enabled)
    .map(([_k, p]) => p);
  setActiveProviders(active);
}, [providers]);
```

### 3. Data Operations Hook

#### Comprehensive Data Management
```typescript
// app/lib/hooks/useDataOperations.ts
export function useDataOperations({
  onReloadSettings,
  onReloadChats,
  onResetSettings,
  onResetChats,
  customDb,
}: UseDataOperationsProps = {}) {
  const { db: defaultDb } = useIndexedDB();
  const db = customDb || defaultDb;
  
  const [isExporting, setIsExporting] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [isResetting, setIsResetting] = useState(false);
  const [isDownloadingTemplate, setIsDownloadingTemplate] = useState(false);
  const [progressMessage, setProgressMessage] = useState<string>('');
  const [progressPercent, setProgressPercent] = useState<number>(0);
  const [lastOperation, setLastOperation] = useState<{ type: string; data: any } | null>(null);
}
```

#### Progress Tracking System
```typescript
const showProgress = useCallback((message: string, percent: number) => {
  setProgressMessage(message);
  setProgressPercent(percent);

  // Dismiss any existing progress toast before showing a new one
  toast.dismiss('progress-toast');

  toast.loading(`${message} (${percent}%)`, {
    position: 'bottom-right',
    autoClose: 3000,
    toastId: 'progress-toast', // Use the same ID for all progress messages
  });
}, []);

const handleExportSettings = useCallback(async () => {
  setIsExporting(true);
  setProgressPercent(0);

  try {
    showProgress('Exporting settings', 25);
    const settingsData = await ImportExportService.exportSettings();
    
    showProgress('Creating file', 50);
    const blob = new Blob([JSON.stringify(settingsData, null, 2)], {
      type: 'application/json',
    });
    
    showProgress('Downloading', 75);
    // File download logic
    
    showProgress('Complete', 100);
  } catch (error) {
    // Error handling
  } finally {
    setIsExporting(false);
  }
}, [showProgress]);
```

### 4. Git Integration Hook

#### WebContainer Git Operations
```typescript
// app/lib/hooks/useGit.ts
export function useGit() {
  const [ready, setReady] = useState(false);
  const [webcontainer, setWebcontainer] = useState<WebContainer>();
  const [fs, setFs] = useState<PromiseFsClient>();
  const fileData = useRef<Record<string, { data: any; encoding?: string }>>({});
  
  useEffect(() => {
    webcontainerPromise.then((container) => {
      fileData.current = {};
      setWebcontainer(container);
      setFs(getFs(container, fileData));
      setReady(true);
    });
  }, []);
}
```

#### Git Authentication System
```typescript
const lookupSavedPassword = (url: string) => {
  const domain = url.split('/')[2];
  const gitCreds = Cookies.get(`git:${domain}`);

  if (!gitCreds) {
    return null;
  }

  try {
    const { username, password } = JSON.parse(gitCreds || '{}');
    return { username, password };
  } catch (error) {
    console.log(`Failed to parse Git Cookie ${error}`);
    return null;
  }
};

const saveGitAuth = (url: string, auth: GitAuth) => {
  const domain = url.split('/')[2];
  Cookies.set(`git:${domain}`, JSON.stringify(auth));
};
```

#### Git Clone with Retry Logic
```typescript
const gitClone = useCallback(
  async (url: string, retryCount = 0) => {
    if (!webcontainer || !fs || !ready) {
      throw new Error('Webcontainer not initialized. Please try again later.');
    }

    const headers: { [x: string]: string } = {
      'User-Agent': 'bolt.diy',
    };

    const auth = lookupSavedPassword(url);
    if (auth) {
      headers.Authorization = `Basic ${Buffer.from(`${auth.username}:${auth.password}`).toString('base64')}`;
    }

    try {
      // Add retry delay
      if (retryCount > 0) {
        await new Promise((resolve) => setTimeout(resolve, 1000 * retryCount));
        console.log(`Retrying git clone (attempt ${retryCount + 1})...`);
      }

      await git.clone({
        fs,
        http,
        dir: webcontainer.workdir,
        url,
        depth: 1,
        singleBranch: true,
        corsProxy: '/api/git-proxy',
        headers,
        onProgress: (event) => {
          console.log('Git clone progress:', event);
        },
        onAuth: (url) => {
          // Interactive authentication
          return handleGitAuth(url);
        },
      });
    } catch (error) {
      if (retryCount < 3) {
        return gitClone(url, retryCount + 1);
      }
      throw error;
    }
  },
  [webcontainer, fs, ready],
);
```

### 5. Shortcuts & Keyboard Management

#### Global Shortcut System
```typescript
// app/lib/hooks/useShortcuts.ts
class ShortcutEventEmitter {
  #emitter = new EventTarget();

  dispatch(type: keyof Shortcuts) {
    this.#emitter.dispatchEvent(new Event(type));
  }

  on(type: keyof Shortcuts, cb: VoidFunction) {
    this.#emitter.addEventListener(type, cb);

    return () => {
      this.#emitter.removeEventListener(type, cb);
    };
  }
}

export const shortcutEventEmitter = new ShortcutEventEmitter();
```

#### Smart Input Detection
```typescript
const INPUT_ELEMENTS = ['input', 'textarea'];

const handleKeyDown = (event: KeyboardEvent): void => {
  // Don't trigger shortcuts when typing in input fields
  if (
    document.activeElement &&
    INPUT_ELEMENTS.includes(document.activeElement.tagName.toLowerCase()) &&
    !event.altKey && // Allow Alt combinations even in input fields
    !event.metaKey && // Allow Cmd/Win combinations even in input fields
    !event.ctrlKey // Allow Ctrl combinations even in input fields
  ) {
    return;
  }

  // Handle shortcuts
  for (const [name, shortcut] of Object.entries(shortcuts)) {
    const keyMatches =
      shortcut.key.toLowerCase() === event.key.toLowerCase() || 
      `Key${shortcut.key.toUpperCase()}` === event.code;

    // Handle ctrlOrMetaKey based on OS
    const ctrlOrMetaKeyMatches = shortcut.ctrlOrMetaKey
      ? (isMac && event.metaKey) || (!isMac && event.ctrlKey)
      : true;

    const modifiersMatch =
      ctrlOrMetaKeyMatches &&
      (shortcut.ctrlKey === undefined || shortcut.ctrlKey === event.ctrlKey) &&
      (shortcut.metaKey === undefined || shortcut.metaKey === event.metaKey) &&
      (shortcut.shiftKey === undefined || shortcut.shiftKey === event.shiftKey) &&
      (shortcut.altKey === undefined || shortcut.altKey === event.altKey);

    if (keyMatches && modifiersMatch) {
      if (shortcut.isPreventDefault) {
        event.preventDefault();
        event.stopPropagation();
      }

      shortcutEventEmitter.dispatch(name as keyof Shortcuts);
      shortcut.action();
      break;
    }
  }
};
```

### 6. Feature Management Hook

#### Feature Flag System
```typescript
// app/lib/hooks/useFeatures.ts
const VIEWED_FEATURES_KEY = 'bolt_viewed_features';

const getViewedFeatures = (): string[] => {
  try {
    const stored = localStorage.getItem(VIEWED_FEATURES_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
};

export const useFeatures = () => {
  const [hasNewFeatures, setHasNewFeatures] = useState(false);
  const [unviewedFeatures, setUnviewedFeatures] = useState<Feature[]>([]);
  const [viewedFeatureIds, setViewedFeatureIds] = useState<string[]>(() => getViewedFeatures());

  useEffect(() => {
    const checkNewFeatures = async () => {
      try {
        const features = await getFeatureFlags();
        const unviewed = features.filter((feature) => !viewedFeatureIds.includes(feature.id));
        setUnviewedFeatures(unviewed);
        setHasNewFeatures(unviewed.length > 0);
      } catch (error) {
        console.error('Failed to check for new features:', error);
      }
    };

    checkNewFeatures();
  }, [viewedFeatureIds]);

  const acknowledgeFeature = async (featureId: string) => {
    try {
      await markFeatureViewed(featureId);
      const newViewedIds = [...viewedFeatureIds, featureId];
      setViewedFeatureIds(newViewedIds);
      setViewedFeatures(newViewedIds);
      setUnviewedFeatures((prev) => prev.filter((feature) => feature.id !== featureId));
      setHasNewFeatures(unviewedFeatures.length > 1);
    } catch (error) {
      console.error('Failed to acknowledge feature:', error);
    }
  };
};
```

### 7. Connection & Status Monitoring

#### Connection Status Hook
```typescript
// app/lib/hooks/useConnectionStatus.ts
type ConnectionIssueType = 'disconnected' | 'high-latency' | null;

export const useConnectionStatus = () => {
  const [hasConnectionIssues, setHasConnectionIssues] = useState(false);
  const [currentIssue, setCurrentIssue] = useState<ConnectionIssueType>(null);
  const [acknowledgedIssue, setAcknowledgedIssue] = useState<string | null>(() => getAcknowledgedIssue());

  const checkStatus = async () => {
    try {
      const status = await checkConnection();
      const issue = !status.connected ? 'disconnected' : status.latency > 1000 ? 'high-latency' : null;

      setCurrentIssue(issue);
      setHasConnectionIssues(issue !== null && issue !== acknowledgedIssue);
    } catch (error) {
      console.error('Failed to check connection:', error);
      setCurrentIssue('disconnected');
      setHasConnectionIssues(true);
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 10 * 1000);
    return () => clearInterval(interval);
  }, [acknowledgedIssue]);
};
```

#### Notification System Hook
```typescript
// app/lib/hooks/useNotifications.ts
export const useNotifications = () => {
  const [hasUnreadNotifications, setHasUnreadNotifications] = useState(false);
  const [unreadNotifications, setUnreadNotifications] = useState<Notification[]>([]);
  const logs = useStore(logStore.logs);

  const checkNotifications = async () => {
    try {
      const notifications = await getNotifications();
      const unread = notifications.filter((n) => !logStore.isRead(n.id));
      setUnreadNotifications(unread);
      setHasUnreadNotifications(unread.length > 0);
    } catch (error) {
      console.error('Failed to check notifications:', error);
    }
  };

  useEffect(() => {
    checkNotifications();
    const interval = setInterval(checkNotifications, 60 * 1000);
    return () => clearInterval(interval);
  }, [logs]);
};
```

## API Architecture

### 1. Model Management API

#### Dynamic Model Discovery
```typescript
// app/routes/api.models.ts
export async function loader({
  request,
  params,
  context,
}: {
  request: Request;
  params: { provider?: string };
  context: { cloudflare?: { env: Record<string, string> } };
}): Promise<Response> {
  const llmManager = LLMManager.getInstance(context.cloudflare?.env);

  // Get client-side API keys and settings from cookies
  const cookieHeader = request.headers.get('Cookie');
  const apiKeys = getApiKeysFromCookie(cookieHeader);
  const providerSettings = getProviderSettingsFromCookie(cookieHeader);

  const { providers, defaultProvider } = getProviderInfo(llmManager);

  let modelList: ModelInfo[] = [];

  if (params.provider) {
    // Update models for specific provider
    const provider = llmManager.getProvider(params.provider);
    if (provider) {
      modelList = await llmManager.getModelListFromProvider(provider, {
        apiKeys,
        providerSettings,
        serverEnv: context.cloudflare?.env,
      });
    }
  } else {
    // Update all models
    modelList = await llmManager.updateModelList({
      apiKeys,
      providerSettings,
      serverEnv: context.cloudflare?.env,
    });
  }

  return json<ModelsResponse>({
    modelList,
    providers,
    defaultProvider,
  });
}
```

#### Provider Caching Strategy
```typescript
let cachedProviders: ProviderInfo[] | null = null;
let cachedDefaultProvider: ProviderInfo | null = null;

function getProviderInfo(llmManager: LLMManager) {
  if (!cachedProviders) {
    cachedProviders = llmManager.getAllProviders().map((provider) => ({
      name: provider.name,
      staticModels: provider.staticModels,
      getApiKeyLink: provider.getApiKeyLink,
      labelForGetApiKey: provider.labelForGetApiKey,
      icon: provider.icon,
    }));
  }

  if (!cachedDefaultProvider) {
    const defaultProvider = llmManager.getDefaultProvider();
    cachedDefaultProvider = {
      name: defaultProvider.name,
      staticModels: defaultProvider.staticModels,
      getApiKeyLink: defaultProvider.getApiKeyLink,
      labelForGetApiKey: defaultProvider.labelForGetApiKey,
      icon: defaultProvider.icon,
    };
  }

  return { providers: cachedProviders, defaultProvider: cachedDefaultProvider };
}
```

### 2. LLM Call API

#### Streaming & Non-Streaming Support
```typescript
// app/routes/api.llmcall.ts
async function llmCallAction({ context, request }: ActionFunctionArgs) {
  const { system, message, model, provider, streamOutput } = await request.json<{
    system: string;
    message: string;
    model: string;
    provider: ProviderInfo;
    streamOutput?: boolean;
  }>();

  // Validation
  if (!model || typeof model !== 'string') {
    throw new Response('Invalid or missing model', {
      status: 400,
      statusText: 'Bad Request',
    });
  }

  const cookieHeader = request.headers.get('Cookie');
  const apiKeys = getApiKeysFromCookie(cookieHeader);
  const providerSettings = getProviderSettingsFromCookie(cookieHeader);

  if (streamOutput) {
    try {
      const result = await streamText({
        options: { system },
        messages: [{ role: 'user', content: message }],
        env: context.cloudflare?.env as any,
        apiKeys,
        providerSettings,
      });

      return new Response(result.textStream, {
        status: 200,
        headers: {
          'Content-Type': 'text/plain; charset=utf-8',
        },
      });
    } catch (error: unknown) {
      if (error instanceof Error && error.message?.includes('API key')) {
        throw new Response('Invalid or missing API key', {
          status: 401,
          statusText: 'Unauthorized',
        });
      }
      throw new Response(null, {
        status: 500,
        statusText: 'Internal Server Error',
      });
    }
  }
  // Non-streaming logic...
}
```

### 3. Git Proxy API

#### CORS-Enabled Git Proxy
```typescript
// app/routes/api.git-proxy.$.ts
const ALLOW_HEADERS = [
  'accept-encoding', 'accept-language', 'accept', 'access-control-allow-origin',
  'authorization', 'cache-control', 'connection', 'content-length',
  'content-type', 'dnt', 'pragma', 'range', 'referer', 'user-agent',
  'x-authorization', 'x-http-method-override', 'x-requested-with',
];

const EXPOSE_HEADERS = [
  'accept-ranges', 'age', 'cache-control', 'content-length',
  'content-language', 'content-type', 'date', 'etag', 'expires',
  'last-modified', 'pragma', 'server', 'transfer-encoding', 'vary',
  'x-github-request-id', 'x-redirected-url',
];

async function handleProxyRequest(request: Request, path: string | undefined) {
  // Handle CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': ALLOW_HEADERS.join(', '),
        'Access-Control-Expose-Headers': EXPOSE_HEADERS.join(', '),
        'Access-Control-Max-Age': '86400',
      },
    });
  }

  // Extract domain and path
  const parts = path.match(/([^\/]+)\/?(.*)/);
  if (!parts) {
    return json({ error: 'Invalid path format' }, { status: 400 });
  }

  const domain = parts[1];
  const remainingPath = parts[2] || '';
  const url = new URL(request.url);
  const targetURL = `https://${domain}/${remainingPath}${url.search}`;

  // Filter and prepare headers
  const headers = new Headers();
  for (const header of ALLOW_HEADERS) {
    if (request.headers.has(header)) {
      headers.set(header, request.headers.get(header)!);
    }
  }

  // Proxy the request
  const response = await fetch(targetURL, {
    method: request.method,
    headers,
    body: request.body,
  });

  return response;
}
```

### 4. Deployment APIs

#### Netlify Deployment
```typescript
// app/routes/api.netlify-deploy.ts
export async function action({ request }: ActionFunctionArgs) {
  const { siteId, files, token, chatId } = await request.json() as DeployRequestBody & { token: string };

  if (!token) {
    return json({ error: 'Not connected to Netlify' }, { status: 401 });
  }

  let targetSiteId = siteId;
  let siteInfo: NetlifySiteInfo | undefined;

  // Create new site if needed
  if (!targetSiteId) {
    const siteName = `bolt-diy-${chatId}-${Date.now()}`;
    const createSiteResponse = await fetch('https://api.netlify.com/api/v1/sites', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: siteName,
        custom_domain: null,
      }),
    });

    if (!createSiteResponse.ok) {
      return json({ error: 'Failed to create site' }, { status: 400 });
    }

    const newSite = await createSiteResponse.json();
    targetSiteId = newSite.id;
    siteInfo = {
      id: newSite.id,
      name: newSite.name,
      url: newSite.url,
      chatId,
    };
  }

  // Deploy files...
}
```

#### Supabase Integration
```typescript
// app/routes/api.supabase.ts
export const action: ActionFunction = async ({ request }) => {
  const { token } = await request.json();

  const projectsResponse = await fetch('https://api.supabase.com/v1/projects', {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!projectsResponse.ok) {
    return json({ error: 'Failed to fetch projects' }, { status: 401 });
  }

  const projects = await projectsResponse.json() as SupabaseProject[];

  // Deduplicate and sort projects
  const uniqueProjectsMap = new Map<string, SupabaseProject>();
  for (const project of projects) {
    if (!uniqueProjectsMap.has(project.id)) {
      uniqueProjectsMap.set(project.id, project);
    }
  }

  const uniqueProjects = Array.from(uniqueProjectsMap.values());
  uniqueProjects.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

  return json({
    user: { email: 'Connected', role: 'Admin' },
    stats: {
      projects: uniqueProjects,
      totalProjects: uniqueProjects.length,
    },
  });
};
```

### 5. System Diagnostics API

#### Comprehensive System Health Check
```typescript
// app/routes/api.system.diagnostics.ts
export const loader: LoaderFunction = async ({ request, context }) => {
  // Environment variables check
  const envVars = {
    hasGithubToken: Boolean(process.env.GITHUB_ACCESS_TOKEN || context.env?.GITHUB_ACCESS_TOKEN),
    hasNetlifyToken: Boolean(process.env.NETLIFY_TOKEN || context.env?.NETLIFY_TOKEN),
    nodeEnv: process.env.NODE_ENV,
  };

  // Cookie analysis
  const cookieHeader = request.headers.get('Cookie') || '';
  const cookies = cookieHeader.split(';').reduce((acc, cookie) => {
    const [key, value] = cookie.trim().split('=');
    if (key) acc[key] = value;
    return acc;
  }, {} as Record<string, string>);

  // External API connectivity tests
  let githubApiStatus;
  try {
    const githubResponse = await fetch('https://api.github.com/zen', {
      method: 'GET',
      headers: { Accept: 'application/vnd.github.v3+json' },
    });
    githubApiStatus = {
      isReachable: githubResponse.ok,
      status: githubResponse.status,
      statusText: githubResponse.statusText,
    };
  } catch (error) {
    githubApiStatus = {
      isReachable: false,
      error: error instanceof Error ? error.message : String(error),
    };
  }

  return json({
    envVars,
    cookies: {
      hasGithubToken: Boolean(cookies.githubToken),
      hasNetlifyToken: Boolean(cookies.netlifyToken),
    },
    apiConnectivity: {
      github: githubApiStatus,
      // Additional API tests...
    },
  });
};
```

## Integration Recommendations for Sentient-Core

### 1. Agent-Centric Hook System

#### Multi-Agent Settings Management
```typescript
// Proposed adaptation for sentient-core
export interface AgentSettingsReturn {
  // Agent-specific settings
  agentConfigs: Record<string, AgentConfig>;
  updateAgentConfig: (agentId: string, config: Partial<AgentConfig>) => void;
  
  // Global agent settings
  maxConcurrentAgents: number;
  setMaxConcurrentAgents: (count: number) => void;
  
  // Agent communication settings
  enableAgentToAgentComm: boolean;
  setAgentToAgentComm: (enabled: boolean) => void;
  
  // Resource management
  resourceLimits: AgentResourceLimits;
  updateResourceLimits: (limits: Partial<AgentResourceLimits>) => void;
}

export function useAgentSettings(): AgentSettingsReturn {
  const agentConfigs = useStore(agentConfigStore);
  const resourceLimits = useStore(resourceLimitsStore);
  
  const updateAgentConfig = useCallback((agentId: string, config: Partial<AgentConfig>) => {
    agentConfigStore.setKey(agentId, { ...agentConfigs[agentId], ...config });
    
    // Persist to SurrealDB
    persistAgentConfig(agentId, config);
  }, [agentConfigs]);
  
  return {
    agentConfigs,
    updateAgentConfig,
    resourceLimits,
    // ... other methods
  };
}
```

### 2. Agent Data Operations

#### Multi-Agent Data Management
```typescript
export function useAgentDataOperations() {
  const [agentStates, setAgentStates] = useState<Record<string, AgentState>>({});
  const [isBackingUp, setIsBackingUp] = useState(false);
  const [isRestoring, setIsRestoring] = useState(false);
  
  const backupAgentState = useCallback(async (agentId: string) => {
    setIsBackingUp(true);
    try {
      const agentData = await AgentDataService.exportAgentState(agentId);
      const blob = new Blob([JSON.stringify(agentData, null, 2)], {
        type: 'application/json',
      });
      
      // Save to file or SurrealDB
      await saveAgentBackup(agentId, blob);
      
      toast.success(`Agent ${agentId} state backed up successfully`);
    } catch (error) {
      toast.error(`Failed to backup agent ${agentId}: ${error.message}`);
    } finally {
      setIsBackingUp(false);
    }
  }, []);
  
  const restoreAgentState = useCallback(async (agentId: string, backupData: AgentBackup) => {
    setIsRestoring(true);
    try {
      await AgentDataService.restoreAgentState(agentId, backupData);
      
      // Update local state
      setAgentStates(prev => ({
        ...prev,
        [agentId]: backupData.state,
      }));
      
      toast.success(`Agent ${agentId} state restored successfully`);
    } catch (error) {
      toast.error(`Failed to restore agent ${agentId}: ${error.message}`);
    } finally {
      setIsRestoring(false);
    }
  }, []);
  
  return {
    agentStates,
    backupAgentState,
    restoreAgentState,
    isBackingUp,
    isRestoring,
  };
}
```

### 3. Agent Communication Hook

#### Inter-Agent Communication
```typescript
export function useAgentCommunication(agentId: string) {
  const [incomingMessages, setIncomingMessages] = useState<AgentMessage[]>([]);
  const [outgoingMessages, setOutgoingMessages] = useState<AgentMessage[]>([]);
  const [connectedAgents, setConnectedAgents] = useState<string[]>([]);
  
  const sendMessage = useCallback(async (targetAgentId: string, message: AgentMessage) => {
    try {
      await AgentCommunicationService.sendMessage(agentId, targetAgentId, message);
      
      setOutgoingMessages(prev => [...prev, {
        ...message,
        timestamp: Date.now(),
        status: 'sent',
      }]);
    } catch (error) {
      console.error(`Failed to send message to agent ${targetAgentId}:`, error);
    }
  }, [agentId]);
  
  const broadcastMessage = useCallback(async (message: AgentMessage) => {
    try {
      await AgentCommunicationService.broadcastMessage(agentId, message);
      
      setOutgoingMessages(prev => [...prev, {
        ...message,
        timestamp: Date.now(),
        status: 'broadcast',
      }]);
    } catch (error) {
      console.error('Failed to broadcast message:', error);
    }
  }, [agentId]);
  
  // Listen for incoming messages
  useEffect(() => {
    const unsubscribe = AgentCommunicationService.subscribeToMessages(agentId, (message) => {
      setIncomingMessages(prev => [...prev, message]);
    });
    
    return unsubscribe;
  }, [agentId]);
  
  return {
    incomingMessages,
    outgoingMessages,
    connectedAgents,
    sendMessage,
    broadcastMessage,
  };
}
```

### 4. Agent Status Monitoring

#### Comprehensive Agent Health Monitoring
```typescript
export function useAgentMonitoring() {
  const [agentStatuses, setAgentStatuses] = useState<Record<string, AgentStatus>>({});
  const [systemHealth, setSystemHealth] = useState<SystemHealth>({});
  
  const checkAgentHealth = useCallback(async (agentId: string) => {
    try {
      const health = await AgentHealthService.checkHealth(agentId);
      
      setAgentStatuses(prev => ({
        ...prev,
        [agentId]: {
          ...prev[agentId],
          health,
          lastChecked: Date.now(),
        },
      }));
      
      // Alert on critical issues
      if (health.status === 'critical') {
        toast.error(`Agent ${agentId} is in critical state: ${health.issues.join(', ')}`);
      }
    } catch (error) {
      console.error(`Failed to check health for agent ${agentId}:`, error);
    }
  }, []);
  
  const checkSystemHealth = useCallback(async () => {
    try {
      const health = await SystemHealthService.checkOverallHealth();
      setSystemHealth(health);
      
      // System-wide alerts
      if (health.memoryUsage > 0.9) {
        toast.warning('System memory usage is high (>90%)');
      }
      
      if (health.activeAgents > health.maxAgents * 0.8) {
        toast.warning('Approaching maximum agent capacity');
      }
    } catch (error) {
      console.error('Failed to check system health:', error);
    }
  }, []);
  
  // Periodic health checks
  useEffect(() => {
    const interval = setInterval(() => {
      checkSystemHealth();
      
      // Check each active agent
      Object.keys(agentStatuses).forEach(agentId => {
        if (agentStatuses[agentId].status === 'active') {
          checkAgentHealth(agentId);
        }
      });
    }, 30000); // Every 30 seconds
    
    return () => clearInterval(interval);
  }, [agentStatuses, checkAgentHealth, checkSystemHealth]);
  
  return {
    agentStatuses,
    systemHealth,
    checkAgentHealth,
    checkSystemHealth,
  };
}
```

## Key Takeaways

### Hook System Benefits
- **Modular Architecture**: Each hook handles a specific concern
- **Reusable Logic**: Hooks can be composed and extended
- **State Management**: Seamless integration with Nanostores
- **Error Handling**: Consistent error patterns across hooks
- **Performance**: Optimized with proper memoization and cleanup

### API Architecture Benefits
- **Flexible Routing**: Dynamic route parameters for extensibility
- **Cookie-based Auth**: Secure client-side credential management
- **CORS Support**: Comprehensive proxy system for external APIs
- **Error Handling**: Consistent error responses and logging
- **Caching Strategy**: Intelligent caching for performance

### Integration Strategy
1. **Adapt Hook Patterns**: Use similar patterns for agent-specific functionality
2. **Extend API Architecture**: Build on the routing and middleware patterns
3. **Implement Monitoring**: Use the diagnostic patterns for agent health
4. **Leverage Shortcuts**: Implement global shortcuts for agent management
5. **Build Communication**: Create inter-agent communication hooks

### Next Steps
1. **Part 5**: Persistence Layer & Database Integration
2. **Part 6**: Action System & Execution Engine
3. **Part 7**: Final Integration Roadmap

This hook and API architecture provides a solid foundation for building a comprehensive agent management system with robust monitoring, communication, and data management capabilities.