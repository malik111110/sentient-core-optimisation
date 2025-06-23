# WebContainer Integration Patterns

## Overview
This document captures the key patterns and implementation details for integrating WebContainer into Sentient Core, based on the `bolt.diy` implementation.

## Core Components

### 1. WebContainer Bootstrapping

```typescript
// app/lib/webcontainer/index.ts
import { WebContainer } from '@webcontainer/api';

export let webcontainer: Promise<WebContainer> = WebContainer.boot({
  coep: 'credentialless',
  workdirName: 'project',
  forwardPreviewErrors: true
});
```

Key points:
- Uses `WebContainer.boot()` to initialize the container
- `coep: 'credentialless'` enables cross-origin isolation
- `forwardPreviewErrors: true` enables error forwarding from iframes

### 2. Preview Component

```typescript
// app/routes/webcontainer.preview.$id.tsx
export default function WebContainerPreview() {
  const { previewId } = useLoaderData();
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [previewUrl, setPreviewUrl] = useState('');

  // Handle preview refresh
  const handleRefresh = useCallback(() => {
    if (iframeRef.current && previewUrl) {
      iframeRef.current.src = '';
      requestAnimationFrame(() => {
        if (iframeRef.current) {
          iframeRef.current.src = previewUrl;
        }
      });
    }
  }, [previewUrl]);

  // Set up preview URL and iframe
  useEffect(() => {
    const url = `https://${previewId}.local-credentialless.webcontainer-api.io`;
    setPreviewUrl(url);
    
    if (iframeRef.current) {
      iframeRef.current.src = url;
    }
  }, [previewId]);

  return (
    <div className="w-full h-full">
      <iframe
        ref={iframeRef}
        title="WebContainer Preview"
        className="w-full h-full border-none"
        sandbox="allow-scripts allow-forms allow-popups allow-modals allow-storage-access-by-user-activation allow-same-origin"
        allow="cross-origin-isolated"
        loading="eager"
      />
    </div>
  );
}
```

Key points:
- Uses an iframe to sandbox the preview
- Handles refresh by toggling the iframe src
- Uses `local-credentialless` subdomain for cross-origin isolation
- Configures sandbox permissions appropriately

### 3. File System Operations

```typescript
// app/utils/file-watcher.ts
export async function safeWatch(
  webcontainer: WebContainer, 
  pattern: string = '**/*', 
  callback: () => void
) {
  try {
    const watcher = await webcontainer.fs.watch(pattern, { persistent: true });
    watcher.on('*', callback);
    return () => watcher.close();
  } catch (error) {
    console.error('Error setting up file watcher:', error);
    // Fallback to polling
    const interval = setInterval(callback, 1000);
    return () => clearInterval(interval);
  }
}
```

Key points:
- Uses WebContainer's filesystem API for watching files
- Includes error handling with fallback to polling
- Returns cleanup function to stop watching

### 4. Error Handling

```typescript
// app/utils/stacktrace.ts
export function cleanStackTrace(stack: string): string {
  // Clean webcontainer URLs from stack traces
  const regex = /^https?:\/\/[^\/]+\.webcontainer-api\.io(\/.*)?$/;
  return stack.split('\n')
    .map(line => line.replace(regex, (_, path) => path || ''))
    .join('\n');
}
```

## Integration with Sentient Core

### 1. WebContainerTool Implementation

```python
# src/sentient_core/tools/webcontainer_tool.py
class WebContainerTool:
    def __init__(self):
        self.container = None
        self.preview_url = None
        
    async def initialize(self):
        if not self.container:
            self.container = await WebContainer.boot({
                'coep': 'credentialless',
                'workdirName': 'project',
                'forwardPreviewErrors': True
            })
            
    async def write_files(self, files: Dict[str, str]):
        """Write multiple files to the container"""
        await self.initialize()
        for path, content in files.items():
            await self.container.fs.write(path, content)
            
    async def start_preview(self, port: int = 3000):
        """Start the preview server"""
        await self.initialize()
        # Start the development server
        process = await self.container.spawn('npm', ['run', 'dev'])
        self.preview_url = f"https://{process.id}.local-credentialless.webcontainer-api.io"
        return self.preview_url
```

### 2. Preview Component

```python
# src/sentient_web/components/preview.py
class WebContainerPreview(Component):
    def __init__(self, tool: WebContainerTool):
        self.tool = tool
        self.iframe_id = f"preview-{str(uuid.uuid4())}"
        
    async def render(self):
        preview_url = await self.tool.start_preview()
        return html.Div([
            html.Iframe(
                id=self.iframe_id,
                src=preview_url,
                style={
                    'width': '100%',
                    'height': '100%',
                    'border': 'none',
                },
                sandbox="allow-scripts allow-forms allow-popups allow-modals allow-same-origin",
                allow="cross-origin-isolated"
            ),
            html.Script(f"""
                // Add auto-refresh logic here
                const iframe = document.getElementById('{self.iframe_id}');
                // ...
            """)
        ])
```

## Next Steps

1. **Error Handling**: Implement comprehensive error handling for container operations
2. **State Management**: Add state persistence for container state across page reloads
3. **Performance**: Implement lazy loading for large file operations
4. **Security**: Review and tighten sandbox permissions
5. **Testing**: Add integration tests for container operations

## References
- [WebContainer API Documentation](https://webcontainers.io/)
- [bolt.diy Implementation](https://github.com/stackblitz/bolt.diy)
