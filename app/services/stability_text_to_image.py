from httpx import AsyncClient
import os
from app.utils.stability_utils import StabilityRequestError
from utils.types import StabilityTextToImageRequest, EngineId
from dotenv import load_dotenv

load_dotenv()


def get_image_gen_base_url(engine_id: EngineId) -> str:
    """Get the URL for the image generation API"""
    host = os.getenv("STABILITY_API_HOST_GEN")
    return f"{host}/{engine_id.value}"


async def generate_image_from_text(
    request: StabilityTextToImageRequest, engine_id: EngineId, api_key: str
):
    """Generate an image using the Stability text-to-image API"""
    async with AsyncClient() as client:
        url = get_image_gen_base_url(engine_id)
        url = f"{url}/text-to-image"
        stability_request = request.model_dump(exclude_none=True)
        try:
            response = await client.post(
                url=url,
                json=stability_request,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
            if response.status_code != 200:
                print(f'Stability API Error: {response.json()["message"]}')
                response.raise_for_status()
            return response.json()
        except Exception as e:
            error_message = (
                f"Error fetching image with request url: {url}.",
                e,
            )
            raise StabilityRequestError(error_message, stability_request)
