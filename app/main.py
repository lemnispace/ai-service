from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Text2ImgRequest(BaseModel):
    # Text prompt with description of the things you want in the image to be generated
    prompt: str
    # Items you don't want in the image
    negative_prompt: str | None = None
    # Seed is used to reproduce results, same seed will give you same image in return again. Pass null for a random number.
    seed: int | None = None


class Img2ImgRequest(BaseModel):
    # Text prompt with description of the things you want in the image to be generated
    prompt: str
    # Items you don't want in the image
    negative_prompt: str | None = None
    # Link to the Initial Image
    init_image: str

@app.post("/text2img")
def text2img(request: Text2ImgRequest):
    return {"prompt": request.prompt, "negative_prompt": request.negative_prompt}


@app.post("/img2img")
def img2img(request: Img2ImgRequest):
    return {"prompt": request.prompt, "negative_prompt": request.negative_prompt, "init_image": request.init_image}