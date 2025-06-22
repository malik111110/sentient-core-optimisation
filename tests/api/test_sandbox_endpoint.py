from fastapi.testclient import TestClient
from unittest.mock import patch

from src.main import app

client = TestClient(app)


def test_sandbox_run_endpoint():
    """Happy-path test for /api/v1/sandbox/run endpoint."""

    mock_output = "Hello from sandbox"

    with patch("src.api.routers.sandbox_router.run_in_e2b_sandbox", return_value=mock_output):
        response = client.post(
            "/api/v1/sandbox/run",
            json={"script": "print('hi')", "language": "python"},
        )

    assert response.status_code == 200
    assert response.json() == {"output": mock_output}
