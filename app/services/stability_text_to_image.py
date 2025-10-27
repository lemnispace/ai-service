from httpx import AsyncClient, Timeout, HTTPStatusError
import os
import logging
from typing import Optional
from utils.stability_utils import StabilityRequestError
from utils.types import StabilityTextToImageRequest, EngineId
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Module-level HTTP client for connection pooling
_http_client: Optional[AsyncClient] = None


def get_http_client() -> AsyncClient:
    """Get or create the HTTP client with connection pooling and timeout configuration"""
    global _http_client
    if _http_client is None:
        _http_client = AsyncClient(
            timeout=Timeout(30.0, connect=5.0)
        )
    return _http_client


def get_image_gen_base_url(engine_id: EngineId) -> str:
    """Get the URL for the image generation API"""
    host = os.getenv("STABILITY_API_HOST_GEN")
    return f"{host}/{engine_id.value}"


async def generate_image_from_text(
    request: StabilityTextToImageRequest, engine_id: EngineId, api_key: str
):
    """Generate an image using the Stability text-to-image API"""
    client = get_http_client()
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
            try:
                error_data = response.json()
                error_message = error_data.get("message", "Unknown error")
                logger.error(
                    f"Stability API Error (status {response.status_code}): {error_message}",
                    extra={
                        "status_code": response.status_code,
                        "error_data": error_data,
                        "url": url
                    }
                )
            except Exception as json_error:
                logger.error(
                    f"Stability API returned status {response.status_code} with non-JSON response",
                    extra={
                        "status_code": response.status_code,
                        "response_text": response.text[:500]
                    }
                )
            response.raise_for_status()

        return response.json()

    except HTTPStatusError as e:
        error_message = f"HTTP error fetching image from {url}: {e}"
        logger.error(error_message, exc_info=True)
        raise StabilityRequestError(error_message, stability_request)
    except Exception as e:
        error_message = f"Error fetching image from {url}: {e}"
        logger.error(error_message, exc_info=True)
        raise StabilityRequestError(error_message, stability_request)
