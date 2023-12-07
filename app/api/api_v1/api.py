from fastapi import APIRouter
from .endpoints import text_to_image

router = APIRouter()
router.include_router(
    text_to_image.router,
    prefix="/text-to-image",
    tags=["text-to-image"],
)
