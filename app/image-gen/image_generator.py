from fastapi import FastAPI
from pydantic import BaseModel
from diffusers import DiffusionPipeline
import torch

app = FastAPI()

# load both base & refiner
base = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
)
base.enable_model_cpu_offload()
refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    text_encoder_2=base.text_encoder_2,
    vae=base.vae,
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
)
refiner.enable_model_cpu_offload()

class GenImgRequest(BaseModel):
    # Text prompt with description of the things you want in the image to be generated
    prompt: str
    # Items you don't want in the image
    negative_prompt: str | None = None
    # Seed is used to reproduce results, same seed will give you same image in return again. Pass null for a random number.
    seed: int | None = None
    # Link to the Initial Image
    init_image: str | None = None
    # Number of steps to run the model for
    n_steps: int = 40
    # Fraction of steps to be run on each experts (ex: 80/20)
    high_noise_frac: float = 0.8


@app.post('/generate-image')
async def generate_image(request: GenImgRequest):
    # run both experts
    image = base(
        prompt=request.prompt,
        num_inference_steps=request.n_steps,
        denoising_end=request.high_noise_frac,
        output_type="latent",
    ).images
    image = refiner(
        prompt=request.prompt,
        num_inference_steps=request.n_steps,
        denoising_start=request.high_noise_frac,
        image=image,
    ).images[0]
    # return the generated image
    return {"image": image}
    

# prompt = "A majestic lion jumping from a big stone at night"


