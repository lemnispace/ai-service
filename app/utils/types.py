from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class EngineId(str, Enum):
    v1_6 = "stable-diffusion-v1-6"
    sdxl_v1 = "stable-diffusion-xl-1024-v1-0"


class GenTextToImageRequest(BaseModel):
    """Request to generate an image"""

    prompt: str = Field(
        description="Text prompt with description of the things you want in the image to be generated"
    )
    negative_prompt: Optional[str] = Field(
        default=None, description="Items you don't want in the image"
    )
    engine_id: Optional[EngineId] = Field(
        default=None,
        description="Stable Diffusion engine to use (v1_6 or sdxl_v1). Defaults to v1_6."
    )
    seed: Optional[int] = Field(
        default=None,
        description="Seed is used to reproduce results, same seed will give you same image in return again. Pass null for a random number.",
    )
    steps: Optional[int] = Field(
        default=None, description="Number of steps to run the model for"
    )
    samples: Optional[int] = Field(
        default=None, description="Number of samples to generate"
    )
    width: Optional[int] = Field(default=None, description="Width of the image")
    height: Optional[int] = Field(default=None, description="Height of the image")


class TextPrompt(BaseModel):
    """
    Represents a text prompt with a specific weight.
    """

    text: str  # The text of the prompt.
    weight: float  # The weight of the prompt in influencing the image generation.


class StabilityTextToImageRequest(BaseModel):
    """
    Request schema for generating an image using text prompts and specific parameters.
    """

    height: Optional[int] = Field(
        strict=True,
        default=1024,
        ge=128,
        le=1536,
        multiple_of=64,
        description="Height of the image (multiple of 64, between 128 and 1536).",
    )
    width: Optional[int] = Field(
        strict=True,
        default=1024,
        ge=128,
        le=1536,
        multiple_of=64,
        description="Width of the image (multiple of 64, between 128 and 1536).",
    )
    text_prompts: list[TextPrompt] = Field(
        min_length=1,
        description="A list of text prompts for image generation.",
    )
    cfg_scale: Optional[int] = Field(
        strict=True,
        default=7,
        ge=0,
        le=35,
        description="Controls adherence to prompt text (0 to 35, higher values keep closer to prompt).",
    )
    clip_guidance_preset: Optional[str] = Field(
        strict=True,
        pattern="^(FAST_BLUE|FAST_GREEN|NONE|SIMPLE|SLOW|SLOWER|SLOWEST)$",
        default=None,
        description="Optional preset for clip guidance (e.g., 'FAST_BLUE', 'SIMPLE').",
    )
    sampler: Optional[str] = Field(
        strict=True,
        default=None,
        pattern="^(DDIM|DDPM|K_DPMPP_2M|K_DPMPP_2S_ANCESTRAL|K_DPM_2|K_DPM_2_ANCESTRAL|K_EULER|K_EULER_ANCESTRAL|K_HEUN|K_LMS)$",
        description="Optional: Specifies the diffusion process sampler",
    )
    samples: Optional[int] = Field(
        strict=True,
        default=1,
        ge=1,
        le=10,
        description="Number of images to generate (1 to 10).",
    )
    seed: Optional[int] = Field(
        strict=True,
        default=0,
        ge=0,
        le=4294967295,
        description="Random noise seed (0 for random, up to 4294967295).",
    )
    steps: Optional[int] = Field(
        strict=True,
        default=30,
        ge=10,
        le=50,
        description="Number of diffusion steps (10 to 50).",
    )
    style_preset: Optional[str] = Field(
        strict=True,
        default=None,
        pattern="^(3d-model|analog-film|anime|cinematic|comic-book|digital-art|enhance|fantasy-art|isometric|line-art|low-poly|modeling-compound|neon-punk|origami|photographic|pixel-art|tile-texture)$",
        description="Optional style preset to guide the image model towards a particular style.",
    )
