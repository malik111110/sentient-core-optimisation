"""API router exposing E2B sandbox execution endpoints."""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from src.clients.e2b_sandbox_tool import run_in_e2b_sandbox, E2BSandboxToolInput

router = APIRouter(
    prefix="/sandbox",
    tags=["Sandbox"],
    responses={404: {"description": "Not found"}},
)


class SandboxRunRequest(BaseModel):
    """Request body for running code inside an E2B sandbox."""

    script: str = Field(..., description="Code to execute inside the sandbox.")
    language: str = Field("python", description="Language of the script, e.g., 'python' or 'node'.")


class SandboxRunResponse(BaseModel):
    """Response body containing the stdout of the executed code."""

    output: str


@router.post("/run", response_model=SandboxRunResponse, status_code=status.HTTP_200_OK)
def run_script_in_sandbox(request: SandboxRunRequest) -> SandboxRunResponse:
    """Runs the provided script inside an E2B sandbox and returns its output."""

    try:
        output = run_in_e2b_sandbox(
            E2BSandboxToolInput(script=request.script, language=request.language)
        )
        return SandboxRunResponse(output=output)
    except ValueError as ve:
        # Typically raised when E2B_API_KEY is missing
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve)) from ve
    except Exception as exc:
        # Generic catch-all to avoid leaking internal errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
