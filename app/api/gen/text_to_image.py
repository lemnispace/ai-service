from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException
import logging
from utils.types import (
    GenTextToImageRequest,
    EngineId,
)
from utils.config import get_env_variable, get_parameter_store_client, get_secret
from utils.stability_utils import get_text_to_image_api_request, StabilityRequestError
from services.stability_text_to_image import generate_image_from_text

logger = logging.getLogger(__name__)


def get_stability_api_key(client: Annotated[Any, Depends(get_parameter_store_client)]) -> str:
    name = get_env_variable("STABILITY_API_KEY_NAME", None)
    if name is None:
        raise HTTPException(
            status_code=500,
            detail="STABILITY_API_KEY_NAME environment variable not set",
        )
    return get_secret(client, name)


router = APIRouter()


@router.post("/")
async def text_to_image(
    request: GenTextToImageRequest,
    stability_api_key: Annotated[str, Depends(get_stability_api_key)],
):
    try:
        # Use engine_id from request, default to v1_6 if not provided
        engine_id = request.engine_id if request.engine_id else EngineId.v1_6
        txt_to_img_request = get_text_to_image_api_request(request, engine_id)
        return await generate_image_from_text(
            txt_to_img_request, engine_id, stability_api_key
        )
    except StabilityRequestError as e:
        logger.error(f"Stability API request error: {e}", exc_info=True)
        raise HTTPException(
            status_code=502,
            detail="Failed to generate image from external service"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in text_to_image endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
