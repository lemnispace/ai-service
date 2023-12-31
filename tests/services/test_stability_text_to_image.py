import pytest
import os
import respx
from httpx import Response
from app.services.stability_text_to_image import (
    generate_image_from_text,
    get_image_gen_base_url,
)
from app.utils.types import StabilityTextToImageRequest, EngineId, TextPrompt

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
    os.environ["STABILITY_API_HOST_GEN"] = "https://test_api_host.ai/v1/gen"
    yield
    os.environ.pop("STABILITY_API_HOST_GEN", None)


@pytest.mark.asyncio
async def test_generate_image_from_text_success():
    with respx.mock() as mock:
        request = StabilityTextToImageRequest(
            text_prompts=[TextPrompt(text="Hello", weight=1.0)]
        )
        engine_id = EngineId.v1_6
        api_key = "your_api_key"

        route = mock.post(mock_url).mock(return_value=mock_text_to_image_response)
        result = await generate_image_from_text(request, engine_id, api_key)
        assert route.called
        assert result == mock_text_to_image_response.json()
        assert (
            route.calls.last.request.headers["Authorization"] == "Bearer your_api_key"
        )
        assert route.calls.last.request.headers["Content-Type"] == "application/json"
        assert route.calls.last.request.headers["Accept"] == "application/json"


@pytest.mark.asyncio
async def test_generate_image_from_text_failure():
    with respx.mock() as mock:
        route = mock.post(mock_url).mock(side_effect=Exception("Test Exception"))
        request = StabilityTextToImageRequest(
            text_prompts=[TextPrompt(text="Hello", weight=1.0)]
        )
        engine_id = EngineId.v1_6
        api_key = "your_api_key"
        with pytest.raises(Exception):
            await generate_image_from_text(request, engine_id, api_key)


def test_get_image_gen_base_url():
    engine_id = EngineId.v1_6
    os.environ["STABILITY_API_HOST_GEN"] = "test_api_url"
    assert get_image_gen_base_url(engine_id) == "test_api_url/stable-diffusion-v1-6"
