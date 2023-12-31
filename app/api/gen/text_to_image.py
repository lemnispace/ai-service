from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from utils.types import (
    GenTextToImageRequest,
    EngineId,
)
from utils.config import get_env_variable, get_parameter_store_client, get_secret
from utils.stability_utils import get_text_to_image_api_request
from services.stability_text_to_image import generate_image_from_text


def get_stability_api_key(client: Annotated[any, Depends(get_parameter_store_client)]):
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
        engine_id = EngineId.v1_6
        txt_to_img_request = get_text_to_image_api_request(request, engine_id)
        return await generate_image_from_text(
            txt_to_img_request, engine_id, stability_api_key
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
