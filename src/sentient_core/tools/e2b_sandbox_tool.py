from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Literal, Union
import os
import json
from enum import Enum

class SandboxTemplate(str, Enum):
    """Supported E2B sandbox templates"""
    PYTHON = "python3"
    NODE = "node16"
    NEXTJS = "nextjs-developer"
    VUE = "vue-developer"
    STREAMLIT = "streamlit-developer"
    GRADIO = "gradio-developer"
    CODE_INTERPRETER = "code-interpreter-v1"

class FileModel(BaseModel):
    """Model for file operations in the sandbox"""
    path: str
    content: str

class E2BSandboxToolInput(BaseModel):
    """Input model for the E2BSandboxTool."""
    template: SandboxTemplate = Field(
        SandboxTemplate.PYTHON,
        description="Template to use for the sandbox environment"
    )
    files: List[FileModel] = Field(
        default_factory=list,
        description="Files to write to the sandbox before execution"
    )
    command: Optional[str] = Field(
        None,
        description="Command to execute in the sandbox"
    )
    install_dependencies: bool = Field(
        True,
        description="Whether to install dependencies before execution"
    )
    timeout_seconds: int = Field(
        600,
        description="Maximum execution time in seconds",
        ge=30,
        le=3600
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata to include with the sandbox"
    )

class ExecutionResult(BaseModel):
    """Model for sandbox execution results"""
    status: Literal["success", "error"]
    stdout: str = ""
    stderr: str = ""
    error: Optional[str] = None
    results: List[Any] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    sandbox_id: Optional[str] = None

class E2BSandboxTool:
    """
    A tool for executing code in a secure E2B (e2b.dev) sandbox.
    
    This class provides a high-level interface to the E2B API, allowing for
    secure execution of code in isolated environments with support for
    multiple programming languages and frameworks.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the E2B sandbox tool.
        
        Args:
            api_key: Optional E2B API key. If not provided, will be read from E2B_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("E2B_API_KEY")
        if not self.api_key:
            raise ValueError(
                "E2B API key is required. "
                "Set the E2B_API_KEY environment variable or pass it to the constructor."
            )
        
        # Lazy import to avoid dependency if not used
        try:
            from e2b import Sandbox
            self.Sandbox = Sandbox
        except ImportError:
            raise ImportError(
                "E2B SDK not installed. Install with: pip install e2b"
            )
        
        self.sandbox = None
    
    async def initialize(self):
        """Initialize the E2B client if not already done"""
        if not hasattr(self, '_initialized'):
            # Any initialization that might be needed
            self._initialized = True
    
    async def create_sandbox(self, template: Union[SandboxTemplate, str]) -> str:
        """
        Create a new E2B sandbox.
        
        Args:
            template: Template to use for the sandbox
            
        Returns:
            str: The sandbox ID
        """
        await self.initialize()
        
        if isinstance(template, str):
            try:
                template = SandboxTemplate(template)
            except ValueError:
                raise ValueError(f"Invalid template: {template}")
        
        try:
            self.sandbox = await self.Sandbox.create(template.value)
            return self.sandbox.id
        except Exception as e:
            raise RuntimeError(f"Failed to create sandbox: {str(e)}")
    
    async def write_files(self, files: List[FileModel]):
        """
        Write files to the sandbox.
        
        Args:
            files: List of FileModel objects with path and content
        """
        if not self.sandbox:
            raise RuntimeError("Sandbox not initialized. Call create_sandbox first.")
        
        for file in files:
            try:
                await self.sandbox.files.write(file.path, file.content)
            except Exception as e:
                raise RuntimeError(f"Failed to write file {file.path}: {str(e)}")
    
    async def install_dependencies(self):
        """Install dependencies based on the template"""
        if not self.sandbox:
            raise RuntimeError("Sandbox not initialized. Call create_sandbox first.")
        
        # This is a simplified example - in practice, you'd want to detect
        # the package manager and dependencies based on the template
        try:
            # Check for package.json (Node.js) or requirements.txt (Python)
            if await self.sandbox.files.exists("package.json"):
                await self.sandbox.process.start("npm install")
            elif await self.sandbox.files.exists("requirements.txt"):
                await self.sandbox.process.start("pip install -r requirements.txt")
        except Exception as e:
            raise RuntimeError(f"Failed to install dependencies: {str(e)}")
    
    async def execute_command(self, command: str) -> ExecutionResult:
        """
        Execute a command in the sandbox.
        
        Args:
            command: Command to execute
            
        Returns:
            ExecutionResult with the command output
        """
        if not self.sandbox:
            raise RuntimeError("Sandbox not initialized. Call create_sandbox first.")
        
        try:
            process = await self.sandbox.process.start(command)
            await process.wait()
            
            return ExecutionResult(
                status="success",
                stdout=process.stdout,
                stderr=process.stderr,
                sandbox_id=self.sandbox.id
            )
        except Exception as e:
            return ExecutionResult(
                status="error",
                error=str(e),
                sandbox_id=self.sandbox.id
            )
    
    async def run_code(self, code: str, language: str = "python") -> ExecutionResult:
        """
        Run code in the sandbox.
        
        Args:
            code: Code to execute
            language: Programming language (python, node, etc.)
            
        Returns:
            ExecutionResult with the code execution results
        """
        if not self.sandbox:
            raise RuntimeError("Sandbox not initialized. Call create_sandbox first.")
        
        try:
            result = await self.sandbox.run_code(code, language=language)
            return ExecutionResult(
                status="success",
                stdout=result.stdout,
                stderr=result.stderr,
                results=getattr(result, "results", []),
                sandbox_id=self.sandbox.id,
                metadata={
                    "execution_time_ms": getattr(result, "execution_time_ms", None),
                    "memory_usage_mb": getattr(result, "memory_usage_mb", None)
                }
            )
        except Exception as e:
            return ExecutionResult(
                status="error",
                error=str(e),
                sandbox_id=self.sandbox.id
            )
    
    async def close(self):
        """Close the sandbox and release resources"""
        if self.sandbox:
            await self.sandbox.close()
            self.sandbox = None
    
    async def __aenter__(self):
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def run(self, inputs: E2BSandboxToolInput) -> Dict[str, Any]:
        """
        Execute a task in the E2B sandbox.
        
        This is the main entry point for the tool that implements the standard
        tool interface expected by the agent framework.
        """
        try:
            # Create sandbox
            sandbox_id = await self.create_sandbox(inputs.template)
            
            # Write files if any
            if inputs.files:
                await self.write_files(inputs.files)
            
            # Install dependencies if needed
            if inputs.install_dependencies:
                await self.install_dependencies()
            
            # Execute command if provided
            if inputs.command:
                result = await self.execute_command(inputs.command)
            else:
                # Default to running a Python script if no command is specified
                main_script = next((f for f in inputs.files if f.path.endswith('.py')), None)
                if main_script:
                    result = await self.run_code(main_script.content, "python")
                else:
                    return {
                        "status": "error",
                        "error": "No command or Python script provided"
                    }
            
            # Convert result to dict for JSON serialization
            result_dict = result.dict()
            result_dict["sandbox_id"] = sandbox_id
            return result_dict
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "sandbox_id": getattr(self.sandbox, "id", None) if hasattr(self, 'sandbox') else None
            }
