# E2B Sandbox Integration Patterns

## Overview
This document outlines the key patterns and implementation details for integrating E2B sandbox into Sentient Core, based on the `fragments` implementation.

## Core Components

### 1. Sandbox Initialization

```typescript
// app/api/sandbox/route.ts
import { Sandbox } from '@e2b/code-interpreter';

export async function POST(req: Request) {
  const { fragment, userID, teamID, accessToken } = await req.json();

  // Create sandbox with metadata and auth headers
  const sbx = await Sandbox.create(fragment.template, {
    metadata: {
      template: fragment.template,
      userID: userID ?? '',
      teamID: teamID ?? '',
    },
    timeoutMs: 10 * 60 * 1000, // 10 minutes
    ...(teamID && accessToken ? {
      headers: {
        'X-Supabase-Team': teamID,
        'X-Supabase-Token': accessToken,
      },
    } : {}),
  });

  // ... rest of the implementation
}
```

Key points:
- Uses `Sandbox.create()` with template ID
- Includes metadata for tracking
- Supports team-based authentication
- Configurable timeout

### 2. Template Configuration

```toml
# sandbox-templates/nextjs-developer/e2b.toml
template_id = "scwxnhs1apt5uj7na7db"
dockerfile = "e2b.Dockerfile"
template_name = "nextjs-developer"
start_cmd = "/compile_page.sh"
cpu_count = 4
memory_mb = 4_096
team_id = "460355b3-4f64-48f9-9a16-4442817f79f5"
```

### 3. Dockerfile Structure

```dockerfile
# sandbox-templates/nextjs-developer/e2b.Dockerfile
FROM node:21-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy and set up entrypoint
COPY compile_page.sh /compile_page.sh
RUN chmod +x /compile_page.sh

# Set up application
WORKDIR /home/user/nextjs-app
RUN npx create-next-app@14.2.20 . --ts --tailwind --no-eslint \
    --import-alias "@/*" --use-npm --no-app --no-src-dir

# Install additional dependencies
RUN npx shadcn@2.1.7 init -d
RUN npx shadcn@2.1.7 add --all
RUN npm install posthog-js

# Move to home directory
RUN mv /home/user/nextjs-app/* /home/user/ && \
    rm -rf /home/user/nextjs-app
```

## Integration with Sentient Core

### 1. E2BSandboxTool Implementation

```python
# src/sentient_core/tools/e2b_sandbox_tool.py
from typing import Dict, Optional, Any
import json
from pydantic import BaseModel, Field

class E2BSandboxInput(BaseModel):
    """Input for E2B sandbox operations"""
    code: str = Field(..., description="Code to execute in the sandbox")
    files: Optional[Dict[str, str]] = Field(
        None, 
        description="Files to write to the sandbox before execution"
    )
    template: str = Field(
        "python3", 
        description="Sandbox template to use (e.g., 'python3', 'nodejs')"
    )

class E2BSandboxTool:
    """Tool for interacting with E2B sandboxes"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("E2B_API_KEY")
        if not self.api_key:
            raise ValueError("E2B_API_KEY environment variable is required")
            
        self.client = None
        self.sandbox = None
        
    async def initialize(self):
        """Initialize the E2B client"""
        if not self.client:
            from e2b import Sandbox
            self.client = Sandbox
            
    async def create_sandbox(self, template: str) -> str:
        """Create a new sandbox"""
        await self.initialize()
        self.sandbox = await self.client.create(template)
        return self.sandbox.id
        
    async def write_files(self, files: Dict[str, str]):
        """Write files to the sandbox"""
        if not self.sandbox:
            raise RuntimeError("Sandbox not initialized. Call create_sandbox first.")
            
        for path, content in files.items():
            await self.sandbox.files.write(path, content)
            
    async def run_code(self, code: str) -> Dict[str, Any]:
        """Run code in the sandbox and return the result"""
        if not self.sandbox:
            raise RuntimeError("Sandbox not initialized. Call create_sandbox first.")
            
        result = await self.sandbox.run_code(code)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "error": result.error,
            "results": result.results
        }
        
    async def close(self):
        """Close the sandbox"""
        if self.sandbox:
            await self.sandbox.close()
            self.sandbox = None
            
    async def __aenter__(self):
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

# Example usage:
async def example_usage():
    async with E2BSandboxTool() as sandbox:
        await sandbox.create_sandbox("python3")
        
        # Write files if needed
        await sandbox.write_files({
            "app.py": "print('Hello from E2B!')"
        })
        
        # Run code
        result = await sandbox.run_code("python app.py")
        print(result["stdout"])  # Hello from E2B!
```

### 2. Integration with Agent Workflow

```python
# src/sentient_core/agents/backend_agent.py
class BackendDeveloperAgent(BaseAgent):
    """Agent for backend development tasks using E2B sandbox"""
    
    def __init__(self, sandbox_tool: Optional[E2BSandboxTool] = None):
        super().__init__()
        self.sandbox = sandbox_tool or E2BSandboxTool()
        
    async def execute_task(self, task: Task) -> str:
        """Execute a backend development task"""
        # Initialize sandbox
        await self.sandbox.initialize()
        await self.sandbox.create_sandbox("python3")
        
        try:
            # Write task files
            if task.files:
                await self.sandbox.write_files(task.files)
                
            # Run the task
            result = await self.sandbox.run_code(task.code)
            
            # Process result
            if result.get("error"):
                return f"Error: {result['error']}"
                
            return result["stdout"] or "Task completed successfully"
            
        finally:
            await self.sandbox.close()
```

## Best Practices

1. **Resource Management**
   - Always close sandboxes when done to avoid resource leaks
   - Use context managers (`async with`) when possible
   - Set appropriate timeouts for long-running operations

2. **Error Handling**
   - Handle sandbox creation and execution errors gracefully
   - Implement retries for transient failures
   - Validate inputs before sending to the sandbox

3. **Security**
   - Never expose API keys in client-side code
   - Validate and sanitize all inputs to the sandbox
   - Use the principle of least privilege for sandbox permissions

4. **Performance**
   - Reuse sandboxes when possible for multiple operations
   - Implement caching for frequently used templates
   - Monitor and optimize resource usage

## Next Steps

1. **Template Management**
   - Create custom templates for common use cases
   - Implement template versioning
   - Add template validation

2. **Monitoring**
   - Add logging for sandbox operations
   - Implement metrics collection
   - Set up alerts for failures

3. **Advanced Features**
   - Implement file upload/download support
   - Add support for custom environments
   - Implement collaborative editing

## References
- [E2B Documentation](https://e2b.dev/docs)
- [E2B SDK Reference](https://e2b.dev/docs/sdk/python)
- [Fragments Implementation](https://github.com/e2b-dev/fragments)
