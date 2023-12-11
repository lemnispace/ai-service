from fastapi import APIRouter, HTTPException
from utils.types import (
    GenTextToImageRequest,
    EngineId,
)
from utils.stability_utils import get_text_to_image_api_request
from services.stability_text_to_image import generate_image_from_text

router = APIRouter()


@router.post("/")
async def text_to_image(request: GenTextToImageRequest):
    try:
        engine_id = EngineId.v1_6
        txt_to_img_request = get_text_to_image_api_request(request, engine_id)
        return await generate_image_from_text(txt_to_img_request, engine_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
