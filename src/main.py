from fastapi import FastAPI
from src.api.endpoints import agent_endpoints

app = FastAPI(
    title="Sentient Core API",
    description="API for managing and interacting with Sentient Core agents and tasks.",
    version="0.1.0",
)

# Include the routers
app.include_router(agent_endpoints.router, prefix="/v1", tags=["Agents & Tasks"])

@app.get("/", tags=["Health Check"])
async def read_root():
    """
    Root endpoint for health check.
    """
    return {"status": "ok", "message": "Welcome to the Sentient Core API!"}
