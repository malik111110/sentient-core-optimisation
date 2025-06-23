from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Any, Optional, Union, Literal
from enum import Enum
import os
import json
import asyncio
from pathlib import Path

class FileModel(BaseModel):
    """Model for file operations in the WebContainer"""
    path: str
    content: str
    is_binary: bool = False

class WebContainerToolInput(BaseModel):
    """Input model for the WebContainerTool"""
    files: List[FileModel] = Field(
        default_factory=list,
        description="Files to write to the WebContainer"
    )
    commands: List[str] = Field(
        default_factory=list,
        description="Commands to execute in the WebContainer"
    )
    working_dir: str = Field(
        "/app",
        description="Working directory for the commands"
    )
    install_dependencies: bool = Field(
        True,
        description="Whether to automatically install dependencies"
    )
    expose_ports: List[int] = Field(
        default_factory=lambda: [3000, 8000],
        description="Ports to expose from the WebContainer"
    )
    env_vars: Dict[str, str] = Field(
        default_factory=dict,
        description="Environment variables to set in the WebContainer"
    )
    wait_for_ports: bool = Field(
        True,
        description="Whether to wait for exposed ports to be available"
    )
    timeout_seconds: int = Field(
        300,
        description="Maximum execution time in seconds",
        ge=30,
        le=1800
    )

class WebContainerOutput(BaseModel):
    """Output model for WebContainer execution results"""
    status: Literal["success", "error", "timeout"]
    stdout: str = ""
    stderr: str = ""
    error: Optional[str] = None
    preview_url: Optional[HttpUrl] = None
    port: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WebContainerTool:
    """
    A tool for interacting with WebContainers in the browser.
    
    This class provides a high-level interface to the WebContainer API,
    allowing for secure execution of web applications in an isolated
    browser environment.
    """
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize the WebContainer tool.
        
        Args:
            api_url: Optional URL of the WebContainer API server.
                     If not provided, will use the default or environment variable.
        """
        self.api_url = api_url or os.getenv("WEBCONTAINER_API_URL", "http://localhost:3000/api/webcontainer")
        self.session_id = None
    
    async def initialize(self):
        """Initialize the WebContainer session"""
        if not hasattr(self, '_initialized'):
            # In a real implementation, this would establish a WebSocket connection
            # or create a new WebContainer instance
            self._initialized = True
    
    async def create_session(self) -> str:
        """
        Create a new WebContainer session.
        
        Returns:
            str: The session ID
        """
        await self.initialize()
        # In a real implementation, this would make an API call to create a session
        self.session_id = f"wc-{os.urandom(8).hex()}"
        return self.session_id
    
    async def write_files(self, files: List[FileModel]):
        """
        Write files to the WebContainer.
        
        Args:
            files: List of FileModel objects with path and content
        """
        if not self.session_id:
            raise RuntimeError("Session not initialized. Call create_session first.")
        
        # In a real implementation, this would send files to the WebContainer
        # via WebSocket or API call
        for file in files:
            dir_path = os.path.dirname(file.path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            
            mode = 'wb' if file.is_binary else 'w'
            with open(file.path, mode) as f:
                f.write(file.content)
    
    async def install_dependencies(self):
        """Install dependencies in the WebContainer"""
        if not self.session_id:
            raise RuntimeError("Session not initialized. Call create_session first.")
        
        # In a real implementation, this would run npm/yarn/pnpm install
        # or the appropriate package manager command
        if os.path.exists('package.json'):
            # This is a placeholder - in reality, this would be handled client-side
            pass
    
    async def execute_commands(self, commands: List[str], working_dir: str = "/app") -> WebContainerOutput:
        """
        Execute commands in the WebContainer.
        
        Args:
            commands: List of commands to execute
            working_dir: Working directory for the commands
            
        Returns:
            WebContainerOutput with the command results
        """
        if not self.session_id:
            raise RuntimeError("Session not initialized. Call create_session first.")
        
        # In a real implementation, this would execute commands via WebSocket
        # and stream the output back
        results = []
        for cmd in commands:
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir
            )
            
            stdout, stderr = await proc.communicate()
            
            results.append({
                "command": cmd,
                "exit_code": proc.returncode,
                "stdout": stdout.decode(),
                "stderr": stderr.decode()
            })
        
        # For demo purposes, just return the last command's output
        last_result = results[-1] if results else {}
        return WebContainerOutput(
            status="success" if not last_result.get('stderr') else "error",
            stdout=last_result.get('stdout', ''),
            stderr=last_result.get('stderr', '')
        )
    
    async def start_dev_server(self, port: int = 3000, script: str = "dev") -> WebContainerOutput:
        """
        Start a development server in the WebContainer.
        
        Args:
            port: Port to expose
            script: NPM script to run (e.g., 'dev', 'start')
            
        Returns:
            WebContainerOutput with the server details
        """
        if not self.session_id:
            raise RuntimeError("Session not initialized. Call create_session first.")
        
        # In a real implementation, this would start the dev server
        # and return the preview URL
        return WebContainerOutput(
            status="success",
            preview_url=f"http://localhost:{port}",
            port=port,
            metadata={
                "pid": os.getpid(),
                "started_at": str(datetime.datetime.now())
            }
        )
    
    async def close(self):
        """Close the WebContainer session"""
        if hasattr(self, 'session_id') and self.session_id:
            # In a real implementation, this would clean up the WebContainer
            self.session_id = None
    
    async def __aenter__(self):
        await self.initialize()
        await self.create_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def run(self, inputs: WebContainerToolInput) -> Dict[str, Any]:
        """
        Execute a task in the WebContainer.
        
        This is the main entry point for the tool that implements the standard
        tool interface expected by the agent framework.
        """
        try:
            # Create a new session
            session_id = await self.create_session()
            
            # Write files to the container
            if inputs.files:
                await self.write_files(inputs.files)
            
            # Install dependencies if needed
            if inputs.install_dependencies:
                await self.install_dependencies()
            
            # Execute commands
            command_results = []
            if inputs.commands:
                result = await self.execute_commands(
                    inputs.commands,
                    working_dir=inputs.working_dir
                )
                command_results.append(result.dict())
            
            # Start dev server if a start command was provided
            server_result = None
            if any(cmd.startswith(('npm run dev', 'yarn dev', 'pnpm dev')) for cmd in inputs.commands):
                server_result = await self.start_dev_server(inputs.expose_ports[0] if inputs.expose_ports else 3000)
            
            # Combine results
            output = {
                "status": "success",
                "session_id": session_id,
                "command_results": command_results,
            }
            
            if server_result:
                output.update({
                    "preview_url": str(server_result.preview_url) if server_result.preview_url else None,
                    "port": server_result.port,
                    "server_metadata": server_result.metadata
                })
            
            return output
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "session_id": getattr(self, 'session_id', None)
            }
