from app.utils.stability_utils import get_text_to_image_api_request
from app.utils.types import EngineId, GenTextToImageRequest, StabilityTextToImageRequest


def test_get_text_to_image_api_request_case1():
    # Test case 1: Request with positive and negative prompts and width and height
    request = GenTextToImageRequest(
        prompt="Hello", negative_prompt="Goodbye", height=256, width=256
    )
    engine_id = EngineId.v1_6
    expected_request = StabilityTextToImageRequest(
        height=256,
        width=256,
        text_prompts=[
            {"text": "Hello", "weight": 1.0},
            {"text": "Goodbye", "weight": -1.0},
        ],
        cfg_scale=7,
        samples=None,
        seed=None,
        steps=None,
    )
    assert get_text_to_image_api_request(request, engine_id) == expected_request


def test_get_text_to_image_api_request_case2():
    # Test case 2: Request without width and height
    request = GenTextToImageRequest(prompt="Hello", seed=12345, samples=4, steps=40)
    engine_id = EngineId.v1_6
    expected_request = StabilityTextToImageRequest(
        height=512,
        width=512,
        text_prompts=[
            {"text": "Hello", "weight": 1.0},
        ],
        cfg_scale=7,
        samples=4,
        seed=12345,
        steps=40,
    )
    assert get_text_to_image_api_request(request, engine_id), expected_request


def test_get_text_to_image_api_request_case3():
    # Test case 3: Request with different engine id
    request = GenTextToImageRequest(prompt="Hello", seed=12345, samples=4, steps=40)
    engine_id = EngineId.sdxl_v1
    expected_request = StabilityTextToImageRequest(
        height=1024,
        width=1024,
        text_prompts=[
            {"text": "Hello", "weight": 1.0},
        ],
        cfg_scale=7,
        samples=4,
        seed=12345,
        steps=40,
    )
    assert get_text_to_image_api_request(request, engine_id), expected_request
