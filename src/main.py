from fastapi import FastAPI
# Updated imports for the new router structure
from src.api.routers import agent_router, task_router, sandbox_router

app = FastAPI(
    title="Sentient Core API",
    description="API for managing and interacting with Sentient Core agents and tasks.",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json", # Standard practice to prefix openapi.json
    docs_url="/api/v1/docs",            # Standard practice for Swagger UI
    redoc_url="/api/v1/redoc"           # Standard practice for ReDoc
)

# Include the new routers
app.include_router(agent_router.router, prefix="/api/v1") # agent_router already has /agents prefix
app.include_router(task_router.router, prefix="/api/v1")  # task_router already has /tasks prefix
app.include_router(sandbox_router.router, prefix="/api/v1")  # new sandbox routes

@app.get("/", tags=["Health Check"])
async def read_root():
    """
    Root endpoint for health check.
    """
    return {"status": "ok", "message": "Welcome to the Sentient Core API!"}


@app.get("/api/v1", tags=["Health Check"])
async def read_api_v1_root():
    """
    API v1 root endpoint for health check.
    """
    return {"status": "ok", "message": "Welcome to the Sentient Core API v1!"}
