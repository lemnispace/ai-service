from .types import EngineId, GenTextToImageRequest, StabilityTextToImageRequest
import logging

logger = logging.getLogger(__name__)

# Default CFG scale for Stability AI (recommended for prompt adherence)
DEFAULT_CFG_SCALE = 7


class StabilityRequestError(Exception):
    """
    Exception raised when there is an error with Stability API

    Attributes:
        message -- explanation of the error
        request -- the original request that could not be mapped
    """

    def __init__(self, message, request=None):
        self.message = message
        self.request = request
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.request}"


def get_default_image_dimensions(engine_id: EngineId) -> tuple[int, int]:
    """Get the default image dimensions for a given engine"""
    if engine_id == EngineId.v1_6:
        return (512, 512)
    elif engine_id == EngineId.sdxl_v1:
        return (1024, 1024)
    else:
        raise ValueError(f"Unknown engine id: {engine_id}")


def get_text_to_image_api_request(
    request: GenTextToImageRequest, engine_id: EngineId
) -> StabilityTextToImageRequest:
    """
    Maps GenTextToImageRequest to StabilityTxt2ImgRequest.

    Args:
    request (GenTextToImageRequest): The original request to generate an image.
    engine_id (EngineId): The Stability.ai engine id to use for generating the image.

    Returns:
    StabilityTxt2ImgRequest: Mapped request for the Stability text-to-image API.
    """

    text_prompts = [{"text": request.prompt, "weight": 1.0}]
    if request.negative_prompt:
        text_prompts.append({"text": request.negative_prompt, "weight": -1.0})

    # Get dimensions without mutating the original request
    width = request.width
    height = request.height
    if not width or not height:
        default_width, default_height = get_default_image_dimensions(engine_id)
        width = width or default_width
        height = height or default_height

    try:
        stability_request = StabilityTextToImageRequest(
            height=height,
            width=width,
            text_prompts=text_prompts,
            cfg_scale=DEFAULT_CFG_SCALE,
            samples=request.samples,
            seed=request.seed,
            steps=request.steps,
        )
        return stability_request
    except Exception as e:
        logger.error(
            f"Error mapping request to Stability API request: {e}",
            exc_info=True,
            extra={"original_request": request.model_dump()}
        )
        raise StabilityRequestError(
            f"Error mapping request to Stability API request: {e}",
            request
        )
