import os
from typing import Optional
from httpx import AsyncClient
from pydantic import BaseModel
from app.image_gen.types import (
    StabilityTxt2ImgRequest,
    GenTextToImageRequest,
    EngineId,
)


def get_default_image_dimensions(engine_id: EngineId) -> (int, int):
    """Get the default image dimensions for a given engine"""
    if engine_id == EngineId.v1_6:
        return (512, 512)
    elif engine_id == EngineId.sdxl_v1:
        return (1024, 1024)
    else:
        raise Exception(f"Unknown engine id: {engine_id}")


def get_text_to_image_api_request(
    request: GenTextToImageRequest, engine_id: EngineId
) -> StabilityTxt2ImgRequest:
    """
    Maps GenTextToImageRequest to StabilityTxt2ImgRequest.

    Args:
    request (GenTextToImageRequest): The original request to generate an image.

    Returns:
    StabilityTxt2ImgRequest: Mapped request for the Stability text-to-image API.
    """

    text_prompts = [{"text": request.prompt, "weight": 1.0}]
    if request.negative_prompt:
        text_prompts.append({"text": request.negative_prompt, "weight": -1.0})
    if not request.width or not request.height:
        width, height = get_default_image_dimensions(engine_id)
        request.width = width
        request.height = height
    try:
        stability_request = StabilityTxt2ImgRequest(
            height=request.height,
            width=request.width,
            text_prompts=text_prompts,
            cfg_scale=7,  # Assuming a default value, update as needed
            samples=request.samples,
            seed=request.seed
            if request.seed is not None
            else 0,  # Assuming 0 for random
            steps=request.steps,
        )

        return stability_request
    except Exception as e:
        print(e)
        raise Exception("Error mapping request to Stability API request")


def get_image_gen_base_url(engine_id: EngineId) -> str:
    """Get the URL for the image generation API"""
    host = os.getenv("STABILITY_API_HOST_GEN")
    return f"{host}/{engine_id.value}"


def get_api_key() -> str:
    """Get the API key for the image generation API"""
    key = os.getenv("STABILITY_API_KEY")
    if not key:
        raise Exception("Stability API key not found")
    return key


async def generate_image(request: GenTextToImageRequest):
    """Generate an image"""
    async with AsyncClient() as client:
        engine_id = EngineId.v1_6
        url = get_image_gen_base_url(engine_id)
        url = f"{url}/text-to-image"
        api_key = get_api_key()
        stability_request = get_text_to_image_api_request(
            request, engine_id
        ).model_dump(exclude_none=True)
        response = await client.post(
            url=url,
            json=stability_request,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()
