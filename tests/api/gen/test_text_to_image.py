import app.api.gen.text_to_image as text_to_image
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import Response
import os
import pytest
import respx
import json

app = FastAPI()
app.include_router(text_to_image.router)
client = TestClient(app)

# mock url
mock_url = "https://test_api_host.ai/v1/gen/stable-diffusion-v1-6/text-to-image"
# mock response
mock_text_to_image_response = Response(
    status_code=200,
    json={
        "artifacts": [
            {
                "base64": "image_data",
                "seed": 2005800665,
                "finishReason": "done",
            }
        ]
    },
)


@pytest.fixture(autouse=True)
def set_env_vars():
    os.environ["STABILITY_API_HOST"] = "https://test_api_host.ai"
    os.environ["STABILITY_API_HOST_GEN"] = "https://test_api_host.ai/v1/gen"
    os.environ["STABILITY_API_KEY"] = "api_key"
    yield
    os.environ.pop("STABILITY_API_HOST", None)
    os.environ.pop("STABILITY_API_HOST_GEN", None)
    os.environ.pop("STABILITY_API_KEY", None)


def test_text_to_image_case1():
    with respx.mock() as mock:
        # Mock the response from the Stability API
        route = mock.post(mock_url).mock(return_value=mock_text_to_image_response)
        response = client.post(
            "/",
            json={
                "prompt": "Hello",
                "negative_prompt": "Goodbye",
                "height": 256,
                "width": 256,
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "artifacts": [
                {"base64": "image_data", "seed": 2005800665, "finishReason": "done"}
            ]
        }
        assert route.called
        assert route.calls.last.request.method == "POST"
        assert (
            route.calls.last.request.url
            == "https://test_api_host.ai/v1/gen/stable-diffusion-v1-6/text-to-image"
        )
        assert route.calls.last.request.headers["Authorization"] == "Bearer api_key"
        assert route.calls.last.request.headers["Content-Type"] == "application/json"
        assert route.calls.last.request.headers["Accept"] == "application/json"
        request_body = json.loads(route.calls.last.request.content)
        assert request_body == {
            "height": 256,
            "width": 256,
            "text_prompts": [
                {"text": "Hello", "weight": 1.0},
                {"text": "Goodbye", "weight": -1.0},
            ],
            "cfg_scale": 7,
        }


def test_text_to_image_case2():
    with respx.mock() as mock:
        # Mock the response from the Stability API
        route = mock.post(mock_url).mock(return_value=mock_text_to_image_response)
        response = client.post(
            "/",
            json={"prompt": "Hello", "seed": 0},
        )
        assert response.status_code == 200
        assert response.json() == {
            "artifacts": [
                {"base64": "image_data", "seed": 2005800665, "finishReason": "done"}
            ]
        }
        assert route.called
        request_body = json.loads(route.calls.last.request.content)
        assert request_body == {
            "height": 512,
            "width": 512,
            "text_prompts": [
                {"text": "Hello", "weight": 1.0},
            ],
            "cfg_scale": 7,
            "seed": 0,
        }
